
import struct
import imghdr
import os
import shutil

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return 0, 0
        else:
            return 0, 0
        return width, height



folder=os.path.dirname(os.path.realpath(__file__))

        
for this_file in os.listdir(folder):
    if os.path.isfile(this_file):
        filename, file_extension = os.path.splitext(this_file)
        print(filename)
        file_path = os.path.join(folder, this_file)
        width, height = get_image_size(file_path)
        print(width)
        if file_extension == ".jpg" and (width < height or width == 0 or width == 272):
            os.remove(file_path)
    