import json
import os

def clean_workflow_file(path):
    print(f"Cleaning workflow: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        wf = json.load(f)

    # 1. Remove dead/invalid links (311, 312, 316)
    valid_links = []
    removed_link_ids = {311, 312, 316}
    for l in wf['links']:
        if l[0] in removed_link_ids:
            print(f"  Removing dead/duplicate link {l[0]}: {l}")
            continue
        valid_links.append(l)

    wf['links'] = valid_links

    # 2. Remove unused orphaned nodes 133 and 160
    wf['nodes'] = [n for n in wf['nodes'] if n['id'] not in {133, 160}]

    nodes = {n['id']: n for n in wf['nodes']}

    # 3. Rebuild output links for all nodes exactly matching active links
    for n in wf['nodes']:
        for out in n.get('outputs', []):
            out['links'] = []

    for l in wf['links']:
        lid, s_id, s_slot, d_id, d_slot, ltype = l
        assert s_id in nodes, f"Source node {s_id} missing"
        assert d_id in nodes, f"Target node {d_id} missing"
        src_node = nodes[s_id]
        dst_node = nodes[d_id]
        src_node['outputs'][s_slot]['links'].append(lid)
        dst_node['inputs'][d_slot]['link'] = lid

    wf['last_node_id'] = max(n['id'] for n in wf['nodes'])
    wf['last_link_id'] = max(l[0] for l in wf['links'])

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(wf, f, indent=2)

    print(f"  Successfully cleaned {path}! Active nodes: {len(wf['nodes'])}, Active links: {len(wf['links'])}\n")

if __name__ == '__main__':
    clean_workflow_file('animeai_workflow.json')
    fast_wf = 'ComfyUI/user/default/workflows/anime_vid2vid_workflow_fast.json'
    if os.path.exists(fast_wf):
        clean_workflow_file(fast_wf)
