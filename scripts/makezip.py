import zipfile
import os
from pathlib import Path
import re

script_path = Path(os.path.abspath(__file__))
markers_folder = script_path.parent.parent
zip_name = "haskha_markers.zip"
exclude = [".git/*", "scripts/*", ".github/*", zip_name]

print(markers_folder)
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
    for folder_name, subfolders, filenames in os.walk(markers_folder):
        for filename in filenames:
            file_path = os.path.join(folder_name, filename)
            relpath = os.path.relpath(file_path, markers_folder)
            found = False
            for ex in exclude:
                if re.match(ex, relpath):
                    found = True
                    break
            
            if not found:
                print(relpath)
                zip_ref.write(file_path, arcname=relpath)
