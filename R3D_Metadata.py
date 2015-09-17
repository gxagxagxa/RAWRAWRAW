#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'mac'

import os
import logging
import collections
import subprocess

logging.basicConfig(level=logging.WARN,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')


class R3D_Metadata(object):
    def __init__(self):
        super(R3D_Metadata, self).__init__()
        self.header = collections.OrderedDict()

    def metadata(self, path, showallframe=False):
        if not os.path.exists(r'/usr/sbin/REDline'):
            logging.error('please install RedCine X Pro')
            return None

        cmd = '/usr/sbin/REDline' + ' --i ' + path + ' --printMeta 3'
        message = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
        # print(message)
        if len(message) > 0:
            keys = message.splitlines()[1].split(',')
            values = message.splitlines()[2].split(',')
            logging.info(keys)
            logging.info(values)

            for index, key in enumerate(keys):
                self.header[key] = values[index]

            if showallframe:
                cmd = '/usr/sbin/REDline' + ' --i ' + path + ' --printMeta 5'
                message = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
                if len(message) > 0:
                    keys = message.splitlines()[1].split(',')
                    values = message.splitlines()[2:]
                    logging.info(keys)
                    logging.info(values)

                    for index, key in enumerate(keys):
                        self.header[key] = []

                    for i in xrange(len(values)):
                        for index, key in enumerate(keys):
                            self.header[key].append(values[i].split(',')[index])
            else:
                self.header['FrameNo'] = ''

            return self.header
        else:
            return None

    def csvString(self, sep=','):
        csvString = ''
        if len(self.header['FrameNo']) > 0:
            csvString = sep.join(self.header.keys()) + os.linesep
            for index in xrange(len(self.header['FrameNo'])):
                templist = []
                for attindex, key in enumerate(self.header.keys()):
                    # print(attindex, key, self.header[key])
                    if key in ('FrameNo', 'Timecode', 'Aperture', 'Focal Length',
                               'Focus Distance', 'Acceleration X', 'Acceleration Y', 'Acceleration Z',
                               'Rotation X', 'Rotation Y', 'Rotation Z'):
                        templist.append(self.header[key][index])
                        # print(self.header[key][index])
                        # print(attindex, key, self.header[key][index])

                    else:
                        templist.append(self.header[key])
                # print(templist)
                csvString += sep.join(templist)
                csvString += os.linesep

        else:
            csvString = sep.join(self.header.keys()) + os.linesep
            csvString += sep.join(self.header.values()) + os.linesep

        logging.info(csvString)
        if len(csvString) > 0:
            return csvString
        else:
            return None


if __name__ == '__main__':
    testclass = R3D_Metadata()
    meta = testclass.metadata(
        '/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW/Conform/BL/E131_C011_0616PD.RDC/E131_C011_0616PD_001.R3D',
        showallframe=True)
    testclass.csvString()
    # print(meta)
