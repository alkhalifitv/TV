import os

def generate_index_html(folder_path='deploy'):
    ignore = {'.git', '.github', '.gitignore', '.DS_Store'}
    items = sorted(os.listdir(folder_path))
    html = ['<html><head><title>Index of TV Repo</title></head><body>']
    html.append('<h2>Index of /</h2><ul>')
    for item in items:
        if item in ignore:
            continue
        full_path = os.path.join(folder_path, item)
        display_name = item + '/' if os.path.isdir(full_path) else item
        href = item + ('/' if os.path.isdir(full_path) else '')
        html.append(f'<li><a href="{href}">{display_name}</a></li>')
    html.append('</ul></body></html>')

    with open(os.path.join(folder_path, 'index.html'), 'w') as f:
        f.write('\n'.join(html))

if __name__ == '__main__':
    generate_index_html()
