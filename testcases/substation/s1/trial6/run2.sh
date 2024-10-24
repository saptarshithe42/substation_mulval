vulExistsLibraryFile="vulExistsLibrary.txt"
vulExistsProgramFile="vulExistsProgram.txt"
vulPropertyListFile="vulPropertyList.txt"
programUsesLibrary="programUsesLibrary.txt"
goal="goal.txt"
haclRules="hacl_rules.txt"
hostsInfo="hosts_info.txt"
customRules="custom_rules2.P"
inputFile="input_file.P"
runFiles="run_files"

export MULVALROOT=~/mulval
export PATH=$PATH:"$MULVALROOT/bin":"$MULVALROOT/utils":/usr/local/bin/xsb-5.0.0/bin

BASEPATH=$MULVALROOT/custom_additions

cd $runFiles

>"$inputFile"

cat $goal >>$inputFile
cat $haclRules >>$inputFile
cat $BASEPATH/$vulPropertyListFile >>$inputFile
cat $BASEPATH/$vulExistsLibraryFile >>$inputFile
cat $BASEPATH/$vulExistsProgramFile >>$inputFile
cat $BASEPATH/$programUsesLibrary >>$inputFile
cat $hostsInfo >>$inputFile

cd ..

mv ./$runFiles/$inputFile ./$inputFile

graph_gen.sh $inputFile -p -v -a $customRules
