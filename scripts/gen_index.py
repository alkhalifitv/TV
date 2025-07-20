# scripts/gen_index.py
import os

def generate_index_html(folder_path='deploy'):
    readme_html = ""
    readme_path = os.path.join(folder_path, 'README.md')

    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            md_lines = f.readlines()

        # Markdown sederhana → HTML
        for line in md_lines:
            if line.startswith("# "):
                readme_html += f"<h1>{line[2:].strip()}</h1>\n"
            elif line.startswith("## "):
                readme_html += f"<h2>{line[3:].strip()}</h2>\n"
            elif line.startswith("- "):
                readme_html += f"<li>{line[2:].strip()}</li>\n"
            elif "[Di SINI]" in line:
                parts = line.split('](')
                if len(parts) == 2:
                    text = parts[0].replace('[', '')
                    url = parts[1].replace(')', '').strip()
                    readme_html += f'<p><a href="{url}">{text}</a></p>\n'
            else:
                readme_html += f"<p>{line.strip()}</p>\n"

    items = sorted(os.listdir(folder_path))
    links = ""
    for item in items:
        if item == 'index.html':
            continue
        links += f'<li><a href="{item}">{item}</a></li>\n'

    html_content = f"""<html>
<head>
  <title>Index of /</title>
  <meta charset=\"UTF-8\">
</head>
<body>
{readme_html}
<h2>Index of /</h2>
<ul>
{links}
</ul>
</body>
</html>"""

    with open(os.path.join(folder_path, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_index_html()
