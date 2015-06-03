#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'mac'


import os
import re
import copy

class EDL(object):

    def __init__(self):
        self._edlclip = []
        self._fps = 24.0
        self._currentclip = {'index': '',
                               'reel': '',
                               'type': '',
                               'cut': '',
                               'sourcein': '',
                               'sourceout': '',
                               'targetin': '',
                               'targetout': '',
                               'clipname': '',
                               'dissolveduration': '',
                               'longreel': '',
                               'speed': '',
                             'duration':''}

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


    def __resetcurrentclip(self):
        self._currentclip['index'] = ''
        self._currentclip['reel'] = ''
        self._currentclip['type'] = ''
        self._currentclip['cut'] = ''
        self._currentclip['sourcein'] = ''
        self._currentclip['sourceout'] = ''
        self._currentclip['targetin'] = ''
        self._currentclip['targetout'] = ''
        self._currentclip['clipname'] = ''
        self._currentclip['dissolveduration'] = ''
        self._currentclip['longreel'] = ''
        self._currentclip['speed'] = ''
        self._currentclip['duration'] = ''


    def edllist(self):
        for index, item in enumerate(self._edlclip):
            print(index, item)

    def __recalculateduration(self, index):
        if self._edlclip[index]['sourcein'] == self._edlclip[index]['sourceout']:
            self._edlclip[index]['sourceout'] = self.__timecodeadd(self._edlclip[index]['sourcein'],
                                                                   '00:00:00:01',
                                                                   self._fps)
        self._edlclip[index]['duration'] = self.__timecodetoframe(self._edlclip[index]['sourceout'], self._fps) - \
                                        self.__timecodetoframe(self._edlclip[index]['sourcein'], self._fps)


    def readedl(self, edlpath):
        with open(edlpath, 'r') as edlfile:
            edllines = edlfile.readlines()

        tcregex = re.compile(r'[0-9]{2}:[0-9]{2}:[0-9]{2}:[0-9]{2}')
        moreinforegex = re.compile(r'^\*')
        speedregex = re.compile(r'^M2')

        for index, line in enumerate(edllines):
            # print(index, line)
            tcmatch = tcregex.findall(line)
            # print(tcmatch)

            if len(tcmatch) == 4:
                linecomponent = line.split()
                if linecomponent[3] == 'C':
                    self._currentclip['index'] = linecomponent[0]
                    self._currentclip['reel'] = linecomponent[1]
                    self._currentclip['type'] = linecomponent[2]
                    self._currentclip['cut'] = linecomponent[3]
                    self._currentclip['sourcein'] = linecomponent[4]
                    self._currentclip['sourceout'] = linecomponent[5]
                    self._currentclip['targetin'] = linecomponent[6]
                    self._currentclip['targetout'] = linecomponent[7]

                    self._edlclip.append(copy.deepcopy(self._currentclip))
                    self.__recalculateduration(-1)
                    self.__resetcurrentclip()
                    continue

                if linecomponent[3] == 'D':
                    self._currentclip['index'] = linecomponent[0]
                    self._currentclip['reel'] = linecomponent[1]
                    self._currentclip['type'] = linecomponent[2]
                    self._currentclip['cut'] = linecomponent[3]
                    self._currentclip['dissolveduration'] = linecomponent[4]
                    self._currentclip['sourcein'] = linecomponent[5]
                    self._currentclip['sourceout'] = linecomponent[6]
                    self._currentclip['targetin'] = linecomponent[7]
                    self._currentclip['targetout'] = linecomponent[8]


                    self._edlclip[-1]['sourceout'] = self.__timecodeadd(self._edlclip[-1]['sourceout'],
                                                                        self.__frametotimecode(int(linecomponent[4]), self._fps),
                                                                        self._fps)


                    self._edlclip.append(copy.deepcopy(self._currentclip))
                    self.__recalculateduration(-1)
                    self.__recalculateduration(-2)
                    self.__resetcurrentclip()
                    continue


            if moreinforegex.match(line) is not None:
                if 'EFFECT NAME' in line:
                    continue

                if 'FROM CLIP NAME' in line:
                    clipname = line.split(':')[-1].lstrip().rstrip()
                    if self._edlclip[-1]['cut'] == 'C':
                        self._edlclip[-1]['clipname'] = clipname
                    else:
                        self._edlclip[-2]['clipname'] = clipname
                    continue

                if 'COMMENT' in line:
                    continue

                if 'TO CLIP NAME' in line:
                    clipname = line.split(':')[-1].lstrip().rstrip()
                    if self._edlclip[-1]['cut'] == 'D':
                        self._edlclip[-1]['clipname'] = clipname
                    continue


            if 'FINAL CUT PRO REEL' in line:
                finalreels = line.replace('FINAL CUT PRO REEL:', ' ').replace('REPLACED BY:', ' ').lstrip().rstrip().split()
                if len(finalreels) == 2:
                    if self._edlclip[-1]['cut'] == 'D':
                        if self._edlclip[-2]['reel'] == finalreels[1]:
                            self._edlclip[-2]['longreel'] = finalreels[0]
                        if self._edlclip[-1]['reel'] == finalreels[1]:
                            self._edlclip[-1]['longreel'] = finalreels[0]
                            continue
                    else:
                        if self._edlclip[-1]['reel'] == finalreels[1]:
                            self._edlclip[-1]['longreel'] = finalreels[0]

                continue


            if speedregex.match(line) is not None:
                speedcomponent = line.lstrip().rstrip().split()
                # print(speedcomponent)
                if len(speedcomponent) == 4:
                    if self._edlclip[-1]['cut'] == 'D':
                        if self._edlclip[-2]['reel'] == speedcomponent[1] and self._edlclip[-2]['speed'] == '':
                            self._edlclip[-2]['speed'] = speedcomponent[2]

                            framein = self.__timecodetoframe(self._edlclip[-2]['sourcein'], self._fps)
                            frameout = self.__timecodetoframe(self._edlclip[-2]['sourceout'], self._fps)
                            duration = round((frameout - framein)/self._fps* float(speedcomponent[2]))
                            self._edlclip[-2]['sourceout'] = self.__timecodeadd(self._edlclip[-2]['sourcein'],
                                                                                self.__frametotimecode(duration, self._fps),
                                                                                self._fps)
                            self.__recalculateduration(-2)

                            continue

                        if self._edlclip[-1]['reel'] == speedcomponent[1] and self._edlclip[-1]['speed'] == '':
                            self._edlclip[-1]['speed'] = speedcomponent[2]

                            framein = self.__timecodetoframe(self._edlclip[-1]['sourcein'], self._fps)
                            frameout = self.__timecodetoframe(self._edlclip[-1]['sourceout'], self._fps)
                            duration = round((frameout - framein) / self._fps * float(speedcomponent[2]))
                            self._edlclip[-1]['sourceout'] = self.__timecodeadd(self._edlclip[-1]['sourcein'],
                                                                                self.__frametotimecode(duration,
                                                                                                       self._fps),
                                                                                self._fps)
                            self.__recalculateduration(-1)

                    else:
                        if self._edlclip[-1]['reel'] == speedcomponent[1] and self._edlclip[-1]['speed'] == '':
                            self._edlclip[-1]['speed'] = speedcomponent[2]

                            framein = self.__timecodetoframe(self._edlclip[-1]['sourcein'], self._fps)
                            frameout = self.__timecodetoframe(self._edlclip[-1]['sourceout'], self._fps)
                            duration = round((frameout - framein) / self._fps * float(speedcomponent[2]))
                            self._edlclip[-1]['sourceout'] = self.__timecodeadd(self._edlclip[-1]['sourcein'],
                                                                                self.__frametotimecode(duration,
                                                                                                       self._fps),
                                                                                self._fps)
                            self.__recalculateduration(-1)



if __name__ == '__main__':
    testclass = EDL()
    testclass.readedl('/Users/andyguo/Desktop/Sequence 1.edl')
    testclass.edllist()