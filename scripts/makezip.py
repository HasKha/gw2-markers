import zipfile
import os
from pathlib import Path
import fnmatch

script_path = Path(os.path.abspath(__file__))
markers_folder = script_path.parent.parent
zip_name = "haskha_markers.zip"
includes = ["*.xml", "Data/*", "README.md", "LICENSE"]

with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
    for folder_name, subfolders, filenames in os.walk(markers_folder):
        for filename in filenames:
            file_path = os.path.join(folder_name, filename)
            relpath = os.path.relpath(file_path, markers_folder)

            if any(fnmatch.fnmatch(relpath, include) for include in includes):
                print(f"adding: {relpath}")
                zip_ref.write(file_path, arcname=relpath)
                