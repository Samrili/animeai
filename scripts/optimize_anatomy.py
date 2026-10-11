import json
import os

def update_workflow_anatomy(path):
    print(f"Applying anatomy and stability optimizations to: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        wf = json.load(f)

    for n in wf['nodes']:
        nid = n['id']
        # 1. ControlNet Apply Advanced (Node 131): Balanced guidance at 0.72 until 76% to let muscles form
        if nid == 131:
            print("  Updating Node 131 (ControlNetApplyAdvanced)...")
            n['widgets_values'] = [0.72, 0.0, 0.76]

        # 2. ScaledSoftControlNetWeights (Node 126): Keep base_multiplier at 0.95
        elif nid == 126:
            print("  Updating Node 126 (ScaledSoftControlNetWeights)...")
            n['widgets_values'] = [0.95, False, 1]

        # 3. AnimateDiff Context Options (Node 122): context_overlap 6 for smooth limb transitions
        elif nid == 122:
            print("  Updating Node 122 (ADE_LoopedUniformContextOptions)...")
            # [context_length, context_stride, context_overlap, closed_loop, fuse_method, use_on_equal_length, start_percent, guarantee_steps]
            n['widgets_values'] = [16, 1, 6, False, 'pyramid', False, 0, 1]

        # 4. KSampler (Node 3): Steps 20, CFG 7.8, denoise 0.67 for sharp muscle convergence
        elif nid == 3:
            print("  Updating Node 3 (KSampler)...")
            # [seed, 'fixed', steps, cfg, sampler_name, scheduler, denoise]
            n['widgets_values'][2] = 20  # steps 20
            n['widgets_values'][3] = 7.8 # cfg 7.8
            n['widgets_values'][6] = 0.67 # denoise 0.67

        # 5. Negative Prompt (Node 7): Targeted anti-drift, anti-flatness, anti-baggy tokens
        elif nid == 7:
            print("  Updating Node 7 (Negative Prompt)...")
            n['widgets_values'] = [
                "worst quality, low quality, normal quality, lowres, (flat shading, soft skin without muscle, undefined flabby muscles, skinny, fat, oversized baggy clothes, oversized puffy hoodie:1.25), blurry, out of focus, motion blur, bad anatomy, bad hands, mutated hands, missing fingers, extra fingers, malformed limbs, deformed feet, floating limbs, disconnected limbs, mutation, gross proportions, body drift, morphing limbs, signature, watermark, jpeg artifacts, deformed"
            ]

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(wf, f, indent=2)

    print(f"Successfully updated {path}!\n")

if __name__ == '__main__':
    update_workflow_anatomy('animeai_workflow.json')
    fast_wf = 'ComfyUI/user/default/workflows/anime_vid2vid_workflow_fast.json'
    if os.path.exists(fast_wf):
        update_workflow_anatomy(fast_wf)
