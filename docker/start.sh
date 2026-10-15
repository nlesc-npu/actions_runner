#!/bin/bash
URL=""
REG_TOKEN=""
RUNNER_NAME=""
RUNNER_LABELS=""

while getopts "u:t:n:l:" opt; do
  case "$opt" in
    u)
      URL=${OPTARG}
      ;;
    t)
      REG_TOKEN=${OPTARG}
      ;;
    n)
      RUNNER_NAME=${OPTARG}
      ;;
    l)
      RUNNER_LABELS=${OPTARG}
      ;;
  esac
done

# Remove arguments to avoid them being picked up by the sourced script of mlir-aie
shift $#

if [[ -z "${URL}" || -z "${REG_TOKEN}" || -z "${RUNNER_NAME}"  || -z "${RUNNER_LABELS}" ]] then
    echo "Not all options are set, exiting"
    exit 1
fi

. /opt/mlir-aie/utils/env_setup.sh
export PATH=$HOME/.local/bin:$PATH
./config.sh --url ${URL} --token ${REG_TOKEN} --name ${RUNNER_NAME} --labels ${RUNNER_LABELS} --no-default-labels --replace --unattended --disableupdate --ephemeral

cleanup() {
    ./config.sh remove --token ${REG_TOKEN}
}

trap 'cleanup; exit 143' TERM
trap 'cleanup; exit 130' INT

./run.sh &
wait $!

