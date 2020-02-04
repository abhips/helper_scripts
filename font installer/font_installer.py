""" -----------------------------------------------------------------------------

    MIT License

    Copyright (c) 2020 Abhilash PS

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

    ----------------------------------------------------------------------------

    :copyright: Abhilash PS
    :month-year: 02-2020

    ----------------------------------------------------------------------------
"""

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
