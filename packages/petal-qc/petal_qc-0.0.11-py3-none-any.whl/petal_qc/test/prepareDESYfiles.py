#!/usr/bin/env python3
"""Prepare raw data input files from DESY so that we can use them with this code."""
import os
import fnmatch
import re
from pathlib import Path
import argparse

def all_files(root, patterns='*', single_level=False, yield_folders=False):
    """A generator that reruns all files in the given folder.

    Args:
    ----
        root (file path): The folder
        patterns (str, optional): The pattern of the files. Defaults to '*'.
        single_level (bool, optional): If true, do not go into sub folders. Defaults to False.
        yield_folders (bool, optional): If True, return folders as well. Defaults to False.

    Yields
    ------
        str: file path name

    """
    patterns = patterns.split(';')
    for path, subdirs, files in os.walk(root):
        if yield_folders:
            files.extend(subdirs)

        files.sort()
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    yield os.path.join(path, name)
                    break

        if single_level:
            break

class PetalCore:
    def __init__(self, front, back):
        self.front = {}
        self.back = {}

def main(folder, out_folder):
    """Main entry point.

    It takes DESY raw data files and combines them into  a single file for front
    and back metrology.

    Args:
        folder: the input folder where to find the original files.
        out_folder: the folder where the new fiels will be stored.
    """
    outF = Path(out_folder).expanduser().resolve()
    if not outF.exists():
        os.mkdir(outF)

    rgx = re.compile(r"Project Name: (\w+)side_.*AlternativeID=PPC[-_](\d+)", re.MULTILINE|re.DOTALL)
    petal_cores = {}
    for fnam in all_files(folder, "*.txt"):
        P = Path(fnam).expanduser().resolve()
        with open(fnam, "r", encoding="UTF-8") as ff:
            R = rgx.search(ff.read())
            if R: 
                petal_id = "PPC.{}".format(R.group(2))
                side = R.group(1).lower()
                if "_2D_" in P.name:
                    test_type = "2D"
                else:
                    test_type = "3D"

                if not petal_id in petal_cores:
                    petal_cores[petal_id] = {
                                             "back":{"2D":None, "3D":None},
                                             "front":{"2D":None, "3D":None},
                                             }

                petal_cores[petal_id][side][test_type] = P

    list_file = open("{}/Desy-cores.txt".format(outF.as_posix()), "w", encoding="UTF-8")
    for petal_id, sides in petal_cores.items():
        for side, values in sides.items():
            oname = "{}/{}-{}.txt".format(outF.as_posix(), petal_id, side)
            list_file.write("{} {}-{} {}\n".format(oname, petal_id, side, petal_id))
            data = ""
            for data_type, fnam in values.items():
                if fnam is None:
                    print("This should not happen.")
                    
                with open(fnam, "r", encoding="UTF-8") as ifile:
                    data += ifile.read()

            with open(oname, "w", encoding="UTF-8") as ofile:
                ofile.write(data)

    list_file.close()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-folder", default=None, help="Input folder")
    parser.add_argument("--output-folder", help="Outout fodler", default=None)
    
    main("/Users/lacasta/Downloads/Report_QC-desy_Sep2024", "/tmp/desy")