import json

with open('ref_workflow.json', encoding='utf-8') as f:
    data = json.load(f)

for node in data['nodes']:
    title = node.get('title', '')
    print(f"ID: {node['id']:2d} | Type: {node['type']:32s} | Title: {title}")
