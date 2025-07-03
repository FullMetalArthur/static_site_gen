import os
import shutil

def copy_files(source, destination):

    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"{src_path} succesfully copied into {dest_path}")

        if os.path.isdir(src_path):
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
                print(f"creating new directory... {dest_path}")
            copy_files(src_path, dest_path)