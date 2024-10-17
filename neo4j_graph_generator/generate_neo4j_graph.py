from neo4j import GraphDatabase, RoutingControl
import xml.dom.minidom


URI = "neo4j://localhost:7687"
AUTH = ("mulval", "12345678")

docs = xml.dom.minidom.parse("test.xml")

arcs = docs.getElementsByTagName("arc")


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


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
    # print()
    command = f'MATCH (a:node {{nodeId: "{edgeSrc}"}}), (b:node {{nodeId: "{edgeDst}"}}) CREATE (a)-[:TO]->(b)'
    createEdgesCommands.append(command)

    # srcNode = childNodes.getElementsByTagName("src")


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

    labels = [":" + x for x in labels]

    nodeLabels = " ".join(labels)

    # print(description)

    nodeId = getText(vertex.getElementsByTagName("id")[0].childNodes)
    # print(nodeId)

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
