#!/usr/bin/env python
# -*- encoding: utf-8 -*-
__author__ = 'mac'

import os
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom as MINIDOM
import xlrd
import subprocess
import copy
import struct


class IOFTRACK(object):
    def __init__(self):
        self._cliplist = []
        self._rawcliplist = []
        self._startframe = -10
        self._endframe = -10
        self._lastfilename = ''
        self._shotlist = []
        self._vfxcliplist = []
        self._shouldrenamefolder = False
        self._subfilelist = []

    def __timecodetoframe(self, timecode, fps):
        # print('==== __timecodetoframe  ====')
        ffps = float(fps)
        hh = int(timecode[0:2])
        mm = int(timecode[3:5])
        ss = int(timecode[6:8])
        ff = 0
        if timecode[8:9] == '.':
            ff = int(float(timecode[9:11]) / 100.0 * ffps)
        else:
            ff = int(timecode[9:11])
        # print(ffps, hh, mm, ss, ff)
        framecount = int((hh * 3600 * ffps) + int(mm * 60 * ffps) + int(ss * ffps) + ff)
        # print(framecount)
        return framecount

    def __frametotimecode(self, frame, fps):
        # print('==== __frametotimecode  ====')
        ffps = float(fps)
        fframe = int(frame)
        hh = fframe // int(3600 * ffps)
        fframe = fframe - int(hh * 3600 * ffps)
        mm = fframe // int(60 * ffps)
        fframe = fframe - int(mm * 60 * ffps)
        ss = fframe // ffps
        ff = fframe - ss * ffps
        tcstring = '%02d:%02d:%02d:%02d' % (hh, mm, ss, ff)
        # print(tcstring)
        return tcstring

    def __timecodeadd(self, tc1, tc2, fps):
        # print('==== __timecodeadd  ====')
        frame1 = self.__timecodetoframe(tc1, fps)
        frame2 = self.__timecodetoframe(tc2, fps)
        # print(frame1, frame2)
        frame2 = frame1 + frame2
        return self.__frametotimecode(frame2, fps)

    def _processexrmessage(self, filepath):
        cmd = ['exrheader {0}'.format(filepath)]
        exrmessage = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
        exrmetadata = {'MASTER_TC': '00:00:00:00', 'REEL': '--', 'fps': '24', 'filepath': filepath}
        for line in exrmessage.split(os.linesep):
            if 'time' in line and '(' not in line:
                # print(line)
                exrmetadata['MASTER_TC'] = line.split('time')[-1].lstrip().rstrip()
            if 'framesPerSecond' in line:
                # print(line)
                exrmetadata['fps'] = line.split(': ')[-1].split('(')[-1].rstrip(')')

        # print(exrmetadata)
        return exrmetadata

    def _processdpxmessage(self, filepath):
        dpxheader = ()
        with open(filepath, 'rb') as dpxfile:
            if struct.unpack('4s', dpxfile.read(4)) == 'SDPX':
                dpxfile.seek(0)
                dpxheader = struct.unpack(
                    '<4s I 8s I I I I I 100s 24s 100s 200s 200s I 104s'  # 764 bytes [0:14]
                    'H H I I 576s 52s'  # 1404 bytes[15:20]
                    'I I f f I I 100s 24s 32s 32s 4h 2i 28s'  # 1660 bytes[21:37]
                    '2s 2s 2s 6s 4s 32s I i i f f 32s 100s 56s'  # 1916 bytes[38:51]
                    '4b 4b 4b f f f f f f f f f f 76s'  # 2044 bytes[47:66]
                    '32s',  # 2076 bytes[67]
                    dpxfile.read(2080))
            else:
                dpxfile.seek(0)
                dpxheader = struct.unpack(
                    '>4s I 8s I I I I I 100s 24s 100s 200s 200s I 104s'  # 768 bytes [0:14]
                    'H H I I 576s 52s'  # 1408 bytes[15:20]
                    'I I f f I I 100s 24s 32s 32s 4h 2i 28s'  # 1664 bytes[21:37]
                    '2s 2s 2s 6s 4s 32s I i i f f 32s 100s 56s'  # 1920 bytes[38:51]
                    '4b 4b 4b f f f f f f f f f f 76s'  # 2048 bytes[47:66]
                    '32s',  # 2080 bytes[67]
                    dpxfile.read(2080))

                # for sss, kkk in enumerate(dpxheader):
                # print(sss, kkk)
        tc = ('%02x' % dpxheader[52]) + ':' + ('%02x' % dpxheader[53]) + ':' + (
            '%02x' % dpxheader[54]) + ':' + ('%02x' % dpxheader[55])
        if dpxheader[52] > 23 or dpxheader[52] < 0:
            tc = '00:00:00:00'
        # print(tc)

        fps = '%.2f' % dpxheader[47]
        if float(fps) <= 0:
            fps = '24'

        reel = re.sub(r'\W', '', dpxheader[29])
        if (len(reel)) == 0:
            reel = '--'

        dpxmetadata = {'MASTER_TC': tc, 'REEL': reel, 'fps': fps, 'filepath': filepath}
        return dpxmetadata

    def _getmetadata(self, filepath):
        # print('==== enter _getmetadata  ====')
        if os.path.splitext(filepath)[-1].lower() == '.exr':
            metadata = self._processexrmessage(filepath)
        if os.path.splitext(filepath)[-1].lower() == '.dpx':
            metadata = self._processdpxmessage(filepath)

        return metadata

    def scantranscodefiles(self, scanpath):
        print('enter scantranscodefiles method')
        self._cliplist = []
        digitregex = re.compile(r'(\d{3,})')
        checkregex = re.compile(r'.*(\d{3,}).*')
        emptyregex = re.compile(r'^\.')
        self._startframe = -10
        self._endframe = -10
        self._lastfilename = ''
        self._subfilelist = []

        for root, subfolder, files in os.walk(scanpath):
            # self._startframe = -10
            # self._endframe = -10
            files = [x for x in files if os.path.splitext(x)[-1].lower() in ['.dpx', '.exr']]
            files.sort()
            self._lastfilename = ''
            self._startframe = -10
            self._endframe = -10
            self._subfilelist = []
            # print(files)

            for index, file in enumerate(files):
                if checkregex.match(file) is None:
                    # print('a name file')
                    continue

                else:
                    m = list(digitregex.finditer(file))[-1]
                    if self._startframe == -10:
                        print('first start file')
                        self._subfilelist = []
                        self._startframe = int(m.group(0))
                        self._endframe = self._startframe
                        self._subfilelist.append(self._getmetadata(os.path.join(root, file)))

                    elif int(m.group(0)) == self._endframe + 1:
                        print('continual files')
                        self._endframe = int(m.group(0))
                        self._subfilelist.append(self._getmetadata(os.path.join(root, file)))

                    else:
                        print('interrupt file')
                        singleclip = {
                            'startframe': self._startframe,
                            'endframe': self._endframe,
                            'metadata': copy.deepcopy(self._subfilelist),
                            'sequence': [],
                            'shot': [],
                            's3d': ''}
                        # print(singleclip)
                        self._startframe = int(m.group(0))
                        self._endframe = self._startframe
                        self._cliplist.append(singleclip)

            if len(self._subfilelist) > 0:
                singleclip = {
                    'startframe': self._startframe,
                    'endframe': self._endframe,
                    'metadata': copy.deepcopy(self._subfilelist),
                    'sequence': [],
                    'shot': [],
                    's3d': ''}
                self._cliplist.append(singleclip)

        for index, item in enumerate(self._cliplist):
            print(index, item)

        print('exit scantranscodefiles method')


if __name__ == '__main__':
    testclass = IOFTRACK()
    testclass.scantranscodefiles(r'/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW/PIPELINE_TEST_20150416/Deliverable')
