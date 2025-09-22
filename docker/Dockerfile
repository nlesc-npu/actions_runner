FROM rocm/dev-ubuntu-24.04:6.4.3-complete

# update packages
RUN apt update -y
RUN apt upgrade -y

# Install required packages for xrt runtime
RUN apt install -y libboost-filesystem-dev libboost-program-options-dev

# Install required packages for xrt build from source
RUN apt install -y jq pkg-config ocl-icd-dev ocl-icd-opencl-dev libssl-dev rapidjson-dev systemtap-sdt-dev wget pybind11-dev

# Install required packages for mlir-aie
RUN apt install -y build-essential cmake python3-venv python3-pip uuid-dev

# Install other tools
RUN apt install -y git

# Create non-root runner user
RUN useradd -ms /bin/bash actions
RUN usermod -a -G render actions
RUN usermod -a -G video actions

USER actions

# Install MLIR-AIE
WORKDIR /opt/mlir-aie
RUN git clone -b v1.1.0 https://github.com/Xilinx/mlir-aie .
RUN python3 -m pip install --break-system-packages --user --upgrade pip
RUN python3 -m pip install --break-system-packages --user cmake
RUN python3 -m pip install --break-system-packages --user mlir_aie -f https://github.com/Xilinx/mlir-aie/releases/expanded_assets/v1.1.0
RUN python3 -m pip install --break-system-packages --user llvm-aie -f https://github.com/Xilinx/llvm-aie/releases/download/nightly/llvm_aie-19.0.0.2025041501+b2a279c1-py3-none-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
RUN python3 -m pip install --break-system-packages --user -r python/requirements.txt
RUN HOST_MLIR_PYTHON_PACKAGE_PREFIX=aie python3 -m pip install --break-system-packages --user -r python/requirements_extras.txt

# Install XRT (manually instead of through provided script as we do not need the kernel module)
USER root
WORKDIR /opt/mlir-aie/utils

RUN eval $(grep ^XDNA_SHA= build_drivers.sh) && \
    git clone https://github.com/amd/xdna-driver.git && \
    cd xdna-driver && \
    git checkout "$XDNA_SHA" && \
    git submodule update --init --recursive

RUN export XDNA_SRC_DIR=$(realpath xdna-driver) && \
    cd "$XDNA_SRC_DIR/xrt/build" && \
    ./build.sh -npu -opt && \
    cd "$XDNA_SRC_DIR/xrt/build/Release" && \
    apt install -y ./*.deb && \
    cd "$XDNA_SRC_DIR/build" && \
    ./build.sh -release -nokmod && \
    ./build.sh -package -nokmod && \
    cd "$XDNA_SRC_DIR/build/Release" && \
    apt install -y ./*.deb

USER actions

# Install github actions runner
WORKDIR /home/actions/actions-runner
COPY actions-runner-linux-x64-2.328.0.tar.gz runner.tar.gz
RUN tar xzf runner.tar.gz && rm runner.tar.gz
COPY start.sh start.sh

ENTRYPOINT ["./start.sh"]
