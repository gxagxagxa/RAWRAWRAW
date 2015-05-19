#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'mac'

import os
import subprocess
import csv
import sys
import datetime
import shutil
import sqlite3
import struct
import re

APP_PATH = os.path.realpath(sys.path[0])


class generaterawdb(object):
    def __init__(self):
        super(generaterawdb, self).__init__()
        self._scanpath = ''
        self._temppath = os.path.join(os.path.realpath(sys.path[0]), r'temppath_andy')
        self._allfiles = []
        self._rawtype = ['.ari', '.R3D']

    def choosescanpath(self):
        pass


    def _symbolari(self, arilist):
        for index, item in enumerate(arilist):
            try:
                os.symlink(item,
                           os.path.join(self._temppath, os.path.basename(self._scanpath), 'ari', '%08d.ari' % index))
            except:
                print('something error in ari symbol link')
        cmd = 'ARRIMetaExtract_CMD -i {0} -s \",\" -o {0}'.format(
            os.path.join(self._temppath, os.path.basename(self._scanpath), 'ari'))
        subprocess.call(cmd, shell=True)


    def _sqliteari(self, arilist, dbpath):
        self._symbolari(arilist)
        connect = sqlite3.connect(dbpath)
        try:
            cursor = connect.cursor()
            aricsv = os.path.join(self._temppath, os.path.basename(self._scanpath), 'ari', 'ArriExtractorOutput_0.csv')
            if os.path.exists(aricsv):
                with open(aricsv, 'r') as csvfile:
                    metadata = csv.reader(csvfile, delimiter=',')
                    for index, item in enumerate(metadata):
                        if index > 0:
                            cursor.execute('INSERT INTO RAWMETADATA ('
                                           'FULLPATH,'
                                           'MASTER_TC,'
                                           'REEL,'
                                           'SCENE,'
                                           'TAKE,'
                                           'DIRECTOR,'
                                           'CINEMATOGRAPHER,'
                                           'PRODUCTION,'
                                           'CIRCLE_TAKE,'
                                           'PRODUCTION_COMPANY,'
                                           'LOCATION,'
                                           'OPERATOR,'
                                           'User_Info_1,'
                                           'User_Info_2,'
                                           'Camera_Clip_Name,'
                                           'Camera_Family,'
                                           'Camera_Serial_Number,'
                                           'Camera_ID,'
                                           'Camera_Index,'
                                           'Camera_SUP_Name,'
                                           'Camera_Model,'
                                           'Camera_Product,'
                                           'Camera_SubProduct,'
                                           'System_Image_Creation_Date,'
                                           'System_Image_Creation_Time,'
                                           'Exposure_Time,'
                                           'Shutter_Angle,'
                                           'Mirror_Shutter_Running,'
                                           'Sensor_FPS,'
                                           'Project_FPS,'
                                           'Master_TC_Time_Base,'
                                           'Master_TC_Frame_Count,'
                                           'Master_TC_User_Info,'
                                           'Storage_Media_Serial_Number,'
                                           'SMPTE_UMID,'
                                           'Recorder_Type,'
                                           'Vari,'
                                           'UUID,'
                                           'Image_Width,'
                                           'Image_Height,'
                                           'Active_Image_Width,'
                                           'Active_Image_Height,'
                                           'Active_Image_Top,'
                                           'Active_Image_Left,'
                                           'Full_Image_Width,'
                                           'Full_Image_Height,'
                                           'Color_Processing_Version,'
                                           'White_Balance,'
                                           'White_Balance_CC,'
                                           'WB_Factor_R,'
                                           'WB_Factor_G,'
                                           'WB_Factor_B,'
                                           'WB_Applied_In_Camera,'
                                           'Exposure_Index_ASA,'
                                           'Target_Color_Space,'
                                           'Sharpness,'
                                           'Lens_Squeeze,'
                                           'Image_Orientation,'
                                           'Look,'
                                           'Look_Burned_In,'
                                           'Look_LUT_Mode,'
                                           'Look_LUT_Offset,'
                                           'Look_LUT_Size,'
                                           'Look_Saturation,'
                                           'CDL_Slope_R,'
                                           'CDL_Slope_G,'
                                           'CDL_Slope_B,'
                                           'CDL_Offset_R,'
                                           'CDL_Offset_G,'
                                           'CDL_Offset_B,'
                                           'CDL_Power_R,'
                                           'CDL_Power_G,'
                                           'CDL_Power_B,'
                                           'Printer_Lights_R,'
                                           'Printer_Lights_G,'
                                           'Printer_Lights_B,'
                                           'CDL_Mode,'
                                           'Lens_Model,'
                                           'Lens_Serial_Number,'
                                           'Lens_Distance_Unit,'
                                           'Lens_Focus_Distance,'
                                           'Lens_Focal_Length,'
                                           'Lens_Iris,'
                                           'Lens_Linear_Iris,'
                                           'RawEncoderFocus_RawLds,'
                                           'RawEncoderFocus_RawMotor,'
                                           'RawEncoderFocal_RawLds,'
                                           'RawEncoderFocal_RawMotor,'
                                           'RawEncoderIris_RawLds,'
                                           'RawEncoderIris_RawMotor,'
                                           'EncoderLimFocusLdsMin,'
                                           'EncoderLimFocusLdsMax,'
                                           'EncoderLimFocusMotorMin,'
                                           'EncoderLimFocusMotorMax,'
                                           'EncoderLimFocalLdsMin,'
                                           'EncoderLimFocalLdsMax,'
                                           'EncoderLimFocalMotorMin,'
                                           'EncoderLimFocalMotorMax,'
                                           'EncoderLimIrisLdsMin,'
                                           'EncoderLimIrisLdsMax,'
                                           'EncoderLimIrisMotorMin,'
                                           'EncoderLimIrisMotorMax,'
                                           'Lds_Lag_Type,'
                                           'Lds_Lag_Value,'
                                           'ND_Filter_Type,'
                                           'ND_Filter_Density,'
                                           'Camera_Tilt,'
                                           'Camera_Roll,'
                                           'Master_Slave_Setup_Info,'
                                           'S3D_Eye_Info,'
                                           'Sound_Roll,'
                                           'RAWTYPE,'
                                           'END_TC'
                                           ') VALUES ('
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                           (arilist[index - 1], item[1], item[2], item[3], item[4], item[5], item[6],
                                            item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14],
                                            item[15], item[16], item[17], item[18], item[19], item[20], item[21],
                                            item[22],
                                            item[23], item[24], item[25], item[26], item[27], item[28], item[29],
                                            item[31], item[32], item[33], item[34], item[35], item[36], item[37],
                                            item[38],
                                            item[39], item[40], item[41], item[42], item[43], item[44], item[45],
                                            item[46],
                                            item[47], item[48], item[49], item[50], item[51], item[52], item[53],
                                            item[54],
                                            item[55], item[56], item[57], item[58], item[59], item[60], item[61],
                                            item[62],
                                            item[63], item[64], item[65], item[66], item[67], item[68], item[69],
                                            item[70],
                                            item[71], item[72], item[73], item[74], item[75], item[76], item[77],
                                            item[78],
                                            item[79], item[80], item[81], item[82], item[83], item[84], item[85],
                                            item[86],
                                            item[87], item[88], item[89], item[90], item[91], item[92], item[93],
                                            item[94],
                                            item[95], item[96], item[97], item[98], item[99], item[100], item[101],
                                            item[102],
                                            item[103], item[104], item[105], item[106], item[107], item[108], item[109],
                                            item[110], item[111],
                                            'ari', item[1]))
                    cursor.close()
                    connect.commit()
        except:
            print('something error in sqlite database')

        finally:
            connect.close()


    def _sqliter3d(self, r3dlist, dbpath):
        r3dscv = os.path.join(self._temppath, os.path.basename(self._scanpath), 'R3D', 'R3D_metadata_output.csv')
        # print(r3dscv)
        for index, item in enumerate(r3dlist):
            try:
                os.symlink(item,
                           os.path.join(self._temppath, os.path.basename(self._scanpath), 'R3D', '%08d.R3D' % index))
                cmd = 'REDline --i {0} --printMeta 2 >> {1}'.format(
                    os.path.join(self._temppath, os.path.basename(self._scanpath), 'R3D', '%08d.R3D' % index), r3dscv)
                subprocess.call(cmd, shell=True)

            except:
                print('something error in R3D symbol link')

        connect = sqlite3.connect(dbpath)
        try:
            # print(r3dlist)
            cursor = connect.cursor()
            if os.path.exists(r3dscv):
                with open(r3dscv) as csvfile:
                    metadata = csv.reader(csvfile, delimiter=',')
                    for index, item in enumerate(metadata):
                        if index % 2 == 1:

                            colorspace = '--'
                            if item[30] == '2' or item[30] == '11':
                                colorspace = 'REDspace'
                            if item[30] == '0' or item[30] == '12':
                                colorspace = 'CameraRGB'
                            if item[30] == '1' or item[30] == '13':
                                colorspace = 'rec709'
                            if item[30] == '14':
                                colorspace = 'REDcolor'
                            if item[30] == '15':
                                colorspace = 'sRGB'
                            if item[30] == '5':
                                colorspace = 'Adobe1998'
                            if item[30] == '18':
                                colorspace = 'REDcolor2'
                            if item[30] == '19':
                                colorspace = 'REDcolor3'
                            if item[30] == '20':
                                colorspace = 'DRAGONcolor'
                            if item[30] == '21':
                                colorspace = 'XYZ'

                            cursor.execute('INSERT INTO RAWMETADATA ('
                                           'FULLPATH,'
                                           'MASTER_TC,'
                                           'REEL,'
                                           'SCENE,'
                                           'TAKE,'
                                           'DIRECTOR,'
                                           'CINEMATOGRAPHER,'
                                           'PRODUCTION,'
                                           'CIRCLE_TAKE,'
                                           'PRODUCTION_COMPANY,'
                                           'LOCATION,'
                                           'OPERATOR,'
                                           'Camera_Clip_Name,'
                                           'Camera_Family,'
                                           'Camera_Serial_Number,'
                                           'Camera_ID,'
                                           'Camera_Index,'
                                           'Camera_SUP_Name,'
                                           'Camera_Model,'
                                           'Camera_Product,'
                                           'Camera_SubProduct,'
                                           'System_Image_Creation_Date,'
                                           'Exposure_Time,'
                                           'Shutter_Angle,'
                                           'Mirror_Shutter_Running,'
                                           'Sensor_FPS,'
                                           'Project_FPS,'
                                           'Master_TC_Time_Base,'
                                           'Master_TC_Frame_Count,'
                                           'Storage_Media_Serial_Number,'
                                           'SMPTE_UMID,'
                                           'Recorder_Type,'
                                           'Image_Width,'
                                           'Image_Height,'
                                           'Active_Image_Width,'
                                           'Active_Image_Height,'
                                           'White_Balance,'
                                           'Exposure_Index_ASA,'
                                           'Target_Color_Space,'
                                           'Lens_Model,'
                                           'Lens_Serial_Number,'
                                           'Lens_Distance_Unit,'
                                           'Lens_Focus_Distance,'
                                           'Lens_Focal_Length,'
                                           'Lens_Iris,'
                                           'S3D_Eye_Info,'
                                           'RAWTYPE,'
                                           'END_TC'
                                           ') VALUES ('
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                           (r3dlist[index / 2 - 1], item[26],
                                            os.path.basename(r3dlist[index / 2 - 1])[:15],
                                            item[77], item[79], item[84], item[83],
                                            item[81], item[86], '--', item[82], item[85],
                                            os.path.basename(r3dlist[index / 2 - 1]),
                                            item[9], item[10], item[10], item[6], item[55], item[7], item[7],
                                            item[13],
                                            item[19], item[52] + ' ms', item[54], 'N/A', item[24], item[23], item[24],
                                            self.__timecodetoframe(item[26], item[24]),
                                            item[12], '--', item[117], item[21],
                                            item[22],
                                            item[21], item[22],
                                            item[32],
                                            item[34], colorspace, item[70], '--', 'mm', item[68], item[67], item[66],
                                            item[116],
                                            'r3d', item[28]))

                    cursor.close()
                    connect.commit()

        except:
            print('something error in sqliter3d method')
        finally:
            connect.close()


    def _initsqlitedb(self, dbpath):
        connect = sqlite3.connect(dbpath)
        try:
            cursor = connect.cursor()
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS RAWMETADATA ('
                'FULLPATH TEXT PRIMARY KEY NOT NULL, '
                'MASTER_TC TEXT NOT NULL, '
                'REEL TEXT NOT NULL,'
                'SCENE TEXT,'
                'TAKE TEXT,'
                'DIRECTOR TEXT,'
                'CINEMATOGRAPHER TEXT,'
                'PRODUCTION TEXT,'
                'CIRCLE_TAKE TEXT,'
                'PRODUCTION_COMPANY TEXT,'
                'LOCATION TEXT,'
                'OPERATOR TEXT,'
                'User_Info_1 TEXT,'
                'User_Info_2 TEXT,'
                'Camera_Clip_Name TEXT,'
                'Camera_Family TEXT,'
                'Camera_Serial_Number TEXT,'
                'Camera_ID TEXT,'
                'Camera_Index TEXT,'
                'Camera_SUP_Name TEXT,'
                'Camera_Model TEXT,'
                'Camera_Product TEXT,'
                'Camera_SubProduct TEXT,'
                'System_Image_Creation_Date TEXT,'
                'System_Image_Creation_Time TEXT,'
                'Exposure_Time TEXT,'
                'Shutter_Angle TEXT,'
                'Mirror_Shutter_Running TEXT,'
                'Sensor_FPS TEXT,'
                'Project_FPS TEXT,'
                'Master_TC_Time_Base TEXT,'
                'Master_TC_Frame_Count TEXT,'
                'Master_TC_User_Info TEXT,'
                'Storage_Media_Serial_Number TEXT,'
                'SMPTE_UMID TEXT,'
                'Recorder_Type TEXT,'
                'Vari TEXT,'
                'UUID TEXT,'
                'Image_Width INT,'
                'Image_Height INT,'
                'Active_Image_Width INT,'
                'Active_Image_Height INT,'
                'Active_Image_Top INT,'
                'Active_Image_Left INT,'
                'Full_Image_Width INT,'
                'Full_Image_Height INT,'
                'Color_Processing_Version INT,'
                'White_Balance INT,'
                'White_Balance_CC TEXT,'
                'WB_Factor_R REAL,'
                'WB_Factor_G REAL,'
                'WB_Factor_B REAL,'
                'WB_Applied_In_Camera TEXT,'
                'Exposure_Index_ASA INT,'
                'Target_Color_Space TEXT,'
                'Sharpness INT,'
                'Lens_Squeeze TEXT,'
                'Image_Orientation TEXT,'
                'Look TEXT,'
                'Look_Burned_In TEXT,'
                'Look_LUT_Mode TEXT,'
                'Look_LUT_Offset TEXT,'
                'Look_LUT_Size TEXT,'
                'Look_Saturation REAL,'
                'CDL_Slope_R REAL,'
                'CDL_Slope_G REAL,'
                'CDL_Slope_B REAL,'
                'CDL_Offset_R REAL,'
                'CDL_Offset_G REAL,'
                'CDL_Offset_B REAL,'
                'CDL_Power_R REAL,'
                'CDL_Power_G REAL,'
                'CDL_Power_B REAL,'
                'Printer_Lights_R REAL,'
                'Printer_Lights_G REAL,'
                'Printer_Lights_B REAL,'
                'CDL_Mode TEXT,'
                'Lens_Model TEXT,'
                'Lens_Serial_Number TEXT,'
                'Lens_Distance_Unit TEXT,'
                'Lens_Focus_Distance TEXT,'
                'Lens_Focal_Length TEXT,'
                'Lens_Iris TEXT,'
                'Lens_Linear_Iris TEXT,'
                'RawEncoderFocus_RawLds TEXT,'
                'RawEncoderFocus_RawMotor TEXT,'
                'RawEncoderFocal_RawLds TEXT,'
                'RawEncoderFocal_RawMotor TEXT,'
                'RawEncoderIris_RawLds TEXT,'
                'RawEncoderIris_RawMotor TEXT,'
                'EncoderLimFocusLdsMin TEXT,'
                'EncoderLimFocusLdsMax TEXT,'
                'EncoderLimFocusMotorMin TEXT,'
                'EncoderLimFocusMotorMax TEXT,'
                'EncoderLimFocalLdsMin TEXT,'
                'EncoderLimFocalLdsMax TEXT,'
                'EncoderLimFocalMotorMin TEXT,'
                'EncoderLimFocalMotorMax TEXT,'
                'EncoderLimIrisLdsMin TEXT,'
                'EncoderLimIrisLdsMax TEXT,'
                'EncoderLimIrisMotorMin TEXT,'
                'EncoderLimIrisMotorMax TEXT,'
                'Lds_Lag_Type TEXT,'
                'Lds_Lag_Value TEXT,'
                'ND_Filter_Type TEXT,'
                'ND_Filter_Density TEXT,'
                'Camera_Tilt REAL,'
                'Camera_Roll REAL,'
                'Master_Slave_Setup_Info TEXT,'
                'S3D_Eye_Info TEXT,'
                'Sound_Roll TEXT,'
                'RAWTYPE TEXT,'
                'END_TC TEXT'
                ');')
            cursor.close()
            connect.commit()
        except:
            print('something error init sqlite db')
        finally:
            connect.close()


    def _processmovmetadata(self, movmessage):
        movmetadata = {'MASTER_TC': '00:00:00:00', 'REEL': '--', 'duration': '00:00:00:00', 'creation_date': '',
                       'creation_time': '', 'encoder': '', 'fps': '24', 'width': '', 'height': ''}
        for index, line in enumerate(movmessage.split(os.linesep)):
            # print(index, line)
            if 'Duration' in line:
                # print(line.split(',')[0].split(':')[-1].lstrip().rstrip())
                movmetadata['duration'] = line.split(',')[0].split(': ')[-1].lstrip().rstrip()
            if 'creation_time' in line:
                # print(line.split(' : ')[-1].lstrip().rstrip())
                movmetadata['creation_date'] = line.split(' : ')[-1].lstrip().rstrip().split(' ')[0]
                movmetadata['creation_time'] = line.split(' : ')[-1].lstrip().rstrip().split(' ')[1]
            if 'encoder' in line:
                # print(line.split(':')[-1].lstrip().rstrip())
                movmetadata['encoder'] = line.split(' : ')[-1].lstrip().rstrip()
            if 'reel_name' in line:
                # print(line.split(':')[-1].lstrip().rstrip())
                movmetadata['REEL'] = line.split(' : ')[-1].lstrip().rstrip()
            if 'timecode' in line:
                # print(line.split(' : ')[-1].lstrip().rstrip())
                movmetadata['MASTER_TC'] = line.split(' : ')[-1].lstrip().rstrip()
            if 'Stream' in line and 'Video' in line and 'fps' in line:
                # print(line.split(',')[4].lstrip().rstrip().split(' ')[0])
                movmetadata['fps'] = line.split('fps')[0].lstrip().rstrip().split(',')[-1].lstrip().rstrip()
                movmetadata['width'] = line.split(',')[2].lstrip().rstrip().split(' ')[0].split('x')[0]
                movmetadata['height'] = line.split(',')[2].lstrip().rstrip().split(' ')[0].split('x')[1]
        return movmetadata


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


    def _sqlitemov(self, movlist, dbpath):
        connect = sqlite3.connect(dbpath)
        try:
            cursor = connect.cursor()
            for index, item in enumerate(movlist):
                os.symlink(item,
                           os.path.join(self._temppath, os.path.basename(self._scanpath), 'mov', '%08d.mov' % index))
                cmd = ['ffmpeg -i {0}'.format(
                    os.path.join(self._temppath, os.path.basename(self._scanpath), 'mov', '%08d.mov' % index))]
                message = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE).communicate()[1]

                movmetadata = self._processmovmetadata(message)
                # print(movmetadata)
                # print(index, item)

                cursor.execute('INSERT INTO RAWMETADATA ('
                               'FULLPATH,'
                               'MASTER_TC,'
                               'REEL,'
                               'Camera_Clip_Name,'
                               'System_Image_Creation_Date,'
                               'System_Image_Creation_Time,'
                               'Sensor_FPS,'
                               'Project_FPS,'
                               'Master_TC_Time_Base,'
                               'Master_TC_Frame_Count,'
                               'Recorder_Type,'
                               'Image_Width,'
                               'Image_Height,'
                               'Active_Image_Width,'
                               'Active_Image_Height,'
                               'Active_Image_Top,'
                               'Active_Image_Left,'
                               'Full_Image_Width,'
                               'Full_Image_Height,'
                               'RAWTYPE,'
                               'END_TC'
                               ') VALUES ('
                               '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                               '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                               (movlist[index], movmetadata['MASTER_TC'], movmetadata['REEL'],
                                os.path.basename(movlist[index]), movmetadata['creation_date'],
                                movmetadata['creation_time'], movmetadata['fps'], movmetadata['fps'],
                                movmetadata['fps'],
                                self.__timecodetoframe(movmetadata['MASTER_TC'], movmetadata['fps']),
                                movmetadata['encoder'],
                                movmetadata['width'], movmetadata['height'],
                                movmetadata['width'], movmetadata['height'], '0', '0', movmetadata['width'],
                                movmetadata['height'], 'mov',
                                self.__timecodeadd(movmetadata['MASTER_TC'], movmetadata['duration'],
                                                   movmetadata['fps'])))

            cursor.close()
            connect.commit()

        except:
            print('something error in mov symbol link')
        finally:
            connect.close()


    def _processmp4metadata(self, mp4message):
        mp4metadata = {'MASTER_TC': '00:00:00:00', 'REEL': '--', 'duration': '00:00:00:00', 'creation_date': '',
                       'creation_time': '', 'encoder': '', 'fps': '24', 'width': '', 'height': ''}
        for index, line in enumerate(mp4message.split(os.linesep)):
            # print(index, line)
            if 'Duration' in line:
                # print(line.split(',')[0].split(':')[-1].lstrip().rstrip())
                mp4metadata['duration'] = line.split(',')[0].split(': ')[-1].lstrip().rstrip()
            if 'creation_time' in line:
                # print(line.split(' : ')[-1].lstrip().rstrip())
                mp4metadata['creation_date'] = line.split(' : ')[-1].lstrip().rstrip().split(' ')[0]
                mp4metadata['creation_time'] = line.split(' : ')[-1].lstrip().rstrip().split(' ')[1]
            if 'encoder' in line:
                # print(line.split(':')[-1].lstrip().rstrip())
                mp4metadata['encoder'] = line.split(' : ')[-1].lstrip().rstrip()
            if 'reel_name' in line:
                # print(line.split(':')[-1].lstrip().rstrip())
                mp4metadata['REEL'] = line.split(' : ')[-1].lstrip().rstrip()
            if 'timecode' in line:
                # print(line.split(' : ')[-1].lstrip().rstrip())
                mp4metadata['MASTER_TC'] = line.split(' : ')[-1].lstrip().rstrip()
            if 'Stream' in line and 'Video' in line and 'fps' in line:
                # print(line.split(',')[4].lstrip().rstrip().split(' ')[0])
                mp4metadata['fps'] = line.split('fps')[0].lstrip().rstrip().split(',')[-1].lstrip().rstrip()
                mp4metadata['width'] = line.split(',')[2].lstrip().rstrip().split(' ')[0].split('x')[0]
                mp4metadata['height'] = line.split(',')[2].lstrip().rstrip().split(' ')[0].split('x')[1]
        return mp4metadata


    def _sqlitemp4(self, mp4list, dbpath):
        connect = sqlite3.connect(dbpath)
        try:
            cursor = connect.cursor()
            for index, item in enumerate(mp4list):
                os.symlink(item,
                           os.path.join(self._temppath, os.path.basename(self._scanpath), 'mp4', '%08d.mp4' % index))
                cmd = ['ffmpeg -i {0}'.format(
                    os.path.join(self._temppath, os.path.basename(self._scanpath), 'mp4', '%08d.mp4' % index))]
                message = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE).communicate()[1]

                mp4metadata = self._processmp4metadata(message)
                # print(mp4metadata)
                # print(index, item)

                cursor.execute('INSERT INTO RAWMETADATA ('
                               'FULLPATH,'
                               'MASTER_TC,'
                               'REEL,'
                               'Camera_Clip_Name,'
                               'System_Image_Creation_Date,'
                               'System_Image_Creation_Time,'
                               'Sensor_FPS,'
                               'Project_FPS,'
                               'Master_TC_Time_Base,'
                               'Master_TC_Frame_Count,'
                               'Recorder_Type,'
                               'Image_Width,'
                               'Image_Height,'
                               'Active_Image_Width,'
                               'Active_Image_Height,'
                               'Active_Image_Top,'
                               'Active_Image_Left,'
                               'Full_Image_Width,'
                               'Full_Image_Height,'
                               'RAWTYPE,'
                               'END_TC'
                               ') VALUES ('
                               '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                               '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                               (mp4list[index], mp4metadata['MASTER_TC'], mp4metadata['REEL'],
                                os.path.basename(mp4list[index]), mp4metadata['creation_date'],
                                mp4metadata['creation_time'], mp4metadata['fps'], mp4metadata['fps'],
                                mp4metadata['fps'],
                                self.__timecodetoframe(mp4metadata['MASTER_TC'], mp4metadata['fps']),
                                mp4metadata['encoder'],
                                mp4metadata['width'], mp4metadata['height'],
                                mp4metadata['width'], mp4metadata['height'], '0', '0', mp4metadata['width'],
                                mp4metadata['height'], 'mp4',
                                self.__timecodeadd(mp4metadata['MASTER_TC'], mp4metadata['duration'],
                                                   mp4metadata['fps'])))

            cursor.close()
            connect.commit()

        except:
            print('something error in mp4 symbol link')
        finally:
            connect.close()


    def _sqlitedpx(self, dpxlist, dbpath):
        # print('==== _sqlitedpx  ====')
        connect = sqlite3.connect(dbpath)
        try:
            cursor = connect.cursor()
            for index, item in enumerate(dpxlist):
                os.symlink(item,
                           os.path.join(self._temppath, os.path.basename(self._scanpath), 'dpx', '%08d.dpx' % index))
                dpxheader = ()
                with open(os.path.join(self._temppath, os.path.basename(self._scanpath), 'dpx', '%08d.dpx' % index),
                          'rb') as dpxfile:
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

                reel =re.sub(r'\W', '', dpxheader[29])
                if(len(reel)) == 0:
                    reel = '--'
                # print(reel)

                cursor.execute('INSERT INTO RAWMETADATA ('
                               'FULLPATH, '
                               'MASTER_TC, '
                               'REEL, '
                               'Camera_Clip_Name, '
                               'Sensor_FPS,'
                               'Project_FPS,'
                               'Master_TC_Time_Base,'
                               'Master_TC_Frame_Count,'
                               'Image_Width,'
                               'Image_Height,'
                               'Active_Image_Width,'
                               'Active_Image_Height,'
                               'Active_Image_Top,'
                               'Active_Image_Left,'
                               'Full_Image_Width,'
                               'Full_Image_Height,'
                               'RAWTYPE,'
                               'END_TC'
                               ') VALUES ('
                               '?, ?, ?, ?, ?, ? ,?, ?, ?, ?,'
                               '?, ?, ?, ?, ?, ? , ?, ?)',
                               (item, tc, reel, os.path.basename(item),
                                fps, fps, fps, self.__timecodetoframe(tc, fps), dpxheader[17], dpxheader[18],
                                dpxheader[17], dpxheader[18], 0, 0, dpxheader[17], dpxheader[18], 'dpx',
                                tc))

            cursor.close()
            connect.commit()


        except:
            print('something error in sqlitedpx')
        finally:
            connect.close()


    def _processmxfmetadata(self, mxfmessage):
        mxfmetadata = {'MASTER_TC': '00:00:00:00', 'REEL': '--', 'duration': '00:00:00:00', 'creation_date': '',
                       'creation_time': '', 'encoder': '', 'fps': '24', 'width': '', 'height': ''}
        for index, line in enumerate(mxfmessage.split(os.linesep)):
            # print(index, line)
            if 'Duration' in line:
                # print(line.split(',')[0].split(':')[-1].lstrip().rstrip())
                mxfmetadata['duration'] = line.split(',')[0].split(': ')[-1].lstrip().rstrip()
            if 'modification_date' in line or 'creation_time' in line:
                # print(line.split(' : ')[-1].lstrip().rstrip())
                mxfmetadata['creation_date'] = line.split(': ')[-1].lstrip().rstrip().split(' ')[0]
                mxfmetadata['creation_time'] = line.split(': ')[-1].lstrip().rstrip().split(' ')[1]
            if 'product_name' in line:
                # print(line.split(':')[-1].lstrip().rstrip())
                mxfmetadata['encoder'] = line.split(' : ')[-1].lstrip().rstrip()
            if 'reel_name' in line:
                # print(line.split(':')[-1].lstrip().rstrip())
                mxfmetadata['REEL'] = line.split(' : ')[-1].lstrip().rstrip()
            if 'timecode' in line:
                # print(line.split(' : ')[-1].lstrip().rstrip())
                mxfmetadata['MASTER_TC'] = line.split(' : ')[-1].lstrip().rstrip()
            if 'Stream' in line and 'Video' in line and 'fps' in line:
                # print(line.split(',')[4].lstrip().rstrip().split(' ')[0])
                mxfmetadata['fps'] = line.split('tbr')[0].lstrip().rstrip().split(',')[-1].lstrip().rstrip()
                mxfmetadata['width'] = line.split(',')[2].lstrip().rstrip().split(' ')[0].split('x')[0]
                mxfmetadata['height'] = line.split(',')[2].lstrip().rstrip().split(' ')[0].split('x')[1]
        # print(mxfmetadata)
        return mxfmetadata


    def _sqlitemxf(self, mxflist, dbpath):
        connect = sqlite3.connect(dbpath)
        try:
            cursor = connect.cursor()
            for index, item in enumerate(mxflist):
                os.symlink(item,
                           os.path.join(self._temppath, os.path.basename(self._scanpath), 'mxf', '%08d.mxf' % index))
                cmd = ['ffmpeg -i {0}'.format(
                    os.path.join(self._temppath, os.path.basename(self._scanpath), 'mxf', '%08d.mxf' % index))]
                message = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE).communicate()[1]

                mxfmetadata = self._processmxfmetadata(message)
                # print(mp4metadata)
                # print(index, item)

                cursor.execute('INSERT INTO RAWMETADATA ('
                               'FULLPATH,'
                               'MASTER_TC,'
                               'REEL,'
                               'Camera_Clip_Name,'
                               'System_Image_Creation_Date,'
                               'System_Image_Creation_Time,'
                               'Sensor_FPS,'
                               'Project_FPS,'
                               'Master_TC_Time_Base,'
                               'Master_TC_Frame_Count,'
                               'Recorder_Type,'
                               'Image_Width,'
                               'Image_Height,'
                               'Active_Image_Width,'
                               'Active_Image_Height,'
                               'Active_Image_Top,'
                               'Active_Image_Left,'
                               'Full_Image_Width,'
                               'Full_Image_Height,'
                               'RAWTYPE,'
                               'END_TC'
                               ') VALUES ('
                               '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                               '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                               (item, mxfmetadata['MASTER_TC'], mxfmetadata['REEL'],
                                os.path.basename(item), mxfmetadata['creation_date'],
                                mxfmetadata['creation_time'], mxfmetadata['fps'], mxfmetadata['fps'],
                                mxfmetadata['fps'],
                                self.__timecodetoframe(mxfmetadata['MASTER_TC'], mxfmetadata['fps']),
                                mxfmetadata['encoder'],
                                mxfmetadata['width'], mxfmetadata['height'],
                                mxfmetadata['width'], mxfmetadata['height'], '0', '0', mxfmetadata['width'],
                                mxfmetadata['height'], 'mxf',
                                self.__timecodeadd(mxfmetadata['MASTER_TC'], mxfmetadata['duration'],
                                                   mxfmetadata['fps'])))

            cursor.close()
            connect.commit()

        except:
            print('something error in mxf symbol link')
        finally:
            connect.close()


    def _processexrmessage(self, exrmessage):
        exrmetadata = {'MASTER_TC': '00:00:00:00', 'REEL': '--', 'duration': '00:00:00:00', 'creation_date': '',
                       'creation_time': '', 'encoder': '', 'fps': '24', 'width': '', 'height': ''}
        for line in exrmessage.split(os.linesep):
            if 'time' in line and '(' not in line:
                # print(line)
                exrmetadata['MASTER_TC'] = line.split('time')[-1].lstrip().rstrip()
            if 'dataWindow' in line:
                # print(line)
                exrmetadata['width'] = int(line.split(': ')[-1].split(' - ')[-1].lstrip('(').rstrip(')').split(' ')[0]) + 1
                exrmetadata['height'] = int(line.split(': ')[-1].split(' - ')[-1].lstrip('(').rstrip(')').split(' ')[-1]) + 1
            if 'framesPerSecond' in line:
                # print(line)
                exrmetadata['fps'] = line.split(': ')[-1].split('(')[-1].rstrip(')')
            if 'compression' in line:
                # print(line)
                exrmetadata['encoder'] = line.split(': ')[-1].rstrip()

        # print(exrmetadata)
        return exrmetadata



    def _sqliteexr(self, exrlist, dbpath):
        connect = sqlite3.connect(dbpath)
        try:
            cursor = connect.cursor()
            for index, item in enumerate(exrlist):
                os.symlink(item,
                           os.path.join(self._temppath, os.path.basename(self._scanpath), 'exr', '%08d.exr' % index))
                cmd = ['exrheader {0}'.format(
                    os.path.join(self._temppath, os.path.basename(self._scanpath), 'exr', '%08d.exr' % index))]
                message = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
                # print(message)
                exrmetadata = self._processexrmessage(message)
                # print(mp4metadata)
                # print(index, item)

                cursor.execute('INSERT INTO RAWMETADATA ('
                               'FULLPATH,'
                               'MASTER_TC,'
                               'REEL,'
                               'Camera_Clip_Name,'
                               'System_Image_Creation_Date,'
                               'System_Image_Creation_Time,'
                               'Sensor_FPS,'
                               'Project_FPS,'
                               'Master_TC_Time_Base,'
                               'Master_TC_Frame_Count,'
                               'Recorder_Type,'
                               'Image_Width,'
                               'Image_Height,'
                               'Active_Image_Width,'
                               'Active_Image_Height,'
                               'Active_Image_Top,'
                               'Active_Image_Left,'
                               'Full_Image_Width,'
                               'Full_Image_Height,'
                               'RAWTYPE,'
                               'END_TC'
                               ') VALUES ('
                               '?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                               '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                               (item, exrmetadata['MASTER_TC'], exrmetadata['REEL'],
                                os.path.basename(item), exrmetadata['creation_date'],
                                exrmetadata['creation_time'], exrmetadata['fps'], exrmetadata['fps'],
                                exrmetadata['fps'],
                                self.__timecodetoframe(exrmetadata['MASTER_TC'], exrmetadata['fps']),
                                exrmetadata['encoder'],
                                exrmetadata['width'], exrmetadata['height'],
                                exrmetadata['width'], exrmetadata['height'], '0', '0', exrmetadata['width'],
                                exrmetadata['height'], 'exr',
                                exrmetadata['MASTER_TC']))

            cursor.close()
            connect.commit()

        except:
            print('something error in exr symbol link')
        finally:
            connect.close()




    def generatedb(self):
        self._allfiles = []
        self._allfiles = [os.path.join(root, singlefile) for root, subfolder, files in os.walk(self._scanpath) for
                          singlefile in files]
        # self._allfiles.sort()
        arilist = [item for item in self._allfiles if os.path.splitext(item)[-1].lower() == '.ari']
        r3dlist = [item for item in self._allfiles if os.path.splitext(item)[-1].lower() == '.r3d']
        movlist = [item for item in self._allfiles if os.path.splitext(item)[-1].lower() == '.mov']
        mp4list = [item for item in self._allfiles if os.path.splitext(item)[-1].lower() == '.mp4']
        dpxlist = [item for item in self._allfiles if os.path.splitext(item)[-1].lower() == '.dpx']
        mxflist = [item for item in self._allfiles if os.path.splitext(item)[-1].lower() == '.mxf']
        exrlist = [item for item in self._allfiles if os.path.splitext(item)[-1].lower() == '.exr']


        if os.path.exists(self._temppath):
            shutil.rmtree(self._temppath)
        os.mkdir(self._temppath)
        os.mkdir(os.path.join(self._temppath, os.path.basename(self._scanpath)))
        os.mkdir(os.path.join(self._temppath, os.path.basename(self._scanpath), 'ari'))
        os.mkdir(os.path.join(self._temppath, os.path.basename(self._scanpath), 'R3D'))
        os.mkdir(os.path.join(self._temppath, os.path.basename(self._scanpath), 'mov'))
        os.mkdir(os.path.join(self._temppath, os.path.basename(self._scanpath), 'mp4'))
        os.mkdir(os.path.join(self._temppath, os.path.basename(self._scanpath), 'dpx'))
        os.mkdir(os.path.join(self._temppath, os.path.basename(self._scanpath), 'mxf'))
        os.mkdir(os.path.join(self._temppath, os.path.basename(self._scanpath), 'exr'))

        starttime = datetime.datetime.now()
        print(starttime)

        dbpath = os.path.join(os.path.expanduser('~'), 'Desktop', os.path.basename(self._scanpath) + '.db')
        self._initsqlitedb(dbpath)
        # self._sqliteari(arilist, dbpath)
        # self._sqliter3d(r3dlist, dbpath)
        # self._sqlitemov(movlist, dbpath)
        # self._sqlitemp4(mp4list, dbpath)
        # self._sqlitedpx(dpxlist, dbpath)
        # self._sqlitemxf(mxflist, dbpath)
        self._sqliteexr(exrlist, dbpath)

        endtime = datetime.datetime.now()
        print(endtime - starttime)


if __name__ == '__main__':
    testclass = generaterawdb()
    testclass._scanpath = r'/Volumes/work/TEST_Footage/~Footage'
    # testclass._scanpath = r'/Users/andyguo/Desktop/work/FOOTAGE'
    testclass.generatedb()
    pass