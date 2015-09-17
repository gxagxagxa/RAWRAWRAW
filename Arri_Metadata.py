#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import struct
import re
import collections
import os


class Arri_Metadata(object):
    def __init__(self):
        super(Arri_Metadata, self).__init__()
        self.header = collections.OrderedDict()
        # self.header = {'Master_TC': '00:00:00:00',
        #                'Reel': '--',
        #                'Scene': '',
        #                'Take': '',
        #                'Director': '',
        #                'Cinematographer': '',
        #                'Production': '',
        #                'Circle_Take': '',
        #                'Production_Company': '',
        #                'Location': '',
        #                'Operator': '',
        #                'User_Info_1': '',
        #                'User_Info_2': '',
        #                'Camera_Clip_Name': '',
        #                'Camera_Family': '',
        #                'Camera_Serial_Number': '',
        #                'Camera_ID': '',
        #                'Camera_Index': '',
        #                'Camera_SUP_Name': '',
        #                'Camera_Model': '',
        #                'Camera_Product': '',
        #                'Camera_SubProduct': '',
        #                'System_Image_Creation_Date': '',
        #                'System_Image_Creation_Time': '',
        #                'Exposure_Time': '',
        #                'Shutter_Angle': '',
        #                'Mirror_Shutter_Running': '',
        #                'Sensor_FPS': '',
        #                'Project_FPS': '',
        #                'Master_TC_Time_Base': '',
        #                'Master_TC_Frame_Count': '',
        #                'Master_TC_User_Info': '',
        #                'Storage_Media_Serial_Number': '',
        #                'SMPTE_UMID': '',
        #                'Recorder_Type': '',
        #                'Vari': '',
        #                'UUID': '',
        #                'Image_Width': '',
        #                'Image_Height': '',
        #                'Active_Image_Width': '',
        #                'Active_Image_Height': '',
        #                'Active_Image_Top': '',
        #                'Active_Image_Left': '',
        #                'Full_Image_Width': '',
        #                'Full_Image_Height': '',
        #                'Color_Processing_Version': '',
        #                'White_Balance': '',
        #                'White_Balance_CC': '',
        #                'WB_Factor_R': '',
        #                'WB_Factor_G': '',
        #                'WB_Factor_B': '',
        #                'WB_Applied_In_Camera': '',
        #                'Exposure_Index_ASA': '',
        #                'Target_Color_Space': '',
        #                'Sharpness': '',
        #                'Lens_Squeeze': '',
        #                'Image_Orientation': '',
        #                'Look': '',
        #                'Look_Burned_In': '',
        #                'Look_LUT_Mode': '',
        #                'Look_LUT_Offset': '',
        #                'Look_LUT_Size': '',
        #                'Look_Saturation': '',
        #                'CDL_Slope_R': '',
        #                'CDL_Slope_G': '',
        #                'CDL_Slope_B': '',
        #                'CDL_Offset_R': '',
        #                'CDL_Offset_G': '',
        #                'CDL_Offset_B': '',
        #                'CDL_Power_R': '',
        #                'CDL_Power_G': '',
        #                'CDL_Power_B': '',
        #                'Printer_Lights_R': '',
        #                'Printer_Lights_G': '',
        #                'Printer_Lights_B': '',
        #                'CDL_Mode': '',
        #                'Lens_Model': '',
        #                'Lens_Serial_Number': '',
        #                'Lens_Distance_Unit': '',
        #                'Lens_Focus_Distance': '',
        #                'Lens_Focal_Length': '',
        #                'Lens_Iris': '',
        #                'Lens_Linear_Iris': '',
        #                'RawEncoderFocus_RawLds': '',
        #                'RawEncoderFocus_RawMotor': '',
        #                'RawEncoderFocal_RawLds': '',
        #                'RawEncoderFocal_RawMotor': '',
        #                'RawEncoderIris_RawLds': '',
        #                'RawEncoderIris_RawMotor': '',
        #                'EncoderLimFocusLdsMin': '',
        #                'EncoderLimFocusLdsMax': '',
        #                'EncoderLimFocusMotorMin': '',
        #                'EncoderLimFocusMotorMax': '',
        #                'EncoderLimFocalLdsMin': '',
        #                'EncoderLimFocalLdsMax': '',
        #                'EncoderLimFocalMotorMin': '',
        #                'EncoderLimFocalMotorMax': '',
        #                'EncoderLimIrisLdsMin': '',
        #                'EncoderLimIrisLdsMax': '',
        #                'EncoderLimIrisMotorMin': '',
        #                'EncoderLimIrisMotorMax': '',
        #                'Lds_Lag_Type': '',
        #                'Lds_Lag_Value': '',
        #                'ND_Filter_Type': '',
        #                'ND_Filter_Density': '',
        #                'Camera_Tilt': '',
        #                'Camera_Roll': '',
        #                'Master_Slave_Setup_Info': '',
        #                'S3D_Eye_Info': '',
        #                'Sound_Roll': '',
        #                'RAWTYPE': 'ari',
        #                'END_TC': '00:00:00:00',
        #                'FULL_PATH': '--'
        #                }

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
        with open(path, 'rb') as file:
            file.seek(0)
            arristruct = struct.unpack('<4s 3I'  # RootInformation
                                       'I I I I I 4I 4I I I 8s'  # ImageDataInformation
                                       'I I I 4f I I I I 12f f f I I I f I 32s I I I I f 3f 3f 3f 3f I I I I 32s'  # ImageContentInformation
                                       'I I I I I 4s 4s 8B 4B I I I I I I I I '
                                       '4B I I I I 43I 8B 12s'
                                       '32B 8s 32s I I I 16B 24s 20s H H 96s'  # CameraDeviceInformation
                                       'I I I I I I 2H I I I 32s 2H 2H 2H 2H 2H 2H 2H 2H 2H '
                                       'B B B B 88s'  # LensDataInformation
                                       'I 2I 2I I I I 2h 2h 2h I I I 128s'  # VfxInformation
                                       'I I 8s 16s 8s 32s 32s 32s 32s 256s 24s 104s'  # ClipInformation
                                       'I 4I 32s 32s 32s 32s 32s I I 32s'  # SoundInformation
                                       'I I I I I I I I I I I 40s'  # CameraInformation
                                       'I I 32s 32s '
                                       'I 32s H H H H H H '
                                       'I 32s H H H H H H '
                                       'I 32s H H H H H H '
                                       'I 32s H H H H H H '
                                       'I 32s H H H H H H '
                                       'I 32s H H H H H H '
                                       '32s'  # FramelineInformation
                                       'I 512s 1068s'  # ARRIReserved
                                       , file.read(4096))

            # print(arristruct)
            self.header['FULL_PATH'] = path
            self.header['Image_Width'] = arristruct[5]
            self.header['Image_Height'] = arristruct[6]
            self.header['Active_Image_Left'] = arristruct[9]
            self.header['Active_Image_Top'] = arristruct[10]
            self.header['Active_Image_Width'] = arristruct[11]
            self.header['Active_Image_Height'] = arristruct[12]
            self.header['Full_Image_Width'] = arristruct[15]
            self.header['Full_Image_Height'] = arristruct[16]

            self.header['White_Balance'] = arristruct[22]
            self.header['White_Balance_CC'] = arristruct[23]
            self.header['WB_Factor_R'] = arristruct[24]
            self.header['WB_Factor_G'] = arristruct[25]
            self.header['WB_Factor_B'] = arristruct[26]

            WBAppliedInCameraFlag = ('NO', 'YES')
            self.header['WB_Applied_In_Camera'] = WBAppliedInCameraFlag[arristruct[27]]

            self.header['Exposure_Index_ASA'] = arristruct[28]

            TargetColorSpace = ('REC 709', 'ITU P3', 'LogC-WideGamut', 'LogC-ArriFilmColor')
            self.header['Target_Color_Space'] = TargetColorSpace[arristruct[46]]

            self.header['Sharpness'] = arristruct[47]
            self.header['Lens_Squeeze'] = arristruct[48]

            Flip = ('No flip', 'H flip', 'V flip', 'H+V flip')
            self.header['Image_Orientation'] = Flip[arristruct[49]]

            self.header['Look'] = re.sub('\W', '', arristruct[50])

            LookLutMode = ('No Look LUT', 'Monochromatic Look LUT')
            self.header['Look_LUT_Mode'] = LookLutMode[arristruct[51]]
            self.header['Look_LUT_Offset'] = arristruct[52]
            self.header['Look_LUT_Size'] = arristruct[53]
            self.header['Look_Saturation'] = arristruct[55]

            self.header['CDL_Slope_R'] = arristruct[56]
            self.header['CDL_Slope_G'] = arristruct[57]
            self.header['CDL_Slope_B'] = arristruct[58]
            self.header['CDL_Offset_R'] = arristruct[59]
            self.header['CDL_Offset_G'] = arristruct[60]
            self.header['CDL_Offset_B'] = arristruct[61]
            self.header['CDL_Power_R'] = arristruct[62]
            self.header['CDL_Power_G'] = arristruct[63]
            self.header['CDL_Power_B'] = arristruct[64]
            self.header['Printer_Lights_R'] = arristruct[65]
            self.header['Printer_Lights_G'] = arristruct[66]
            self.header['Printer_Lights_B'] = arristruct[67]

            #TODO: this will out of range sometimes?
            # CdlApplicationMode = ('ARRI_LOOK_NONE', 'ARRI_LOOK_ALEXA_VIDEO', 'ARRI_LOOK_CDL_VIDEO', 'ARRI_LOOK_CDL_LOGC')
            # print(arristruct[68])
            # self.header['CDL_Mode'] = CdlApplicationMode[arristruct[68]]

            CameraTypeID = ('none', 'D21', 'ALEXA', 'ALEXA_65')
            self.header['Camera_Family'] = CameraTypeID[arristruct[74]]

            self.header['Camera_SUP_Name'] = arristruct[76]
            self.header['Camera_Serial_Number'] = arristruct[77]
            self.header['Camera_ID'] = arristruct[78]
            self.header['Camera_Index'] = re.sub('\W', '', arristruct[79])

            self.header['System_Image_Creation_Date'] = '%02x' % arristruct[83] + '%02x' % arristruct[82] + \
                                                        '-' + '%02x' % arristruct[81] + '-' + '%02x' % arristruct[80]
            self.header['System_Image_Creation_Time'] = '%02x' % arristruct[87] + ':' + '%02x' % arristruct[86] + \
                                                        ':' + '%02x' % arristruct[85] + ':' + '%02x' % arristruct[84]
            self.header['ExposureTime'] = str(arristruct[93] / 1000.0) + ' ms'
            self.header['Shutter_Angle'] = arristruct[94] / 1000.0
            self.header['Sensor_FPS'] = arristruct[98] / 1000.0
            self.header['Project_FPS'] = arristruct[99] / 1000.0

            self.header['Master_TC'] = '%02x' % arristruct[103] + ':' + '%02x' % arristruct[102] + \
                                                        ':' + '%02x' % arristruct[101] + ':' + '%02x' % arristruct[100]
            self.header['Master_TC_Frame_Count'] = arristruct[104]
            self.header['Master_TC_Time_Base'] = arristruct[105] / 1000.0
            self.header['Master_TC_User_Info'] = arristruct[108]

            self.header['Storage_Media_Serial_Number'] = ''.join(['%02x' % kk for kk in arristruct[158:150:-1]])
            self.header['SMPTE_UMID'] = ''.join(['%02x' % kk for kk in arristruct[160:191:1]]).upper()
            self.header['Camera_Family'] = re.sub('\\x00', '', arristruct[192])
            self.header['Recorder_Type'] = re.sub('\\x00', '', arristruct[193])
            MirrorShutterRunning = ('NO', 'YES')
            self.header['Mirror_Shutter_Running'] = MirrorShutterRunning[arristruct[194]]

            self.header['UUID'] = ''.join(['%02x' % kk for kk in arristruct[197:212:1]]).upper()
            self.header['Camera_SUP_Name'] = re.sub('\\x00', '', arristruct[213])
            self.header['Camera_Model'] = re.sub('\\x00', '', arristruct[214])

            FocusUnit = ('Feet', 'Meter')
            self.header['Lens_Distance_Unit'] = FocusUnit[arristruct[219]]
            self.header['Lens_Focus_Distance'] = arristruct[220]
            self.header['Lens_Focal_Length'] = arristruct[221]
            self.header['Lens_Serial_Number'] = arristruct[222]
            self.header['Lens_Linear_Iris'] = arristruct[223]
            self.header['Lens_Iris'] = 'T %.2f' % (2**(((arristruct[223]/1000.0)-1)/2))

            NdFilterType = ('No Filter', 'ALEXA Studio ND Type 1')
            self.header['ND_Filter_Type'] = NdFilterType[arristruct[224]]
            self.header['ND_Filter_Density'] = arristruct[225]
            self.header['Lens_Model'] = re.sub('\\x00', '', arristruct[229])

            self.header['RawEncoderFocus_RawLds'] = arristruct[230]
            self.header['RawEncoderFocus_RawMotor'] = arristruct[231]
            self.header['RawEncoderFocal_RawLds'] = arristruct[232]
            self.header['RawEncoderFocal_RawMotor'] = arristruct[233]
            self.header['RawEncoderIris_RawLds'] = arristruct[234]
            self.header['RawEncoderIris_RawMotor'] = arristruct[235]
            self.header['EncoderLimFocusLdsMin'] = arristruct[236]
            self.header['EncoderLimFocusLdsMax'] = arristruct[237]
            self.header['EncoderLimFocalLdsMin'] = arristruct[238]
            self.header['EncoderLimFocalLdsMax'] = arristruct[239]
            self.header['EncoderLimIrisLdsMin'] = arristruct[240]
            self.header['EncoderLimIrisLdsMax'] = arristruct[241]
            self.header['EncoderLimFocusMotorMin'] = arristruct[242]
            self.header['EncoderLimFocusMotorMax'] = arristruct[243]
            self.header['EncoderLimFocalMotorMin'] = arristruct[244]
            self.header['EncoderLimFocalMotorMax'] = arristruct[245]
            self.header['EncoderLimIrisMotorMin'] = arristruct[246]
            self.header['EncoderLimIrisMotorMax'] = arristruct[247]
            self.header['Lds_Lag_Type'] = arristruct[248]
            self.header['Lds_Lag_Value'] = arristruct[249]

            self.header['Camera_X'] = arristruct[258]
            self.header['Camera_Y'] = arristruct[259]
            self.header['Camera_Z'] = arristruct[260]
            self.header['Camera_Pan'] = arristruct[261] / 10.0
            self.header['Camera_Tilt'] = arristruct[263] / 10.0
            self.header['Camera_Roll'] = arristruct[265] / 10.0

            MasterFlag = ('Independent', 'Master', 'Slave')
            self.header['Master_Slave_Setup_Info'] = MasterFlag[arristruct[267]]
            ChannelInfo = ('Single', 'Left Eye', 'Right Eye', 'Multi Eye')
            self.header['S3D_Eye_Info'] = ChannelInfo[arristruct[268]]

            self.header['Circle_Take'] = arristruct[272]
            self.header['Reel'] = re.sub('\\x00', '', arristruct[273])
            self.header['Scene'] = re.sub('\\x00', '', arristruct[274])
            self.header['Take'] = re.sub('\\x00', '', arristruct[275])
            self.header['Director'] = re.sub('\\x00', '', arristruct[276])
            self.header['Cinematographer'] = re.sub('\\x00', '', arristruct[277])
            self.header['Production'] = re.sub('\\x00', '', arristruct[278])
            self.header['Production_Company'] = re.sub('\\x00', '', arristruct[279])
            self.header['Notes'] = re.sub('\\x00', '', arristruct[280])
            self.header['Camera_Clip_Name'] = re.sub('\\x00', '', arristruct[281])

            self.header['Sound_File_Name'] = re.sub('\\x00', '', arristruct[288])
            self.header['Sound_Roll'] = re.sub('\\x00', '', arristruct[289])
            self.header['Audio_Scene_Name'] = re.sub('\\x00', '', arristruct[290])
            self.header['Audio_Take_Name'] = re.sub('\\x00', '', arristruct[291])
            self.header['Audio_Info'] = re.sub('\\x00', '', arristruct[292])
            self.header['Audio_ Data_Offset'] = arristruct[293]

            self.header['END_TC'] = self.__timecodeadd(self.header['Master_TC'], '00:00:00:01', self.header['Sensor_FPS'])

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
    testmetadata = Arri_Metadata()
    myheader = testmetadata.metadata('/Users/mac/Desktop/meta/A003C028_140924_R6QB.0403757.ari')
    # testmetadata.metadata('/Volumes/VIP_DATA/TEST_Footage/Alexa/XT/A001C001_140207_R3HU.1178954.ari')
    # testmetadata.metadata('/Users/andyguo/Desktop/untitled folder/A008C003_150320_R0DA.0000123.ari')
    print(testmetadata.csvString())
