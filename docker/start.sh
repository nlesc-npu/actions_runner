#!/bin/bash
. /opt/mlir-aie/utils/env_setup.sh

./config.sh --url ${URL} --token ${REG_TOKEN} --name ${RUNNER_NAME} --labels ${RUNNER_LABEL} --no-default-labels --replace --unattended --disableupdate --ephemeral

cleanup() {
    ./config.sh remove --token ${REG_TOKEN}
}

unset URL
unset REG_TOKEN
unset RUNNER_NAME
unset RUNNER_LABEL

trap 'cleanup; exit 143' TERM
trap 'cleanup; exit 130' INT

./run.sh &
wait $!

