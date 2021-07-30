#!/bin/sh

source $(dirname "$0")/vars.sh
source $ROOT_FOLDER/$VIRTUAL_ENV/bin/activate

YARN="yarn"
PRETTIER_SCSS=".prettiercss"

function format_python {
    file=$1
    # autopep8 --in-place --exit-code $file
    black --quiet --check $file
    code=$?
    if [ $code == 1 ]; then
        echo "File $file automatically changed, please verify"
        black $file
        isort $file
    fi

    #pylint -rn $file
    flake8 $file
    lint_code=$?
    if [ $lint_code -ne 0 ]; then
        code=3
    fi

    return $code
}

function format_typescript {
    current=$(pwd)
    ret_code=0
    cd "$ROOT_FOLDER/$FRONT_FOLDER"
    file=$1
    yarn run prettier --check $file >/dev/null
    code=$?
    if [ $code -eq 1 ]; then
        echo "File $FRONT_FOLDER/$file automatically changed, please verify"
        yarn run prettier --write $file >/dev/null
        ret_code=2
    elif [ $code -eq 2 ]; then
        ret_code=1
    fi

    yarn run eslint $file
    code=$?
    if [ $code -ne 0 ]; then
        ret_code=3
    fi

    cd $current
    return $ret_code
}

function sumarize_code {
    prev=$1
    new=$2
    ret_code=$1
    if [ $prev -eq 0 ] || ( [ $prev -eq 2 ] && [ $new -ne 0 ] ) || [ $new -eq 3 ]; then
        ret_code=$new
    fi
    return $ret_code
}

# Get against what we are commiting
if git rev-parse --verify HEAD >/dev/null 2>&1
then
	against=HEAD
else
	# Initial commit: diff against an empty tree object
	against=$(git hash-object -t tree /dev/null)
fi

files_to_commit=$(git diff --cached --name-only $against)

# Check style code
typescript_style_code=0
python_style_code=0
OLD_IFS=$IFS
IFS=$'\n'
for file in $files_to_commit; do
    if [ -e $file ]; then
        if [ ${file: -3} == ".py" ]; then
            format_python $file
            sumarize_code $python_style_code $?
            python_style_code=$?
        elif [ ${file: -4} == ".tsx" ] || [ ${file: -3} == ".ts" ]; then
            subfile=${file:6}
            prev=$typescript_style_code
            format_typescript $subfile
            new=$?
            sumarize_code $typescript_style_code $new
            typescript_style_code=$?
        fi
    fi
done
IFS=$OLD_IFS

$ROOT_FOLDER/manage.py test
python_tests=$?

if [ $python_style_code == 3 ] || [ $typescript_style_code == 3 ]; then
    echo "Please check the linted files"
    exit 3
elif [ $python_style_code == 2 ] || [ $typescript_style_code == 2 ]; then
    echo "Please review automatic formatting"
    exit 2
elif [ $python_style_code == 1 ] || [ $typescript_style_code == 1 ]; then
    echo "There was an error autoformating, please check it"
    exit 1
fi

if [ $python_tests -ne 0 ]; then
    echo "Tests are not passing, please solve it"
    exit 1
fi

# exit 1
# find atom_platform -name "*.py" -exec autopep8 --in-place {} \;
