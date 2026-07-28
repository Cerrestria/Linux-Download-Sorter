from pathlib import Path 
import shutil

'''
@author: Cerrestria (https://github.com/Cerrestria)
@version: 1.2
'''

def getFileEndings(files):
    extensions = set()
    for file in files:
        suf = file.suffix.lower()
        if suf:
            extensions.add(suf)
    return  list(extensions)

def createFolders(extensionList, directory):
    folders = []
    for extension in extensionList:
        name = (extension)[1:]
        (directory / name).mkdir(exist_ok=True)
        folders.append(f'{name}')
    return folders

def sortFile(folders, fileName, filePath, directory):
    if not fileName.suffix:
        (directory / 'misc').mkdir(exist_ok = True)
        shutil.move(filePath, directory / 'misc' / fileName)
    for folder in folders:
        folderPath = directory / folder
        # 6. does file ending matches folder name?
        if fileName.suffix.lower() == f'.{folder}':
            # 7. does a file with this name already exist in the folder?
            if (folderPath / fileName).exists():
                c = 1
                # appends filename with '_{c}' and moves into folder
                while True:
                    newName = f'{fileName.stem}_{c}{fileName.suffix}'
                    if (folderPath / newName).exists():
                        c += 1
                    else:
                        shutil.move(filePath, folderPath / newName )
                        return True
            # if not, then move into folder 
            else:
                shutil.move(filePath, folderPath / fileName)
                return True
    return False

def main():
    # 1. get user Downloads folder
    directory = Path.home() / 'Downloads'

    # 2. gets all files
    files = [f for f in directory.iterdir() if f.is_file() and not f.name.startswith('.')]

    # 3. gets all file endings and collects them in a list
    extensionList = getFileEndings(files)
    # sorts list
    if not extensionList:
        print('Nothing to sort!')
    else:
        extensionList.sort()
    
    # 4. creates folders for each file ending found
    folders = createFolders(extensionList, directory)
    
    # 5. grabs a file and iterates through all folders until ending fits the folder name and moves file into it
    moved = 0
    for file in files:
        if sortFile(folders, Path(file.name), file, directory):
            moved += 1
    if moved > 0:
        print(f'Sorted {moved} items into {len(folders)} folders!') 
    return


if __name__ == '__main__':
    main()