# Prestartup script for ComfyUI-AutoTextCleaner & AnimeAI
# Enables CORS for local companion tools such as mask_tool.html
try:
    from comfy.cli_args import args
    if not args.enable_cors_header:
        args.enable_cors_header = "*"
except Exception:
    pass

# Enable TensorFloat-32 (TF32) hardware acceleration on supported NVIDIA GPUs without quality loss
try:
    import torch
    if torch.cuda.is_available():
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        torch.backends.cudnn.benchmark = True
except Exception:
    pass
