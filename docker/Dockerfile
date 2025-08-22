FROM rocm/dev-ubuntu-24.04:6.4.3-complete

# update packages
RUN apt update -y
RUN apt upgrade -y

# Install required packages for xrt
RUN apt install -y libboost-filesystem-dev libboost-program-options-dev

# Install required packages for mlir-aie
RUN apt install -y build-essential cmake python3-venv python3-pip uuid-dev

# Install other tools
RUN apt install -y git

# Create non-root runner user
RUN useradd -ms /bin/bash actions
RUN usermod -a -G render actions
RUN usermod -a -G video actions

USER actions

# Install MLIR-AIE V1.0.1
WORKDIR /opt/mlir-aie
RUN git clone https://github.com/Xilinx/mlir-aie -b v1.0.1 .
RUN python3 -m pip install --break-system-packages --user --upgrade pip
RUN python3 -m pip install --break-system-packages --user mlir_aie -f https://github.com/Xilinx/mlir-aie/releases/expanded_assets/v1.0.1
RUN python3 -m pip install --break-system-packages --user https://github.com/Xilinx/llvm-aie/releases/download/nightly/llvm_aie-19.0.0.2025041501+b2a279c1-py3-none-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
RUN python3 -m pip install --break-system-packages --user -r python/requirements.txt
RUN HOST_MLIR_PYTHON_PACKAGE_PREFIX=aie python3 -m pip install --break-system-packages --user -r python/requirements_extras.txt

# Install github actions runner
WORKDIR /home/actions/actions-runner
COPY actions-runner-linux-x64-2.328.0.tar.gz runner.tar.gz
RUN tar xzf runner.tar.gz && rm runner.tar.gz
COPY start.sh start.sh

ENTRYPOINT ["./start.sh"]
