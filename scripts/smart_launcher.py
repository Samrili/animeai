"""
Hardware-aware launcher for AnimeAI Studio.
Probes CUDA device properties and available VRAM to select appropriate ComfyUI
memory flags (--lowvram / --reserve-vram / --highvram) before spawning the server.
"""

import os
import sys
import subprocess


def detect_hardware():
    gpu_info = {
        "has_cuda": False,
        "name": "CPU Only",
        "vram_gb": 0.0,
        "flags": ["--cpu", "--preview-method", "none", "--enable-cors-header", "*"]
    }

    try:
        import torch
        if torch.cuda.is_available():
            dev_idx = 0
            dev_name = torch.cuda.get_device_name(dev_idx)
            vram_bytes = torch.cuda.get_device_properties(dev_idx).total_memory
            vram_gb = vram_bytes / (1024 ** 3)
            gpu_info["has_cuda"] = True
            gpu_info["name"] = dev_name
            gpu_info["vram_gb"] = round(vram_gb, 2)

            if vram_gb < 5.5:
                flags = ["--lowvram", "--reserve-vram", "0.3", "--preview-method", "none", "--enable-cors-header", "*"]
                profile = "LOW VRAM (Dynamic Offloading)"
            elif vram_gb <= 9.5:
                flags = ["--reserve-vram", "0.5", "--preview-method", "none", "--enable-cors-header", "*"]
                profile = "BALANCED VRAM (Protected DWM)"
            else:
                flags = ["--highvram", "--reserve-vram", "0.5", "--preview-method", "none", "--enable-cors-header", "*"]
                profile = "HIGH PERFORMANCE (Full VRAM)"

            gpu_info["flags"] = flags
            gpu_info["profile"] = profile
            return gpu_info
    except Exception:
        pass

    gpu_info["profile"] = "CPU SAFE MODE"
    return gpu_info


def clean_stale_ports(port=8188):
    if sys.platform == "win32":
        try:
            cmd = f'netstat -aon | findstr :{port} | findstr LISTENING'
            output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
            for line in output.strip().split("\n"):
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    if pid.isdigit() and int(pid) != os.getpid():
                        subprocess.run(
                            f"taskkill /f /pid {pid}",
                            shell=True,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
        except Exception:
            pass


def clean_lock_files(base_dir):
    lock_file = os.path.join(base_dir, "ComfyUI", "user", "comfyui.db.lock")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
        except Exception:
            pass


def launch():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    os.environ["CUDA_MODULE_LOADING"] = "LAZY"
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

    hw = detect_hardware()

    print("=" * 65)
    print("      AnimeAI Studio - Universal Hardware Engine")
    print("=" * 65)
    print(f" Target Workstation : {hw['name']}")
    print(f" Available VRAM     : {hw['vram_gb']} GB" if hw['has_cuda'] else " Available Device   : CPU (No CUDA GPU detected)")
    print(f" Runtime Profile    : {hw['profile']}")
    print(f" Optimized Flags    : {' '.join(hw['flags'])}")
    print("=" * 65)

    clean_stale_ports(8188)
    clean_lock_files(base_dir)

    tab_script = os.path.join(base_dir, "scripts", "open_browser_tabs.py")
    if os.path.exists(tab_script):
        if sys.platform == "win32":
            subprocess.Popen(["pythonw", tab_script], shell=False)
        else:
            subprocess.Popen([sys.executable, tab_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    comfy_main = os.path.join(base_dir, "ComfyUI", "main.py")
    cmd = [
        sys.executable,
        comfy_main,
        "--listen", "127.0.0.1",
        "--port", "8188",
        "--auto-launch",
        "--enable-manager",
    ] + hw["flags"]

    try:
        sys.exit(subprocess.call(cmd))
    except KeyboardInterrupt:
        print("\nStudio shutting down gracefully...")
        sys.exit(0)


if __name__ == "__main__":
    launch()
