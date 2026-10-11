"""
AnimeAI - Smart Universal Hardware Launcher
Detects host GPU architecture, total VRAM, and operating system to dynamically
apply the optimal memory management flags (--lowvram / --normalvram / --highvram)
preventing Out-Of-Memory crashes across any computer configuration.
"""

import os
import sys
import time
import subprocess
import shutil

def detect_hardware():
    """
    Analyzes available computing hardware and determines optimal ComfyUI runtime flags.
    """
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

            # Determine optimal flags based on hardware profile
            if vram_gb < 5.5:
                # Low VRAM budget (< 6GB) -> aggressively offload models
                flags = ["--lowvram", "--reserve-vram", "0.3", "--preview-method", "none", "--enable-cors-header", "*"]
                profile = "LOW VRAM (Dynamic Offloading)"
            elif vram_gb <= 9.5:
                # Balanced VRAM budget (6GB - 9GB) -> standard execution + DWM headroom
                flags = ["--reserve-vram", "0.5", "--preview-method", "none", "--enable-cors-header", "*"]
                profile = "BALANCED VRAM (Protected DWM)"
            else:
                # High VRAM budget (> 10GB) -> full VRAM residency
                flags = ["--highvram", "--reserve-vram", "0.5", "--preview-method", "none", "--enable-cors-header", "*"]
                profile = "HIGH PERFORMANCE (Full VRAM)"

            gpu_info["flags"] = flags
            gpu_info["profile"] = profile
            return gpu_info
    except Exception as e:
        pass

    gpu_info["profile"] = "CPU SAFE MODE"
    return gpu_info

def clean_stale_ports(port=8188):
    """
    Closes any zombie processes holding the ComfyUI port.
    """
    if sys.platform == "win32":
        try:
            cmd = f'netstat -aon | findstr :{port} | findstr LISTENING'
            output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
            for line in output.strip().split("\n"):
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    if pid.isdigit() and int(pid) != os.getpid():
                        subprocess.run(f"taskkill /f /pid {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

def clean_lock_files(base_dir):
    """
    Removes database locks left by abrupt shutdowns.
    """
    lock_file = os.path.join(base_dir, "ComfyUI", "user", "comfyui.db.lock")
    if os.path.exists(lock_file):
        try:
            os.remove(lock_file)
        except Exception:
            pass

def launch():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)

    # 1. Set optimal PyTorch memory allocators
    os.environ["CUDA_MODULE_LOADING"] = "LAZY"
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

    # 2. Hardware profile detection
    hw = detect_hardware()

    print("=" * 65)
    print("      AnimeAI Studio - Universal Hardware Engine")
    print("=" * 65)
    print(f" Target Workstation : {hw['name']}")
    print(f" Available VRAM     : {hw['vram_gb']} GB" if hw['has_cuda'] else " Available Device   : CPU (No CUDA GPU detected)")
    print(f" Runtime Profile    : {hw['profile']}")
    print(f" Optimized Flags    : {' '.join(hw['flags'])}")
    print("=" * 65)

    # 3. Clean environment
    clean_stale_ports(8188)
    clean_lock_files(base_dir)

    # 4. Spawn background browser opener
    tab_script = os.path.join(base_dir, "scripts", "open_browser_tabs.py")
    if os.path.exists(tab_script):
        if sys.platform == "win32":
            subprocess.Popen(["pythonw", tab_script], shell=False)
        else:
            subprocess.Popen([sys.executable, tab_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 5. Launch ComfyUI
    comfy_main = os.path.join(base_dir, "ComfyUI", "main.py")
    cmd = [sys.executable, comfy_main, "--listen", "127.0.0.1", "--port", "8188", "--auto-launch", "--enable-manager"] + hw["flags"]
    
    try:
        sys.exit(subprocess.call(cmd))
    except KeyboardInterrupt:
        print("\nStudio shutting down gracefully...")
        sys.exit(0)

if __name__ == "__main__":
    launch()
