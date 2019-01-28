import sys
import getopt
import os
import numpy as np
sys.path.append("modules")
import idx

def main(argv):
    in_path = ''
    out_path = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",[])
    except getopt.GetoptError:
        print('packer.py -i <inputpath> -o <outputpath>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('packer.py -i <inputpath> -o <outputpath>')
            sys.exit()
        elif opt in ("-i"):
            in_path = arg
        elif opt in ("-o"):
            out_path = arg


    out_lbl = idx.file(dtype=">u1", datashape=[])
    out_img = idx.file(dtype=">u1", datashape=[28, 28])

    for file_lbl in os.listdir(in_path):
        if file_lbl.endswith(".idx1-ubyte"):
            path_lbl = os.path.join(in_path, file_lbl)
            path_img = os.path.splitext(path_lbl)[0] + ".idx3-ubyte"
            out_lbl.append(idx.read(path_lbl).body)
            out_img.append(idx.read(path_img).body)
    
    idx.write(os.path.join(out_path, "lbl.idx1-ubyte"), out_lbl)
    idx.write(os.path.join(out_path, "img.idx3-ubyte"), out_img)

    saved =idx.read(os.path.join(out_path, "img.idx3-ubyte")).body
    print(saved.shape)
if __name__ == "__main__":
   main(sys.argv[1:])