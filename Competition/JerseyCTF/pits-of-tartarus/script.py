import tarfile
import os

patch = "/mnt/c/Users/C4t_f4t/Desktop/CTF-WriteUp/Competition/JerseyCTF/pits-of-tartarus"
folder = ''
count = 0

while True:
    pathnew = os.path.join(patch, folder)
    for tar_file in os.listdir(pathnew):
        if tar_file != 'unzip.py':
            try:
                if tar_file.endswith('.tar.gz'):
                    print('Extracting file:', tar_file)
                    with tarfile.open(os.path.join(pathnew, tar_file), 'r:gz') as archive:
                        folder = 'unzip' + str(count)
                        archive.extractall(folder)
                    count += 1
                else:
                    print(f'Skipping file: {tar_file} is not a gzip-compressed tarball')
            except tarfile.TarError:
                print(f'Error: {tar_file} is not a valid tar file')
                raise
            except FileNotFoundError:
                print(f'Error: {tar_file} not found')
                raise
