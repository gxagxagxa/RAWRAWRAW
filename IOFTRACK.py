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
import sqlite3


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
                        # print('first start file')
                        self._subfilelist = []
                        self._startframe = int(m.group(0))
                        self._endframe = self._startframe
                        self._subfilelist.append(self._getmetadata(os.path.join(root, file)))

                    elif int(m.group(0)) == self._endframe + 1:
                        # print('continual files')
                        self._endframe = int(m.group(0))
                        self._subfilelist.append(self._getmetadata(os.path.join(root, file)))

                    else:
                        # print('interrupt file')
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

        # for index, item in enumerate(self._cliplist):
        #     print(index, item)

        for clip in self._cliplist:
            if 'l' in clip['metadata'][0]['filepath'].split(os.sep)[-2].lower():
                clip['s3d'] = 'l'
            elif 'r' in clip['metadata'][0]['filepath'].split(os.sep)[-2].lower():
                clip['s3d'] = 'r'
            else:
                clip['s3d'] = 'main'

        print('exit scantranscodefiles method')

    def conformdb(self, dbpath):
        connect = sqlite3.connect(dbpath)

        try:
            cursor = connect.cursor()
            for index, item in enumerate(self._cliplist):
                for singlefile in item['metadata']:
                    cmd = 'SELECT * FROM RAWMETADATA ' \
                          'WHERE Camera_Clip_Name LIKE \"%s\"' \
                          'AND MASTER_TC <= \"%s\"' \
                          'AND END_TC >= \"%s\"' % (os.path.basename(singlefile['filepath']).split('.')[0] + '%',
                                                    singlefile['MASTER_TC'], singlefile['MASTER_TC'])
                    cursor.execute(cmd)
                    values = cursor.fetchall()
                    # print(values[0])
                    if values is not None and len(values) > 0:
                        singlefile['FULLPATH'] = values[0][0]
                        singlefile['SCENE'] = values[0][3]
                        singlefile['TAKE'] = values[0][4]
                        singlefile['DIRECTOR'] = values[0][5]
                        singlefile['CINEMATOGRAPHER'] = values[0][6]
                        singlefile['PRODUCTION'] = values[0][7]
                        singlefile['CIRCLE_TAKE'] = values[0][8]
                        singlefile['PRODUCTION_COMPANY'] = values[0][9]
                        singlefile['LOCATION'] = values[0][10]
                        singlefile['OPERATOR'] = values[0][11]
                        singlefile['User_Info_1'] = values[0][12]
                        singlefile['User_Info_2'] = values[0][13]
                        singlefile['Camera_Clip_Name'] = values[0][14]
                        singlefile['Camera_Family'] = values[0][15]
                        singlefile['Camera_Serial_Number'] = values[0][16]
                        singlefile['Camera_ID'] = values[0][17]
                        singlefile['Camera_Index'] = values[0][18]
                        singlefile['Camera_SUP_Name'] = values[0][19]
                        singlefile['Camera_Model'] = values[0][20]
                        singlefile['Camera_Product'] = values[0][21]
                        singlefile['Camera_SubProduct'] = values[0][22]
                        singlefile['System_Image_Creation_Date'] = values[0][23]
                        singlefile['System_Image_Creation_Time'] = values[0][24]
                        singlefile['Exposure_Time'] = values[0][25]
                        singlefile['Shutter_Angle'] = values[0][26]
                        singlefile['Mirror_Shutter_Running'] = values[0][27]
                        singlefile['Sensor_FPS'] = values[0][28]
                        singlefile['Project_FPS'] = values[0][29]
                        singlefile['Master_TC_Time_Base'] = values[0][30]
                        singlefile['Master_TC_Frame_Count'] = values[0][31]
                        singlefile['Master_TC_User_Info'] = values[0][32]
                        singlefile['Storage_Media_Serial_Number'] = values[0][33]
                        singlefile['SMPTE_UMID'] = values[0][34]
                        singlefile['Recorder_Type'] = values[0][35]
                        singlefile['Vari'] = values[0][36]
                        singlefile['UUID'] = values[0][37]
                        singlefile['Image_Width'] = values[0][38]
                        singlefile['Image_Height'] = values[0][39]
                        singlefile['Active_Image_Width'] = values[0][40]
                        singlefile['Active_Image_Height'] = values[0][41]
                        singlefile['Active_Image_Top'] = values[0][42]
                        singlefile['Active_Image_Left'] = values[0][43]
                        singlefile['Full_Image_Width'] = values[0][44]
                        singlefile['Full_Image_Height'] = values[0][45]
                        singlefile['Color_Processing_Version'] = values[0][46]
                        singlefile['White_Balance'] = values[0][47]
                        singlefile['White_Balance_CC'] = values[0][48]
                        singlefile['WB_Factor_R'] = values[0][49]
                        singlefile['WB_Factor_G'] = values[0][50]
                        singlefile['WB_Factor_B'] = values[0][51]
                        singlefile['WB_Applied_In_Camera'] = values[0][52]
                        singlefile['Exposure_Index_ASA'] = values[0][53]
                        singlefile['Target_Color_Space'] = values[0][54]
                        singlefile['Sharpness'] = values[0][55]
                        singlefile['Lens_Squeeze'] = values[0][56]
                        singlefile['Image_Orientation'] = values[0][57]
                        singlefile['Look'] = values[0][58]
                        singlefile['Look_Burned_In'] = values[0][59]
                        singlefile['Look_LUT_Mode'] = values[0][60]
                        singlefile['Look_LUT_Offset'] = values[0][61]
                        singlefile['Look_LUT_Size'] = values[0][62]
                        singlefile['Look_Saturation'] = values[0][63]
                        singlefile['CDL_Slope_R'] = values[0][64]
                        singlefile['CDL_Slope_G'] = values[0][65]
                        singlefile['CDL_Slope_B'] = values[0][66]
                        singlefile['CDL_Offset_R'] = values[0][67]
                        singlefile['CDL_Offset_G'] = values[0][68]
                        singlefile['CDL_Offset_B'] = values[0][69]
                        singlefile['CDL_Power_R'] = values[0][70]
                        singlefile['CDL_Power_G'] = values[0][71]
                        singlefile['CDL_Power_B'] = values[0][72]
                        singlefile['Printer_Lights_R'] = values[0][73]
                        singlefile['Printer_Lights_G'] = values[0][74]
                        singlefile['Printer_Lights_B'] = values[0][75]
                        singlefile['CDL_Mode'] = values[0][76]
                        singlefile['Lens_Model'] = values[0][77]
                        singlefile['Lens_Serial_Number'] = values[0][78]
                        singlefile['Lens_Distance_Unit'] = values[0][79]
                        singlefile['Lens_Focus_Distance'] = values[0][80]
                        singlefile['Lens_Focal_Length'] = values[0][81]
                        singlefile['Lens_Iris'] = values[0][82]
                        singlefile['Lens_Linear_Iris'] = values[0][83]
                        singlefile['RawEncoderFocus_RawLds'] = values[0][84]
                        singlefile['RawEncoderFocus_RawMotor'] = values[0][85]
                        singlefile['RawEncoderFocal_RawLds'] = values[0][86]
                        singlefile['RawEncoderFocal_RawMotor'] = values[0][87]
                        singlefile['RawEncoderIris_RawLds'] = values[0][88]
                        singlefile['RawEncoderIris_RawMotor'] = values[0][89]
                        singlefile['EncoderLimFocusLdsMin'] = values[0][90]
                        singlefile['EncoderLimFocusLdsMax'] = values[0][91]
                        singlefile['EncoderLimFocusMotorMin'] = values[0][92]
                        singlefile['EncoderLimFocusMotorMax'] = values[0][93]
                        singlefile['EncoderLimFocalLdsMin'] = values[0][94]
                        singlefile['EncoderLimFocalLdsMax'] = values[0][95]
                        singlefile['EncoderLimFocalMotorMin'] = values[0][96]
                        singlefile['EncoderLimFocalMotorMax'] = values[0][97]
                        singlefile['EncoderLimIrisLdsMin'] = values[0][98]
                        singlefile['EncoderLimIrisLdsMax'] = values[0][99]
                        singlefile['EncoderLimIrisMotorMin'] = values[0][100]
                        singlefile['EncoderLimIrisMotorMax'] = values[0][101]
                        singlefile['Lds_Lag_Type'] = values[0][102]
                        singlefile['Lds_Lag_Value'] = values[0][103]
                        singlefile['ND_Filter_Type'] = values[0][104]
                        singlefile['ND_Filter_Density'] = values[0][105]
                        singlefile['Camera_Tilt'] = values[0][106]
                        singlefile['Camera_Roll'] = values[0][107]
                        singlefile['Master_Slave_Setup_Info'] = values[0][108]
                        singlefile['S3D_Eye_Info'] = values[0][109]
                        singlefile['Sound_Roll'] = values[0][110]
                        singlefile['RAWTYPE'] = values[0][111]
                        singlefile['END_TC'] = values[0][112]


                        # print(values[0])

            cursor.close()

        except:
            print('something error in conformdb')
        finally:
            connect.close()

    def readvfxshotlist(self, vfxshotlistpath):
        for item in self._cliplist:
            item['shot'] = []
            item['sequence'] = []
        shotlist = xlrd.open_workbook(vfxshotlistpath)
        sheet = shotlist.sheets()[0]
        for row in xrange(sheet.nrows):
            cell = sheet.cell(row, 3)
            for clip in self._cliplist:
                if cell.value.split('.')[0].lower() in os.path.basename(clip['metadata'][0]['filepath'].lower()):
                    # print('find a match')
                    clip['sequence'].append(sheet.cell(row, 1).value)
                    if '_' in sheet.cell(row, 2).value:
                        clip['shot'].append(sheet.cell(row, 2).value.split('_')[-1])
                    else:
                        clip['shot'].append(sheet.cell(row, 2).value)

    def renametoVFX(self):
        digitregex = re.compile(r'(\d{3,})')
        for j in xrange(len(self._cliplist)):
            item = self._cliplist[j]
            duration = item['endframe'] - item['startframe'] + 1
            m = list(digitregex.finditer(item['metadata'][0]['filepath']))[-1]
            for i in xrange(duration):
                diframe = str(item['startframe'] + i).zfill(m.end() - m.start())
                oldname = item['metadata'][i]['filepath']
                newname = item['sequence'][0] + '_' + item['shot'][0] + '_plate_' + ('%04d' % (1001 + i)) + \
                          os.path.splitext(oldname)[-1]
                newname = os.path.join(os.path.dirname(oldname), newname)
                # print(oldname, newname)
                os.rename(oldname, newname)
            if self._shouldrenamefolder:
                oldfolder = os.path.dirname(oldname)
                newfolder = os.path.join(os.path.dirname(os.path.dirname(oldname)),
                                         ('%04d' % (j + 1)) + '_' + item['sequence'][0] + '_' + item['shot'][0])
                # print(oldfolder, newfolder)
                os.rename(oldfolder, newfolder)

    def updateftrackshotinfo(self, FTRACK_SERVER='http://192.168.9.200',
                             FTRACK_APIKEY='b445309f-1c5d-40ac-b68b-3fdfb4f3ccb9',
                             LOGNAME='andyguo', PROJECTNAME='Piggy Bank'):
        os.environ['FTRACK_SERVER'] = FTRACK_SERVER
        os.environ['FTRACK_APIKEY'] = FTRACK_APIKEY
        os.environ['LOGNAME'] = LOGNAME

        import ftrack

        project = ftrack.getProject(PROJECTNAME)

        if project is not None:
            print(project)

            for clip in self._cliplist:
                try:
                    shot = ftrack.getShot([PROJECTNAME, clip['sequence'][0], clip['shot'][0]])
                    shot.setMeta({})
                    temp = {}
                    temp['01_sequence'] = clip['sequence'][0]
                    temp['02_shot'] = clip['shot'][0]
                    temp['05_s3d'] = clip['s3d']
                    temp['06_metadata'] = str(clip['metadata'])
                    temp['03_startframe'] = clip['startframe']
                    temp['04_endframe'] = clip['endframe']

                    print(shot)

                    shot.setMeta(temp)
                    # break
                except:
                    print('no such shot')


if __name__ == '__main__':
    testclass = IOFTRACK()
    testclass.scantranscodefiles(r'/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW/PIPELINE_TEST_20150416 copy/Deliverable')
    testclass.readvfxshotlist(
        r'/Volumes/work/TEST_Footage/IOTOVFX_WORKFLOW/PIPELINE_TEST_20150416/Deliverable/template copy.xls')
    testclass.conformdb(r'/Users/mac/Desktop/Original.db')
    # testclass.conformdb(r'/Users/mac/Desktop/~Footage.db')
    # testclass.renametoVFX()
    testclass.updateftrackshotinfo()


    # print(testclass._cliplist)
