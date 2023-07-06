#!/bin/bash

#script to sort several files in a row
#to execute, type in cmd line: ./sort.sh <sort_file> <first_run> <last_run>
#change the fout variable for a different output file name
#change the mv line for a different sort file output name

echo ''
echo 'Sort file:' $1
echo 'Sorting from run' $2 'to run' $3 '...'
echo ''

for i in `seq $2 $3`
do
      nin=${i}
    num=${#nin}
        
    if [ $num -eq 1 ]; then
       nout=0000${i}
    elif [ $num -eq 2 ]; then
       nout=000${i}
    elif [ $num -eq 3 ]; then
       nout=00${i}
    else
       echo Invalid file name!
    fi
        
    fin=run${nout}
        fout=run${nin}.root

    echo
    echo Input: $fin   Output: $fout

        hupsort -p 49292 -f "$1" ../data/"$fin"

        mv output.root ../RootFiles/GLWtreedata/"$fout"
done
