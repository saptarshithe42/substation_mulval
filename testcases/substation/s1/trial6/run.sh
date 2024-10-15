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

cd $runFiles

>"$inputFile"

cat $goal >>$inputFile
cat $haclRules >>$inputFile
cat $vulPropertyListFile >>$inputFile
cat $vulExistsLibraryFile >>$inputFile
cat $vulExistsProgramFile >>$inputFile
cat $programUsesLibrary >>$inputFile
cat $hostsInfo >>$inputFile

cd ..

mv ./$runFiles/$inputFile ./$inputFile

source init_mulval_vars.sh

graph_gen.sh $inputFile -p -v -a $customRules
