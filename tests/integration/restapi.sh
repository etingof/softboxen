#!/bin/bash
#
# Invoke CLI simulator REST API server and issue a series of REST API
# calls to create an example network device (box).
#
# Fail the entire script on any failure.
#

set -e

RESTAPI_CONF=$(mktemp /tmp/softboxen.XXXXXX)

USAGE=$(cat << EOF
Usage: $0 [options]
  --help                          Usage help message
  --recreate-db                   Populate REST API DB with some data
  --keep-running                  Keep REST API servers running
EOF)


recreate_db=no
keep_running=no

POSITIONAL=()
while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        --help)
            echo Synopsis: invoke REST API servers, optionally initialize
            echo the underlying DB.
            echo "$USAGE"
            exit 0
            ;;
        --recreate-db)
            recreate_db=yes
            shift # past argument
            ;;
        --keep-running)
            keep_running=yes
            shift # past argument
            ;;
    esac
done

sed -e 's/DEBUG = True/DEBUG = False/g' $(pwd)/conf/softboxen.conf > $RESTAPI_CONF

if [ $recreate_db = "yes" ]; then
    softboxen-restapi \
        --config $RESTAPI_CONF \
        --recreate-db
fi

softboxen-restapi \
    --config $RESTAPI_CONF &

RESTAPI_PID=$!

function cleanup()
{
    rm -fr  $RESTAPI_CONF
    kill $RESTAPI_PID && true
}

trap cleanup EXIT

echo Waiting for dust to settle down...

sleep 10

if [ $recreate_db = "yes" ]; then
    bash conf/bootstraps/create-box-port-vlan.sh
fi

if [ $keep_running = "yes" ]; then
    cat -
fi

exit 0
