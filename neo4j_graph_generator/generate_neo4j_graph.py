from neo4j import GraphDatabase, RoutingControl
import xml.dom.minidom


URI = "neo4j://localhost:7687"
AUTH = ("mulval", "12345678")
attackGraph = "AttackGraph.xml"


docs = xml.dom.minidom.parse(attackGraph)

arcs = docs.getElementsByTagName("arc")


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


indegreeCount = {}
outdegreeCount = {}

createEdgesCommands = []

for arc in arcs:
    childNodes = arc.childNodes

    srcNode = childNodes[1]
    src = getText(srcNode.childNodes)

    dstNode = childNodes[3]
    dst = getText(dstNode.childNodes)

    # print("src = ", src, ", dst = ", dst)

    edgeSrc = dst
    edgeDst = src

    if edgeDst in indegreeCount:
        indegreeCount[edgeDst] += 1
    else:
        indegreeCount[edgeDst] = 1

    if edgeSrc in outdegreeCount:
        outdegreeCount[edgeSrc] += 1
    else:
        outdegreeCount[edgeSrc] = 1

    command = f'MATCH (a:node {{nodeId: "{edgeSrc}"}}), (b:node {{nodeId: "{edgeDst}"}}) CREATE (a)-[:TO]->(b)'
    createEdgesCommands.append(command)


for cmd in createEdgesCommands:
    print(cmd)


vertices = docs.getElementsByTagName("vertex")

createNodeCommands = []


for vertex in vertices:
    fact = vertex.getElementsByTagName("fact")[0]
    description = getText(fact.childNodes)

    labels = ["node"]

    if "RULE" in description:
        labels.append("rule")

    if "vulExists" in description:
        labels.append("vulnerability")

    if "hacl" in description:
        labels.append("hacl_rule")

    if "networkServiceInfo" in description:
        labels.append("network_service_info")

    nodeId = getText(vertex.getElementsByTagName("id")[0].childNodes)

    if nodeId not in outdegreeCount and indegreeCount[nodeId] == 1:
        labels.append("goal")

    labels = [":" + x for x in labels]
    nodeLabels = " ".join(labels)

    command = f'CREATE ({nodeLabels} {{nodeId : "{nodeId}", description : "{description}"}})'

    createNodeCommands.append(command)


for cmd in createNodeCommands:
    print(cmd)


with GraphDatabase.driver(URI, auth=AUTH) as driver:
    with driver.session(database="neo4j") as session:
        transaction = session.begin_transaction()
        for command in createNodeCommands:
            transaction.run(command)

        for command in createEdgesCommands:
            transaction.run(command)
        transaction.commit()

print("successful")
