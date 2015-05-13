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
        connect = sqlite3.connect(dbpath)
        try:
            cursor = connect.cursor()
            aricsv = os.path.join(self._temppath, os.path.basename(self._scanpath), 'ari', 'ArriExtractorOutput_0.csv')
            if os.path.exists(aricsv):
                with open(aricsv, 'r') as csvfile:
                    metadata = csv.reader(csvfile, delimiter=',')
                    for index, item in enumerate(metadata):
                        if index > 0:
                            cursor.execute('INSERT INTO RAWMETADATA (FULLPATH, MASTER_TC, REEL) VALUES (?, ?, ?)',
                                           (arilist[index - 1], item[1], item[2]))
                    cursor.close()
                    connect.commit()
        except:
            print('something error in sqlite database')

        finally:
            connect.close()


    def _symbolr3d(self, r3dlist):
        for index, item in enumerate(r3dlist):
            try:
                os.symlink(item,
                           os.path.join(self._temppath, os.path.basename(self._scanpath), 'ari', '%08d.ari' % index))
            finally:
                print('something error in ari symbol link')
        cmd = 'ARRIMetaExtract_CMD -i {0} -s \",\" -o {0}'.format(os.path.join(self._temppath, 'ari'))
        subprocess.call(cmd, shell=True)


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
                'OPERATIR TEXT,'
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
                'Sound_Roll TEXT'
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
        self._symbolari(arilist)
        self._sqliteari(arilist, dbpath)

        endtime = datetime.datetime.now()
        print(endtime - starttime)


if __name__ == '__main__':
    testclass = generaterawdb()
    testclass._scanpath = r'/Volumes/work/TEST_Footage/~Footage'
    testclass.generatedb()