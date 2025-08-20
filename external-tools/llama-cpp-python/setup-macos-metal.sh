#!/usr/bin/env bash
set -euo pipefail

# llama-cpp-python macOS (Metal) setup script
# - Installs Xcode CLT if missing
# - Installs Miniforge (Conda) for arm64
# - Creates conda env and installs latest llama-cpp-python with Metal
# - Optional: downloads a GGUF model

ENV_NAME="llama"
PY_VER="3.9.16"
MODEL_ID_DEFAULT="TheBloke/CodeLlama-7B-GGUF"
MODEL_FILENAME_DEFAULT="codellama-7b.Q4_0.gguf"

help() {
  cat <<EOF
Usage: $0 [-e env_name] [-p python_version] [-m model_id] [-f model_filename] [-d model_dir]

Options:
  -e  Conda env name (default: ${ENV_NAME})
  -p  Python version (default: ${PY_VER})
  -m  Hugging Face model repo id to download (default: ${MODEL_ID_DEFAULT})
  -f  Model filename (default: ${MODEL_FILENAME_DEFAULT})
  -d  Local models directory (default: ./models)

Examples:
  $0 -e llama -p 3.9.16 -m TheBloke/CodeLlama-7B-GGUF -f codellama-7b.Q4_0.gguf -d ./models

After setup:
  export MODEL=./models/codellama-7b.Q4_0.gguf
  python -m llama_cpp.server --model "$MODEL" --n_gpu_layers 1
EOF
}

MODELS_DIR="./models"
while getopts ":e:p:m:f:d:h" opt; do
  case ${opt} in
    e) ENV_NAME="$OPTARG" ;;
    p) PY_VER="$OPTARG" ;;
    m) MODEL_ID_DEFAULT="$OPTARG" ;;
    f) MODEL_FILENAME_DEFAULT="$OPTARG" ;;
    d) MODELS_DIR="$OPTARG" ;;
    h) help; exit 0 ;;
    *) help; exit 1 ;;
  esac
done

echo "[1/6] Checking Xcode Command Line Tools..."
if ! xcode-select -p >/dev/null 2>&1; then
  echo "Xcode CLT not found. Installing..."
  xcode-select --install || true
  echo "Please complete Xcode CLT installation and re-run this script if it prompts a GUI installer."
fi

echo "[2/6] Ensuring Miniforge (arm64) installed..."
if ! command -v conda >/dev/null 2>&1; then
  echo "Installing Miniforge for arm64..."
  URL="https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh"
  TMP_SCRIPT="/tmp/Miniforge3-MacOSX-arm64.sh"
  curl -L "$URL" -o "$TMP_SCRIPT"
  bash "$TMP_SCRIPT" -b
  rm -f "$TMP_SCRIPT"
  # shellcheck disable=SC1090
  source "$HOME/miniforge3/etc/profile.d/conda.sh"
else
  # shellcheck disable=SC1090
  source "$(conda info --base)/etc/profile.d/conda.sh"
fi

echo "[3/6] Creating/activating conda env: ${ENV_NAME} (Python ${PY_VER})..."
if ! conda env list | grep -q "^${ENV_NAME}\s"; then
  conda create -y -n "${ENV_NAME}" "python=${PY_VER}"
fi
conda activate "${ENV_NAME}"

echo "[4/6] Installing llama-cpp-python with Metal..."
pip uninstall -y llama-cpp-python || true
export CMAKE_ARGS="-DGGML_METAL=on"
pip install -U --no-cache-dir "llama-cpp-python[server]"

python - <<'PY'
import pkg_resources
v = pkg_resources.get_distribution('llama-cpp-python').version
print(f"llama-cpp-python version: {v}")
PY

echo "[5/6] Preparing models directory: ${MODELS_DIR}"
mkdir -p "${MODELS_DIR}"

if command -v huggingface-cli >/dev/null 2>&1; then
  echo "[6/6] Optionally downloading GGUF model via huggingface-cli..."
  echo "Downloading: ${MODEL_ID_DEFAULT}/${MODEL_FILENAME_DEFAULT} -> ${MODELS_DIR}"
  huggingface-cli download "${MODEL_ID_DEFAULT}" "${MODEL_FILENAME_DEFAULT}" --local-dir "${MODELS_DIR}" || echo "Skipping download (ensure you have access or correct filename)."
else
  echo "huggingface-cli not found. To download models, run: pip install -U huggingface_hub && huggingface-cli download '${MODEL_ID_DEFAULT}' '${MODEL_FILENAME_DEFAULT}' --local-dir '${MODELS_DIR}'"
fi

echo "\n✅ Setup complete. To start the server:"
echo "  conda activate ${ENV_NAME}"
echo "  export MODEL=${MODELS_DIR}/${MODEL_FILENAME_DEFAULT}"
echo "  python -m llama_cpp.server --model \"$MODEL\" --n_gpu_layers 1 --host 0.0.0.0 --port 8080"