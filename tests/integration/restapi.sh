#!/bin/bash
#
# Invoke CLI simulator REST API server and issue a series of REST API
# calls to create an example network device (box).
#
# Fail the entire script on any failure.
#

set -e

RESTAPI_CONF=$(mktemp /tmp/softboxen.XXXXXX)

sed -e 's/DEBUG = True/DEBUG = False/g' $(pwd)/conf/softboxen.conf > $RESTAPI_CONF

softboxen-restapi \
    --config $RESTAPI_CONF \
    --recreate-db

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

bash conf/bootstraps/create-box-port-vlan.sh

exit 0
