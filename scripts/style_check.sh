#!/bin/bash

filenames="exomerge.py unit_tests/exomerge_unit_test.py"

pep8_exe="pep8"
pyflakes_exe="pyflakes"

# check for pep8
echo -n "Checking for pep8..."
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

# run tests on each file
for filename in $filenames; do
    tempfile=$(mktemp)
    cp "$filename" "$tempfile"
    echo "Copied file to $tempfile"

    # check for trailing whitespace
    echo
    echo "Checking $filename for trailing whitespace..."
    check=$(grep -r '[[:blank:]]$' -c "$filename")
    if [ $check -ne 0 ]
    then
        echo "Found $check lines with trailing whitespace."
        read -n 1 -p "Should I delete trailing whitespace [y/N]? " ans
        echo
        if [[ ! "$ans" =~ ^[Yy]$ ]]
        then
	          echo
	          echo "Style checks did not pass."
            success=1
        else
            # delete trailing whitespace
            sed -i 's/[ \t]*$//' "$filename"
            echo "Trailing spaces removed."
        fi
    else
        echo "No trailing whitespace found."
    fi


    # check for tabs
    echo
    echo "Checking for tabs..."
    tab_lines=$(grep $'\t' -c "$filename")
    if [ $tab_lines -ne 0 ]
    then
        echo "Found "$tab_lines" lines with tabs."
        echo
        grep $'\t' -n -B 2 -A 2 "$filename" | sed -e 's/\t/    /g'
        echo
        read -n 1 -p "Should I replace tabs with 4 spaces [y/N]? " ans
        echo
        if [[ ! "$ans" =~ ^[Yy]$ ]]
        then
	          echo
	          echo "Style checks did not pass."
            success=1
        else
            sed -i 's/\t/    /g' "$filename"
            echo "Tabs replaced."
        fi
    else
        echo "No tabs found!"
    fi

    # run pep8
    echo
    echo "Running pep8..."
    pep8 "$filename"
    status=$?
    if [ $status -ne 0 ]
    then
        success=1
        echo
        echo "Errors found.  Correct these and run again."
    else
        echo "Passed!"
    fi

    # run pyflakes
    echo
    echo "Running pyflakes..."
    pyflakes "$filename"
    status=$?
    if [ $status -ne 0 ]
    then
        success=1
        echo
        echo "Errors found.  Correct these and run again."
    else
        echo "Passed!"
    fi

done

exit $success
