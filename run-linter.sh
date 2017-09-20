directories="integration-tests ui-tests perf-tests"
fail=0

function prepare_venv() {
    virtualenv -p python3 venv && source venv/bin/activate && python3 `which pip3` install pycodestyle
}

echo "----------------------------------------------------"
echo "Running Python linter against following directories:"
echo $directories
echo "----------------------------------------------------"
echo

ls -1

[ "$NOVENV" == "1" ] || prepare_venv || exit 1

# checks for the whole directories
for directory in $directories
do
    files=`find $directory -path $directory/venv -prune -o -name '*.py' -print`

    for source in $files
    do
        echo $source
        pycodestyle $source
        if [ $? -eq 0 ]
        then
            echo "    Pass"
        else
            echo "    Fail"
            let "fail++"
        fi
    done
done


if [ $fail -eq 0 ]
then
    echo "All checks passed"
else
    echo "Linter fail, $fail source files need to be fixed"
    exit 1
fi
