FROM rocm/dev-ubuntu-26.04:10.1.0-full

# update packages
RUN apt update -y
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:amd-team/xrt
RUN apt update -y
RUN apt upgrade -y

# Install XRT
RUN apt install -y libxrt2 libxrt-npu2 libxrt-dev libxrt-utils libxrt-utils-npu

# Install required packages for mlir-aie
RUN apt install -y build-essential cmake python3-venv python3-pip uuid-dev

# Install other tools
RUN apt install -y git wget

# Install HIP fortran bindings
RUN wget https://github.com/ROCm/hipfort/archive/refs/tags/rocm-10.1.0.tar.gz -O hipfort-rocm-10.1.0.tar.gz && \
    tar xzf hipfort-rocm-10.1.0.tar.gz && \
    rm hipfort-rocm-10.1.0.tar.gz

RUN cd hipfort-rocm-10.1.0 && \
    cmake -S . -B build -DCMAKE_C_COMPILER=amdclang -DCMAKE_CXX_COMPILER=amdclang++ -DCMAKE_Fortran_COMPILER=amdflang -DCMAKE_INSTALL_PREFIX=/opt/rocm/ && \
    make -C build -j install

# Install OpenMPI
WORKDIR /root/
RUN wget https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.11.tar.gz && \
    tar xzf openmpi-5.0.11.tar.gz && \
    rm openmpi-5.0.11.tar.gz

WORKDIR /root/
RUN cd openmpi-5.0.11 && \
    CC=amdclang CXX=amdclang++ FC=amdflang ./configure --with-rocm --prefix=/usr && \
    make -j install


# Create non-root runner user
ARG VIDEOGID
ARG RENDERGID
RUN groupadd -og ${VIDEOGID} hostvideo
RUN groupadd -og ${RENDERGID} hostrender
RUN useradd -ms /bin/bash actions
RUN usermod -a -G hostrender actions
RUN usermod -a -G hostvideo actions

USER actions

# Install MLIR-AIE
WORKDIR /opt/mlir-aie
RUN git clone -b v1.4.4 https://github.com/Xilinx/mlir-aie .
RUN python3 -m pip install --break-system-packages --user --upgrade pip
RUN python3 -m pip install --break-system-packages --user cmake
RUN python3 -m pip install --break-system-packages --user mlir_aie -f https://github.com/Xilinx/mlir-aie/releases/expanded_assets/v1.4.4
RUN python3 -m pip install --break-system-packages --user -r utils/peano-requirements.txt

USER actions

# Add file required for xrt-smi validation
WORKDIR /home/actions/.local/share/xrt/2.25.00/amdxdna/bins
RUN git clone https://github.com/Xilinx/VTD /tmp/VTD && \
    mv /tmp/VTD/archive/strx/* . && \
    rm -r /tmp/VTD

# Install github actions runner
WORKDIR /home/actions/actions-runner
RUN wget https://github.com/actions/runner/releases/download/v2.337.0/actions-runner-linux-x64-2.337.0.tar.gz && \
    tar xzf actions-runner-linux-x64-2.337.0.tar.gz && \
    rm  actions-runner-linux-x64-2.337.0.tar.gz
COPY start.sh start.sh

ENTRYPOINT ["./start.sh"]
