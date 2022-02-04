from os.path import isdir, join, splitext, getsize
from os import remove, listdir
import sys

filetypes = ['.tmp', '.log', '.obj', '.txt']


def delCertainFiles (directory):
    if not isdir(directory):
        return
    for filename in listdir(directory):
        temp = join(directory, filename)
        if isdir(temp):
            delCertainFiles(temp)
        elif splitext(temp)[1] in filetypes or getsize(temp) == 0:
            remove(temp)
            print(temp, 'deleted...')


directory = sys.argv[0]
delCertainFiles(directory)


