"""
llama_cpp_adapter: Run a local OpenAI-compatible server backed by llama-cpp-python.
- macOS Metal via --n_gpu_layers + GGML_METAL build
- Reads config from environment variables for easy integration with CAI-CERBERUS

Usage:
  python external-tools/llama-cpp-python/llama_cpp_adapter.py

Env:
  LLAMACPP_MODEL: path to *.gguf file
  LLAMACPP_HOST: default 0.0.0.0
  LLAMACPP_PORT: default 8080
  LLAMACPP_THREADS: default auto (-1)
  LLAMACPP_CTX: context size (default 4096)
  LLAMACPP_N_GPU_LAYERS: default 1 (Metal on macOS)
  LLAMACPP_CHAT_FORMAT: optional chat template

This launches the same server as `python -m llama_cpp.server` with provided options.
"""
from __future__ import annotations
import os
import sys
import argparse
import subprocess
import shlex
from typing import Optional


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenAI-compatible llama-cpp server wrapper")
    parser.add_argument("--model", type=str, default=os.getenv("LLAMACPP_MODEL"), help="Path to GGUF model")
    parser.add_argument("--host", type=str, default=os.getenv("LLAMACPP_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("LLAMACPP_PORT", "8080")))
    parser.add_argument("--threads", type=int, default=int(os.getenv("LLAMACPP_THREADS", "-1")), help="Number of threads (-1 for auto)")
    parser.add_argument("--ctx-size", type=int, default=int(os.getenv("LLAMACPP_CTX", "4096")))
    parser.add_argument("--n-gpu-layers", type=int, default=int(os.getenv("LLAMACPP_N_GPU_LAYERS", "1")))
    parser.add_argument("--chat-format", type=str, default=os.getenv("LLAMACPP_CHAT_FORMAT"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model_path = args.model
    if not model_path:
        print("ERROR: Provide --model or LLAMACPP_MODEL path to a .gguf file", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(model_path):
        print(f"ERROR: Model file not found: {model_path}", file=sys.stderr)
        sys.exit(1)

    cmd = [
        sys.executable,
        "-m",
        "llama_cpp.server",
        "--model",
        model_path,
        "--host",
        args.host,
        "--port",
        str(args.port),
    ]

    if args.ctx_size:
        cmd += ["--n_ctx", str(args.ctx_size)]
    if args.n_gpu_layers is not None:
        cmd += ["--n_gpu_layers", str(args.n_gpu_layers)]
    if args.threads is not None and args.threads != -1:
        cmd += ["--n_threads", str(args.threads)]
    if args.chat_format:
        cmd += ["--chat_format", args.chat_format]

    print(
        "Starting llama-cpp OpenAI-compatible server via CLI...\n"
        f"  model: {model_path}\n"
        f"  host: {args.host}\n"
        f"  port: {args.port}\n"
        f"  ctx: {args.ctx_size}\n"
        f"  n_gpu_layers: {args.n_gpu_layers}\n"
        f"  threads: {args.threads if args.threads != -1 else 'auto'}\n"
        f"  command: {shlex.join(cmd)}"
    )

    # Run the server in the foreground, forwarding stdio
    try:
        subprocess.call(cmd)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()