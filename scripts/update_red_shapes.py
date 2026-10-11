import json
import os

def update_workflow(path):
    print(f"Updating {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        wf = json.load(f)

    for n in wf['nodes']:
        if n['id'] == 205:
            n['title'] = "Auto Text & Red Shape Cleaner"
            n['size'] = [340, 260]
            n['widgets_values'] = [
                True,
                "Box (Tum Kutu ve Sekil Koruma)",
                0.40,
                4,
                5,
                "Telea",
                True,
                "Red (Kirmizi Halka ve Oklar)",
                0.60,
                4,
                8,
                "Inpaint Background (Arka Plani Temizle - Onerilen)"
            ]

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(wf, f, indent=2)
    print(f"Updated {path} successfully!")

update_workflow('animeai_workflow.json')
fast_wf = 'ComfyUI/user/default/workflows/anime_vid2vid_workflow_fast.json'
if os.path.exists(fast_wf):
    update_workflow(fast_wf)
