import json
import os

def update_workflow_selective_delete(path):
    print(f"Updating Node 205 in {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        wf = json.load(f)

    for n in wf['nodes']:
        if n['id'] == 205:
            n['title'] = "Auto Text & Shape Cleaner (Kutusuz Harf Silici)"
            n['size'] = [360, 320]
            n['widgets_values'] = [
                True,                                              # enabled
                "Box (Tum Kutu ve Sekil Koruma)",                  # mask_mode
                0.40,                                              # min_confidence
                4,                                                 # mask_dilation
                5,                                                 # inpaint_radius
                "Telea",                                           # inpaint_method
                "None (Tumunu Koru - Silme Yapma)",                # delete_region_mode
                "",                                                # delete_custom_zones (örn: "top-left" veya "0 0 300 100")
                "",                                                # delete_keywords (örn: "tiktok, watermark, @")
                True,                                              # letter_level_cleaning (kutusuz sadece harfler)
                True,                                              # protect_red_shapes
                "Red (Kirmizi Halka ve Oklar)",                    # shape_color_mode
                0.60,                                              # shape_sensitivity
                4,                                                 # shape_dilation
                8,                                                 # shape_padding
                "Inpaint Background (Arka Plani Temizle - Onerilen)" # clean_mode
            ]

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(wf, f, indent=2)

    print(f"Updated {path} successfully!\n")

if __name__ == '__main__':
    update_workflow_selective_delete('animeai_workflow.json')
    fast_wf = 'ComfyUI/user/default/workflows/anime_vid2vid_workflow_fast.json'
    if os.path.exists(fast_wf):
        update_workflow_selective_delete(fast_wf)
