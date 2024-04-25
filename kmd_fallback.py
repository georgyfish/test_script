# import get_commit
import os,sys,time
from get_deb_version import get_deb_version
import subprocess
import get_commit
import middle_search


def main():
    kmd_right = middle_search('gr-kmd',kmd_list)
    if kmd_right == -1 :
        print('更换kmd无法确认引入；')
        sys.exit(-1)
    else:
        print(f'问题引入为{kmd_list[right]}')