#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'


import sqlite3
import EDL

class CONFORM(object):

    def __init__(self):
        pass


    def conform(self,
                EDLobject,
                dbobjects,
                matchreel=True,
                EDLusingreel='reel'):

        for db in dbobjects:

            connect = sqlite3.connect(db)
            cursor = connect.cursor()

            for clip in EDLobject._edlclip:
                cmd = 'SELECT * FROM RAWMETADATA ' \
                      'WHERE ' \
                      '(MASTER_TC >= \"%s\" AND END_TC <= \"%s\" AND ' \
                      '(RAWTYPE = \"ari\" OR RAWTYPE = \"exr\" OR RAWTYPE = \"dng\" OR RAWTYPE = \"dpx\")) OR ' \
                      '(MASTER_TC <= \"%s\" AND END_TC >= \"%s\" AND ' \
                      '(RAWTYPE = \"mov\" OR RAWTYPE = \"mp4\" OR RAWTYPE = \"cine\" OR RAWTYPE = \"r3d\" OR RAWTYPE = \"mxf\"))' % \
                      (clip['sourcein'], clip['sourceout'], clip['sourcein'], clip['sourceout'])
                print(cmd)

                cursor.execute(cmd)
                matchedframes = cursor.fetchall()
                print(matchedframes)












if __name__ == '__main__':
    edlobject = EDL.EDL()
    edlobject.readedl('/Users/andyguo/Desktop/Sequence 1.edl')

    conformobject = CONFORM()
    conformobject.conform(edlobject, ['/Users/andyguo/Desktop/FOOTAGE.db', ])