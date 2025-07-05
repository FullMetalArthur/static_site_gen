from page_generators import *
import shutil
import sys

source = "static"
destination = "docs"
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
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()





                
