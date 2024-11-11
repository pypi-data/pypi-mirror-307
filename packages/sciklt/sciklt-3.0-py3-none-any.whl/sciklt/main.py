import os
import shutil
import subprocess


available = {'-1  ' : "NLP(Folder)"}

def get(name = None, open = False):
    try:
        if name is not None:
            name = str(name)
        if name in ['-1']     :   get_folder(loc = True)
        else:
            for k, v in available.items():
                sep = " : " if v else ""
                print(k,v,sep = sep)
    except:
        pass

def get_folder(loc = False, i = 0, j = 0):
    src = os.path.realpath(__file__)[:-7]+"\\data\\NLP"
    src = src.replace("\\\\","\\")
    try:
        dest = os.getcwd()+"\\NLP"+(f" ({i})" if i != 0 else "")
        shutil.copytree(src, dest, symlinks=False,
                        copy_function = shutil.copy2,
                        ignore=shutil.ignore_patterns('.ipynb_checkpoints', '__init__.py', '__pycache__'),
                        ignore_dangling_symlinks=False, 
                        dirs_exist_ok=False)
        if loc:
            print("Path:",dest.replace("\\\\","\\"))
    except FileExistsError:
        get_folder(loc, i + 1, j)
    except:
        try:
            dest = os.path.expanduser('~')+"\\Downloads\\NLP"+(f" ({j})" if j != 0 else "")
            shutil.copytree(src, dest, symlinks=False,
                            copy_function = shutil.copy2,
                            ignore=shutil.ignore_patterns('.ipynb_checkpoints', '__init__.py', '__pycache__'),
                            ignore_dangling_symlinks=False, 
                            dirs_exist_ok=False)
            if loc:
                print("Path:",dest.replace("\\\\","\\"))
        except FileExistsError:
            get_folder(loc, i, j + 1)
        except:
            pass