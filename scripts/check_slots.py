import json

def check_workflow(path):
    print(f"Checking {path}...")
    with open(path, encoding='utf-8') as f:
        wf = json.load(f)
    nodes = {n['id']: n for n in wf['nodes']}
    invalid_links = []
    for l in wf['links']:
        lid, s_id, s_slot, d_id, d_slot, ltype = l
        s_node = nodes.get(s_id)
        d_node = nodes.get(d_id)
        s_ok = s_node and s_slot < len(s_node.get('outputs', []))
        d_ok = d_node and d_slot < len(d_node.get('inputs', []))
        if not s_ok or not d_ok:
            invalid_links.append((lid, s_id, s_slot, d_id, d_slot, bool(s_ok), bool(d_ok)))
        else:
            print(f"Valid: Link {lid}: Node {s_id} ({s_node['type']}) -> Node {d_id} ({d_node['type']}) [{ltype}]")

    print(f"\nTotal links: {len(wf['links'])}, Invalid links: {len(invalid_links)}")
    for inv in invalid_links:
        print("  Invalid:", inv)

check_workflow('animeai_workflow.json')
