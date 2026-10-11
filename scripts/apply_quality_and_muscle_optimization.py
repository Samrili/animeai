import json
import os

# Grounded, semi-realistic anime style that stays faithful to the real scene
POSITIVE_PROMPT = (
    "masterpiece, best quality, semi-realistic anime style, clean aesthetic, realistic anatomy, "
    "athletic male boxer with natural defined muscles, natural skin tones, clean outlines, "
    "grounded cinematic lighting, natural street lamp light, calm night atmosphere, anime film still"
)

# Suppress cyberpunk, neon clutter, oversaturation and chaotic hallucinations
NEGATIVE_PROMPT = (
    "worst quality, low quality, normal quality, (cyberpunk, neon glow, oversaturated colors, "
    "high contrast burns, glowing lights, chaotic background, clutter, noisy textures:1.3), "
    "(flat cartoon, 3d render, plastic skin, distorted anatomy, mutated hands, bad hands:1.2), blurry, artifacts"
)

def update_workflow_grounded(path):
    print(f"Applying grounded semi-realistic anime optimization to: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        wf = json.load(f)

    for n in wf['nodes']:
        nid = n['id']
        ntype = n.get('type')

        # 1. Node 24: Positive Prompt (Grounded Semi-Realistic Anime)
        if nid == 24:
            print("  Updating Node 24 (Positive Prompt)...")
            n['widgets_values'] = [POSITIVE_PROMPT]

        # 2. Node 7: Negative Prompt (Anti-Neon, Anti-Clutter)
        elif nid == 7:
            print("  Updating Node 7 (Negative Prompt)...")
            n['widgets_values'] = [NEGATIVE_PROMPT]

        # 3. Node 159: LoraLoader (more_details at 0.25 - subtle, clean, no clutter)
        elif nid == 159:
            print("  Updating Node 159 (LoraLoader: more_details -> 0.25)...")
            n['widgets_values'] = ["more_details.safetensors", 0.25, 0.25]

        # 4. Node 131: ControlNetApplyAdvanced (strength: 0.85, end_percent: 0.88 - faithful to reality)
        elif nid == 131:
            print("  Updating Node 131 (ControlNet: strength 0.85, end 0.88)...")
            n['widgets_values'] = [0.85, 0.0, 0.88]

        # 5. Node 3: KSampler (dpmpp_2m, karras, denoise: 0.48, cfg: 5.2, steps: 20)
        elif nid == 3:
            print("  Updating Node 3 (KSampler: dpmpp_2m, denoise 0.48, cfg 5.2)...")
            # [seed, 'fixed', steps, cfg, sampler_name, scheduler, denoise]
            n['widgets_values'][2] = 20           # steps
            n['widgets_values'][3] = 5.2          # cfg (natural colors, no oversaturation)
            n['widgets_values'][4] = "dpmpp_2m"   # deterministic, smooth ODE sampler
            n['widgets_values'][5] = "karras"     # scheduler
            n['widgets_values'][6] = 0.48         # denoise (grounded, realistic transformation)

        # 6. Node 106: AnimateDiff Loader (motion_scale: 0.90 - balanced motion)
        elif nid == 106:
            print("  Updating Node 106 (ADE_AnimateDiffLoaderWithContext -> 0.90)...")
            n['widgets_values'][2] = 0.90

        # 7. Node 136: ImageScale Downscale (use 'area' instead of 'nearest-exact' to eliminate pixel blocks)
        elif nid == 136:
            print("  Updating Node 136 (ImageScale -> 'area')...")
            n['widgets_values'][0] = "area"

        # 8. Node 152: ADE_AnimateDiffLoRALoader (disable ZoomIn camera drift)
        elif nid == 152:
            print("  Updating Node 152 (Motion LoRA strength -> 0.0)...")
            n['widgets_values'][1] = 0.0

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(wf, f, indent=2)

    print(f"Successfully updated: {path}\n")

if __name__ == '__main__':
    update_workflow_grounded('animeai_workflow.json')
    fast_wf = 'ComfyUI/user/default/workflows/anime_vid2vid_workflow_fast.json'
    if os.path.exists(fast_wf):
        update_workflow_grounded(fast_wf)
