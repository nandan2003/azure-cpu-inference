#!/bin/bash

set -e

echo "=== CPU BENCHMARK SETUP STARTED ==="

# -------------------------------
# 1. System Packages
# -------------------------------
echo "[1/4] Installing system dependencies..."
sudo apt update
sudo apt install -y \
    build-essential \
    cmake \
    python3-dev \
    python3-venv \
    git \
    curl \
    wget

# -------------------------------
# 2. Clone & Build llama.cpp
# -------------------------------
echo "[2/4] Cloning and building llama.cpp..."

if [ ! -d "llama.cpp" ]; then
    git clone https://github.com/ggerganov/llama.cpp.git
else
    echo "llama.cpp already exists. Pulling latest..."
    cd llama.cpp
    git pull
    cd ..
fi

cd llama.cpp
mkdir -p build
cd build

echo "Compiling with AVX2 and FMA optimizations..."
cmake .. -DLLAMA_AVX2=ON -DLLAMA_FMA=ON -DLLAMA_BUILD_TESTS=OFF
make -j$(nproc)

cd ../../

# -------------------------------
# 3. Python Environment
# -------------------------------
echo "[3/4] Creating Python virtual environment..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install psutil tabulate huggingface_hub llama-cpp-python

# -------------------------------
# 4. Validation
# -------------------------------
echo "[4/4] Validating installation..."

echo "CPU flags:"
grep -o 'avx2' /proc/cpuinfo | head -n 1 || true
grep -o 'fma' /proc/cpuinfo | head -n 1 || true

echo "llama.cpp build:"
./llama.cpp/build/bin/llama-cli --help >/dev/null 2>&1 && echo "llama.cpp OK" || echo "llama.cpp failed to build"

echo "llama-cpp-python version:"
python3 -c "import llama_cpp, sys; print('llama-cpp-python OK:', llama_cpp.__version__)"

echo "=== SETUP COMPLETE ==="
