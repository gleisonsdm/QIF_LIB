#!/bin/bash

THIS=$(pwd)

LRED='\e[1;31m'
LGREEN='\e[1;32m'
LBLUE='\e[1;34m'
LPURPLE='\e[1;35m'
LCYAN='\e[1;36m'

RED='\e[0;31m'
GREEN='\e[0;32m'
BLUE='\e[0;34m'
PURPLE='\e0;35m'
CYAN='\e[0;36m'

NC='\e[0m'

function runFile() {
    file="$1"
    
    ## JUST FOR TESTING, limit to the exercise
    #if [ "${file}" != "4_4.py" ]; then
    #    return
    #fi

    index=$(echo "$f" | cut -f1 -d".")
    tests_name="${THIS}/../testing/tests_$index/"
    tests=$(ls "$tests_name")
    for t in $tests; do
        test_file="${THIS}/../testing/tests_$index/$t"
        python3 ${file} ${test_file}
    done
}

function runPyPrograms() {
    cd ../python_src
    files=$(ls)
    for f in $files; do
        echo -e "${LPURPLE}====================${NC}"
        echo -e "${LPURPLE}Running $f${NC}"
        echo -e "${LPURPLE}====================${NC}"
	value=$(runFile "$f")
	echo -e "${LCYAN}${value}${NC}"
    done
}

function main() {
    runPyPrograms
}

main
