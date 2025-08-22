#!/bin/bash
# Like mlir-aie's env_setup.sh, without installation of Python packages

export MLIR_AIE_INSTALL_DIR="$(pip show mlir_aie 2>/dev/null | grep ^Location: | awk '{print $2}')/mlir_aie"
export PEANO_INSTALL_DIR="$(pip show llvm-aie 2>/dev/null | grep ^Location: | awk '{print $2}')/llvm-aie"

XRTSMI=`which xrt-smi`
if ! test -f "$XRTSMI"; then
  source /opt/xilinx/xrt/setup.sh
fi

NPU=`/opt/xilinx/xrt/bin/xrt-smi examine | grep -E "NPU Phoenix|NPU Strix|NPU Strix Halo|NPU Krackan|RyzenAI-npu[1456]"`
# Check if the current environment is NPU2
# npu4 => Strix, npu5 => Strix Halo, npu6 => Krackan
if echo "$NPU" | grep -qiE "NPU Strix|NPU Strix Halo|NPU Krackan|RyzenAI-npu[456]"; then
    export NPU2=1
else
    export NPU2=0
fi

export PATH=${MLIR_AIE_INSTALL_DIR}/bin:${PATH}
export PYTHONPATH=${MLIR_AIE_INSTALL_DIR}/python:${PYTHONPATH}
export LD_LIBRARY_PATH=${MLIR_AIE_INSTALL_DIR}/lib:${LD_LIBRARY_PATH}

echo ""
echo "Note: Peano has not been added to PATH so that it does not conflict with"
echo "      system clang/clang++. It can be found in: \$PEANO_INSTALL_DIR/bin"
echo ""
echo "PATH              : $PATH"
echo "LD_LIBRARY_PATH   : $LD_LIBRARY_PATH"
echo "PYTHONPATH        : $PYTHONPATH"
