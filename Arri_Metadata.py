#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import struct


class Arri_Metadata(object):

    def __init__(self):
        super(Arri_Metadata, self).__init__()


    def metadata(self, path):
        with open(path, 'rb') as file:
            file.seek(0)
            self.header = struct.unpack('<4s 3I'       #  RootInformation
                                        'I I I I I 4I 4I I I 8s'       # ImageDataInformation
                                        'I I I 4f I I I I 12f f f I I I f I 32s I I I I f 3f 3f 3f 3f I I I I 32s' # ImageContentInformation
                                        'I I I I I 4s 4s 2I 2I I I I I I I I '
                                        '50I 12s'
                                        '32s 8s 32s I I I 16s 24s 20s H H 96s'      # CameraDeviceInformation
                                        'I I I I I I 2H I I I 32s 2H 2H 2H 2H 2H 2H 2H 2H 2H '
                                        'B B B B 88s'   # LensDataInformation
                                        'I 2I 2I I I I I I I I I I 128s'    # VfxInformation
                                        'I I 8s 16s 8s 32s 32s 32s 32s 256s 24s 104s'   # ClipInformation
                                        'I 4I 32s 32s 32s 32s 32s I I 32s'  # SoundInformation
                                        'I I I I I I I I I I I 40s'     # CameraInformation
                                        'I I 32s 32s '
                                        'I 32s H H H H H H '
                                        'I 32s H H H H H H '
                                        'I 32s H H H H H H '
                                        'I 32s H H H H H H '
                                        'I 32s H H H H H H '
                                        'I 32s H H H H H H '
                                        '32s'       # FramelineInformation
                                        'I 512s 1068s'      # ARRIReserved
                                        , file.read(4096))




if __name__ == '__main__':
    testmetadata = Arri_Metadata()
    testmetadata.metadata('/Volumes/work/TEST_Footage/~Footage/Alexa-Day/00100000147.0000025.ari')
    print(testmetadata.header)
