#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'


import sqlite3
import EDL
import os


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

            try:
                for clip in EDLobject._edlclip:
                    cmd = 'SELECT * FROM RAWMETADATA ' \
                          'WHERE ' \
                          '(MASTER_TC >= \"%s\" AND END_TC <= \"%s\" AND ' \
                          '(RAWTYPE = \"ari\" OR RAWTYPE = \"exr\" OR RAWTYPE = \"dng\" OR RAWTYPE = \"dpx\")) OR ' \
                          '(MASTER_TC <= \"%s\" AND END_TC >= \"%s\" AND ' \
                          '(RAWTYPE = \"mov\" OR RAWTYPE = \"mp4\" OR RAWTYPE = \"cine\" OR RAWTYPE = \"r3d\" OR RAWTYPE = \"mxf\"))' % \
                          (clip['sourcein'], clip['sourceout'], clip['sourcein'], clip['sourceout'])
                    if matchreel:
                        if EDLusingreel == 'reel':
                            cmd += ' AND (REEL LIKE "%s")' % (clip['reel'])
                        if EDLusingreel == 'clipanme':
                            cmd += ' AND (REEL LIKE "%s")' % (clip['clipname'])
                        if EDLusingreel == 'longreel':
                            cmd += ' AND (REEL LIKE "%s")' % (clip['longreel'])

                    # print(cmd)

                    cursor.execute(cmd)
                    matchedframes = cursor.fetchall()
                    # print(matchedframes)
                    clip['matched'] = matchedframes


            except:
                print('something error in conform')
            finally:
                connect.close()



    def savecopylist(self, EDLobject, savepath):
        with open(savepath, 'w') as f:
            for index, clip in enumerate(EDLobject._edlclip):

                if len(clip['matched']) > 0:
                    for linestring in clip['matched']:
                        # linestring = clip['matched'][0][0]
                        print(linestring)
                        f.write(linestring[0]+os.linesep)










if __name__ == '__main__':
    edlobject = EDL.EDL()
    edlobject.readedl('/Users/andyguo/Desktop/Sequence 1.edl')

    conformobject = CONFORM()
    conformobject.conform(edlobject, ['/Users/andyguo/Desktop/FOOTAGE.db', ], EDLusingreel='longreel')
    # print(edlobject._edlclip)
    conformobject.savecopylist(edlobject, '/Users/andyguo/Desktop/save.txt')