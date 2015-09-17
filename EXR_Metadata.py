#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'mac'

import os
import logging
import collections
import subprocess
import re


class EXR_Metadata(object):
    def __init__(self):
        super(EXR_Metadata, self).__init__()
        self.header = collections.OrderedDict()


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

    def metadata(self, path):
        if not os.path.exists(r'/opt/local/bin/exrheader'):
            logging.error('please install openexr lib')
            return None

        cmd = '/opt/local/bin/exrheader ' + path
        message = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
        key = ''
        value = ''
        rere = re.compile(r'\(.*?\)')
        retype = re.compile(r'.*\(type\ (.*?)\)')

        if len(message) > 0:
            self.header['FULL_PATH'] = path
            for index, line in enumerate(message.splitlines()):
                if len(line) > 0:
                    if line.endswith(':'):
                        key = rere.sub('', line).strip(':').strip()
                        self.header[key] = ''
                    else:
                        if line.startswith('    '):
                            if key == 'timeCode':
                                if 'time' in line:
                                    self.header[key] = line.strip().split(' ')[-1]
                                    myfps = 24.0
                                    if self.header.has_key('framesPerSecond'):
                                        myfps = float(self.header['framesPerSecond'])
                                    self.header['endTimeCode'] = self.__timecodeadd(self.header[key], '00:00:00:01',
                                                                                    myfps)
                                    self.header['frameCount'] = self.__timecodetoframe(self.header[key], myfps)
                            else:
                                self.header[key] += line.replace(',', ' ')

                        else:
                            # print(index, line)
                            key, value = line.split(': ')
                            mytype = ''
                            if retype.match(key):
                                mytype = retype.search(key).groups()[-1]

                            key = rere.sub('', key).strip()

                            if mytype == 'rational':
                                value = '%.02f' % (float(value.split(' ')[0].split(r'/')[0]) / float(
                                    value.split(' ')[0].split('/')[1]))
                            else:
                                value = value.strip().strip(r'"').replace(',', ' ')
                            self.header[key] = value

        return self.header

    def csvString(self, sep=','):
        csvstring = ''
        csvstring = sep.join(self.header.keys())
        csvstring += os.linesep
        csvstring += sep.join(map(str, self.header.values()))
        csvstring += os.linesep

        if len(csvstring) > 0:
            return csvstring
        else:
            return None


if __name__ == '__main__':
    testclass = EXR_Metadata()
    meta = testclass.metadata(
        '/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW/To_VFX/20150915/TST0010/1_B027C024_150201_R6QX/2048x1152/TST_1001.exr')
    print(meta)
    print(testclass.csvString())
