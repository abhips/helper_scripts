"""
    script to unzip all the zip files and install any otf/ttf fonts in that.
    It should cleanup the directory after the installation
"""

import zipfile, os, pathlib, shutil

print()
# recieve download directory path, if non existing create one
download_dir_path = input("Enter the download directory: ")
download_directory = pathlib.Path(download_dir_path)
if not download_directory.exists():
    os.mkdir(download_dir_path)


print()
# create font directory if it is non existing
font_dir_path = os.path.expanduser("~/.fonts")
font_directory = pathlib.Path(font_dir_path)
if not font_directory.exists():
    os.mkdir(font_dir_path)

print()
# find all the font files in the directory
for root, dirs, files in os.walk(download_dir_path, topdown='true'):
    for file in files:
        if file[-4:] == '.zip':
            zip_file = os.path.join(root, file)
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(download_dir_path)

print()
font_files = {}
directory_paths = []
for root, dirs, files in os.walk(download_dir_path, topdown='true'):
    font_files = {font_file:root for font_file in files if font_file[-4:] in ['.otf', '.ttf']}

    # copy the font files to ~/.fonts
    for key in font_files.keys():
        targe_path = os.path.join(font_directory, key)
        source_path = os.path.join(font_files[key], key)

        directory_paths.append(font_files[key])

        try:
            shutil.copy(source_path, targe_path)
        except PermissionError as pe:
            print('PermissionError - {} - {}'.format(pe, targe_path))
        except FileNotFoundError as fne:
            print('FileNotFoundError - {} - {}'.format(fne, targe_path))
        else:
            os.remove(source_path)
            print('source_path --- ', source_path)

print()
paths = list(set(directory_paths))
paths.remove(download_dir_path)
for path in paths:
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(e)

print()
# refresh the font cash
os.system('sudo fc-cache -f -v')
