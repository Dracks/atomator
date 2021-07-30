#!/bin/sh

source $(dirname "$0")/vars.sh

if [ "$VIRTUAL_ENV" == "" ]; then
    echo "Virtual_env not configured, please create the config.sh file"
    exit 1
fi
source $ROOT_FOLDER/$VIRTUAL_ENV

function install_hook {
    hook=$1
    hook_file="$ROOT_FOLDER/.git/hooks/$hook"

    if [ -e $hook_file ]; then
        echo "** WARNING: $hook hook is not installed correctly **"
    else
        cat > $hook_file << EOF
#!/bin/sh

${ROOT_FOLDER}/scripts/${hook}.sh

EOF
        chmod +x $hook_file
    fi
}

function install_node_dependencies {
    current=$(pwd)
    cd $ROOT_FOLDER/$FRONT_FOLDER
    yarn
    cd $current
}

pip install -r requirements.txt
pip install -r requirements_lint.txt

install_node_dependencies

install_hook pre-commit