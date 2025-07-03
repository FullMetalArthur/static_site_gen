import os
import shutil
import sys
from copystatic import copy_files
from markdown_to_HTML_node import markdown_to_html_node

source = "static"
destination = "public"
is_exists = os.path.exists(destination)


def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    if is_exists:
        print("Deleting directory...")
        shutil.rmtree(destination)

    print("Creating directory destination...")
    os.makedirs(destination, exist_ok=True)
    print("Copying static files...")
    copy_files(source, destination)

    print("Generating content...")
    generate_pages_recursive("content", "template.html", "public")

main()


def extract_title(markdown):
    for line in markdown.split("\n"):
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
        elif cleaned_line.startswith("# ") and len(cleaned_line) > 2:
            header = cleaned_line[2:]
            return header
    raise ValueError("missing header")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()
    title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    final_html = final_html.replace('href="/',  f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    dir_name = os.path.dirname(dest_path)
    os.makedirs(dir_name, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    for item in os.listdir(dir_path_content):
        joined_path_content = os.path.join(dir_path_content, item)
        joined_dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(joined_path_content) and item[-3:] == ".md":
            generate_page(joined_path_content, template_path, joined_dest_path.replace(".md", ".html"), basepath)
        elif os.path.isdir(joined_path_content):
            generate_pages_recursive(joined_path_content, template_path, joined_dest_path, basepath)




                
