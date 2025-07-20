import os

def generate_index(path):
    items = sorted(os.listdir(path), key=lambda x: x.lower())
    lines = ['<html><body><h2>Index of {}</h2><ul>'.format(path)]
    if path != '.':
        parent = os.path.relpath(os.path.join(path, '..'), '.')
        lines.append(f'<li><a href="{parent}/">../ (parent dir)</a></li>')
    for item in items:
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            lines.append(f'<li><a href="{item}/">{item}/</a></li>')
        else:
            lines.append(f'<li><a href="{item}">{item}</a></li>')
    lines.append('</ul></body></html>')
    with open(os.path.join(path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

def walk_and_generate(root='.'):
    for dirpath, dirnames, filenames in os.walk(root):
        # skip .git and .github folders biar gak bikin indexnya
        if '.git' in dirpath or '.github' in dirpath:
            continue
        generate_index(dirpath)

if __name__ == '__main__':
    walk_and_generate()
