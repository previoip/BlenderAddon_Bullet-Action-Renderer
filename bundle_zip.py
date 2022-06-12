# a straight forward script that bundles into zip for blender addon intall
from fileinput import filename
from importlib.metadata import metadata
from zipfile import ZipFile
import re, os


folder_excludes = [
    '.git',
    '.gitignore',
    '.gitattributes',
    '__pycache__',
    'Blendfiles',
    'rel',
    'Export',
    'bundle_zip.py'
]

file_excludes = [
    '.git',
    '.gitattributes',
    '.gitignore',
    'bundle_zip.py'
]

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        dirs[:] = [i for i in dirs if i not in folder_excludes]
        ziph.write(root)
        for filename in files:
            if filename not in file_excludes:
                ziph.write(os.path.join(root, filename))

dist = 'rel'

# lmfao
with open('__init__.py', 'r') as fp:
    metadata = fp.read()
pattern = r'(\{(?:\[??[^\[]*?\}))'
metadata = re.findall(pattern, metadata)[0].split('\n')[1:-1]
metadata = [i.strip().split(':') for i in metadata]
metadata = [[j.strip() for j in i] for i in metadata]
metadata = [[j.replace('\'', '') for j in i] for i in metadata]
metadata = [[j.replace('\'', '') for j in i] for i in metadata]
metadata = [[j if j[-1] != ',' else j[:-1] for j in i] for i in metadata]
metadata = dict(metadata)

if 'version' in metadata:
    metadata['version'] = metadata['version'][1:-1].split(',')
    metadata['version'] = tuple(int(i) for i in metadata['version'])

if 'blender' in metadata:
    metadata['blender'] = metadata['blender'][1:-1].split(',')
    metadata['blender'] = tuple(int(i) for i in metadata['blender'])


if __name__ == '__main__':
    if not os.path.exists(dist):
        os.mkdir(dist)

    fn = 'addon'
    support = ''
    version = ''
    bl_version = ''
    ext = '.zip'

    if 'version' in metadata:
        version = '-'.join([str(i) for i in metadata['version']])
        version = '_v' + version

    if 'blender' in metadata:
        bl_version = '-'.join([str(i) for i in metadata['blender']])
        bl_version = '_Blender' + bl_version

    if 'support' in metadata:
        support = '_' + metadata['support'].lower()

    filename = f'{fn}{bl_version}{version}{support}{ext}'
    path_to_zip = os.path.join(dist, filename)

    path_to_files = []

    with ZipFile(path_to_zip, 'w') as ZipObj:
        zipdir('.', ZipObj)