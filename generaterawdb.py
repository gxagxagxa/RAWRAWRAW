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
            finally:
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
                                           'RAWTYPE'
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
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                           (arilist[index - 1], item[1], item[2], item[3], item[4], item[5], item[6],
                                            item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14],
                                            item[15], item[16], item[17], item[18], item[19], item[20], item[21],
                                            item[22],
                                            item[23], item[24], item[25], item[26], item[27], item[28], item[29],
                                            item[30],
                                            item[31], item[32], item[33], item[34], item[35], item[36], item[37],
                                            item[38],
                                            item[39], item[40], item[41], item[42], item[43], item[44], item[45],
                                            item[46],
                                            item[47], item[48], item[49], item[50], item[51], item[52], item[53],
                                            item[54],
                                            item[55], item[56], item[57], item[58], item[59], item[60], item[60],
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
                                            'ari'))
                    cursor.close()
                    connect.commit()
        except:
            print('something error in sqlite database')

        finally:
            connect.close()


    def _sqliter3d(self, r3dlist, dbpath):
        r3dscv = os.path.join(self._temppath, os.path.basename(self._scanpath), 'R3D', 'R3D_metadata_output.csv')
        print(r3dscv)
        for index, item in enumerate(r3dlist):
            try:
                os.symlink(item,
                           os.path.join(self._temppath, os.path.basename(self._scanpath), 'R3D', '%08d.R3D' % index))
                cmd = 'REDline --i {0} --printMeta 2 >> {1}'.format(
                    os.path.join(self._temppath, os.path.basename(self._scanpath), 'R3D', '%08d.R3D' % index), r3dscv)
                subprocess.call(cmd, shell=True)

            finally:
                print('something error in R3D symbol link')

        connect = sqlite3.connect(dbpath)
        try:
            # print(r3dlist)
            cursor = connect.cursor()
            if os.path.exists(r3dscv):
                with open(r3dscv) as csvfile:
                    metadata = csv.reader(csvfile, delimiter=',')
                    for index, item in enumerate(metadata):
                        if index %2 == 1:

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
                                           'RAWTYPE'
                                           ') VALUES ('
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                                           '?, ?, ?, ?, ?, ?, ?, ?)',
                                           (r3dlist[index/2 - 1], item[27], os.path.basename(r3dlist[index/2 - 1])[:15],
                                            item[77], item[79], item[84], item[83],
                                            item[81], item[86], '--', item[82], item[85],
                                            os.path.basename(r3dlist[index/2 - 1]),
                                            item[10], item[11], item[11], item[7], item[56], item[8], item[8],
                                            item[14],
                                            item[21], item[53] + ' ms', item[55], 'N/A', item[25], item[24], item[25],
                                            123456,
                                            item[13], '--', item[118], item[22],
                                            item[23],
                                            item[22], item[23],
                                            item[33],
                                            item[35], item[31], item[71], '--', 'mm', item[69], item[68], item[67],
                                            item[117],
                                            'r3d'))

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
                'RAWTYPE TEXT'
                ');')
            cursor.close()
            connect.commit()
        except:
            print('something error init sqlite db')
        finally:
            connect.close()


    def generatedb(self):
        self._allfiles = []
        self._allfiles = [os.path.join(root, singlefile) for root, subfolder, files in os.walk(self._scanpath) for
                          singlefile in files]
        # self._allfiles.sort()
        arilist = [item for item in self._allfiles if os.path.splitext(item)[-1] == '.ari']
        r3dlist = [item for item in self._allfiles if os.path.splitext(item)[-1] == '.R3D']

        if os.path.exists(self._temppath):
            shutil.rmtree(self._temppath)
        os.mkdir(self._temppath)
        os.mkdir(os.path.join(self._temppath, os.path.basename(self._scanpath)))
        os.mkdir(os.path.join(self._temppath, os.path.basename(self._scanpath), 'ari'))
        os.mkdir(os.path.join(self._temppath, os.path.basename(self._scanpath), 'R3D'))

        starttime = datetime.datetime.now()
        print(starttime)

        dbpath = os.path.join(os.path.expanduser('~'), 'Desktop', os.path.basename(self._scanpath) + '.db')
        self._initsqlitedb(dbpath)
        self._sqliteari(arilist, dbpath)

        self._sqliter3d(r3dlist, dbpath)

        endtime = datetime.datetime.now()
        print(endtime - starttime)


if __name__ == '__main__':
    testclass = generaterawdb()
    testclass._scanpath = r'/Volumes/work/TEST_Footage/~Footage'
    testclass.generatedb()