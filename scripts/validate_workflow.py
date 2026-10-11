import json

def clean_and_validate_workflow(path):
    with open(path, encoding='utf-8') as f:
        wf = json.load(f)

    nodes = {n['id']: n for n in wf['nodes']}
    links = {l[0]: l for l in wf['links']}
    print(f"\n=== Cleaning & Validating {path} ===")

    # 1. Ensure all node output links arrays match actual links in links table
    # Reset all node output links to only those actually defined in wf['links']
    for n in wf['nodes']:
        for out in n.get('outputs', []):
            out['links'] = []

    for lid, l in links.items():
        src_id, src_slot, dst_id, dst_slot, ltype = l[1], l[2], l[3], l[4], l[5]
        assert src_id in nodes, f"Source node {src_id} not found"
        assert dst_id in nodes, f"Target node {dst_id} not found"
        src_node = nodes[src_id]
        dst_node = nodes[dst_id]
        src_out = src_node['outputs'][src_slot]
        dst_in = dst_node['inputs'][dst_slot]
        src_out['links'].append(lid)
        dst_in['link'] = lid

    print(f"Verified and synced all {len(links)} links in {path}!")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(wf, f, indent=2)

if __name__ == '__main__':
    clean_and_validate_workflow('animeai_workflow.json')
    clean_and_validate_workflow('ComfyUI/user/default/workflows/anime_vid2vid_workflow_fast.json')
