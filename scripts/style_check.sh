#!/bin/bash

filenames="exomerge.py unit_tests/exomerge_unit_test.py"

pep8_exe="pycodestyle"
pyflakes_exe="pyflakes"

script_dir=$(dirname $0)

# check for pep8
echo -n "Checking for pycodestyle..."
version=$("$pep8_exe" --version)
if [ "$version" == "" ]; then
    echo " NOT FOUND!"
    exit 1
fi
echo " v$version"

# check for pyflakes
echo -n "Checking for pyflakes..."
version=$("$pyflakes_exe" --version)
if [ "$version" == "" ]; then
    echo " NOT FOUND!"
    exit 1
fi
echo " v$version"

# store success code
success=0

echo
echo "Beginning tests!"

# run tests on each file
for filename in $filenames; do
    echo
    echo "Checking $filename..."
    tempfile=$(mktemp)
    cp "$filename" "$tempfile"
    echo "- Copied file to $tempfile"

    # check for trailing whitespace
    echo -n "- Trailing whitespaces..."
    check=$(grep -r '[[:blank:]]$' -c "$filename")
    if [ $check -ne 0 ]
    then
        echo " FOUND $check LINES"
        echo
        grep -r -n '[[:blank:]]$' $filename
        echo
        read -n 1 -p "Should I delete the trailing whitespace [y/N]? " ans
        echo
        if [[ ! "$ans" =~ ^[Yy]$ ]]
        then
	          echo
	          echo "Style checks will not pass."
            success=1
        else
            # delete trailing whitespace
            sed -i 's/[ \t]*$//' "$filename"
            echo "Trailing whitepace removed."
        fi
    else
        echo " none found"
    fi

    # check for tabs
    echo -n "- Checking for tabs..."
    tab_lines=$(grep $'\t' -c "$filename")
    if [ $tab_lines -ne 0 ]
    then
        echo " FOUND $tab_lines LINES"
        echo
        grep $'\t' -n -B 2 -A 2 "$filename" | sed -e 's/\t/    /g'
        echo
        read -n 1 -p "Should I replace tabs with 4 spaces [y/N]? " ans
        echo
        if [[ ! "$ans" =~ ^[Yy]$ ]]
        then
	          echo
	          echo "Style checks will not pass."
            success=1
        else
            sed -i 's/\t/    /g' "$filename"
            echo "Tabs replaced."
        fi
    else
        echo " none found"
    fi

    # check for tabs
    echo -n "- Checking for todo/debug statements..."
    tempfile=$(mktemp)
    grep -e 'TODO' -e 'DEBUG' "$filename" &> "$tempfile"
    bad_lines=$(cat $tempfile | wc -l | tr -d '\n')
    if [ $bad_lines -ne 0 ]
    then
        success=1
        echo " FOUND $bad_lines LINES"
        echo
        cat $tempfile
        echo
        echo "Correct these and run again."
    else
        echo " none found"
    fi
    rm $tempfile

    # run node_set/side_set discrepancy checker script
    echo -n "- Running node_set/side_set checker..."
    tempfile=$(mktemp)
    python $script_dir/check_node_side_discrepancies.py "$filename" &> $tempfile
    status=$?
    if [ $status -ne 0 ]
    then
        success=1
        echo " ERRORS FOUND"
        echo
        cat $tempfile
        echo
        echo "Correct these and run again."
    else
        echo " passed"
    fi
    rm $tempfile

    # run pep8
    echo -n "- Running pycodestyle..."
    tempfile=$(mktemp)
    "$pep8_exe" "$filename" &> $tempfile
    status=$?
    if [ $status -ne 0 ]
    then
        success=1
        echo " ERRORS FOUND"
        echo
        cat $tempfile
        echo
        echo "Correct these and run again."
    else
        echo " passed"
    fi
    rm $tempfile

    # run pyflakes
    echo -n "- Running pyflakes..."
    tempfile=$(mktemp)
    "$pyflakes_exe" "$filename" &> $tempfile
    status=$?
    if [ $status -ne 0 ]
    then
        success=1
        echo " ERRORS FOUND"
        echo
        cat $tempfile
        echo
        echo "Correct these and run again."
    else
        echo " passed"
    fi
    rm $tempfile

done

if [ $success -eq 0 ]; then
    echo
    echo "Style check was successful!"
else
    echo
    echo "Style check failed."
    echo "Correct issues and rerun."
fi

exit $success
