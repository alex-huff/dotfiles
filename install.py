import os
import sys
from pathlib import Path

def recurseThroughFiles(path='.'):
    for dirEntry in os.scandir(path):
        installPath = os.path.join(targetPath, dirEntry.path)
        if dirEntry.is_dir():
            if not os.path.exists(installPath):
                os.makedirs(installPath)
            recurseThroughFiles(dirEntry.path)
            continue
        absoluteSourcePath = os.path.abspath(dirEntry.path)
        if not linksToFile(installPath, absoluteSourcePath): # if link not already made
            try:
                os.lstat(installPath) # check if path exists (even for broken symlinks)
                backupFile(installPath, dirEntry.path) # backup present path
            except FileNotFoundError:
                pass
            os.symlink(absoluteSourcePath, installPath)
            print(f'Linked {installPath} -> {absoluteSourcePath}.')
        
def backupFile(targetPath, relativePath):
    backupPath = os.path.join(backupDirectory, relativePath)
    backupPathDirectory = os.path.dirname(backupPath)
    if not os.path.exists(backupPathDirectory):
        os.makedirs(backupPathDirectory)
    os.replace(targetPath, backupPath)
    print(f'Backed up {targetPath} to {backupPath}.')

def linksToFile(linkFile, sourceFile):
    return os.path.islink(linkFile) and os.readlink(linkFile) == sourceFile

if len(sys.argv) != 2:
    print('Usage: python install.py (path to install to).')
    sys.exit(1)
targetPath = os.path.abspath(sys.argv[1])
# make sure that current working directory is in folder containing script
scriptParentDirectory = os.path.abspath(os.path.dirname(__file__))
dotfilesDirectory = os.path.join(scriptParentDirectory, 'dotfiles')
backupDirectory = os.path.join(scriptParentDirectory, 'backup')
os.chdir(dotfilesDirectory)
recurseThroughFiles()