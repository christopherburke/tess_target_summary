#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 09:58:28 2022

@author: cjburke
"""

import urllib.request as req
import os
import numpy as np

# storage class for target data
class target_data:
    def __init__(self):
        self.tic = 0
        self.nSec = 0
        self.sectorList = []
        self.nSec20 = 0
        self.sectorList20 = []
        self.ra = 0.0
        self.dec = 0.0
        self.tmag = 0.0


if __name__ == '__main__':
    urlPath = 'https://tess.mit.edu/wp-content/uploads'
    filePrefix2Min = 'all_targets_S'
    filePrefix20Sec = 'all_targets_20s_S'
    filePostfix = '_v1.txt'
    outputFile = 'tess_target_list_summary.txt'

    target_data_dict = {}
    # Read in 2 minute target tables
    errorcount = 0
    for iSec in range(1,1000):
        url2Min = os.path.join(urlPath,filePrefix2Min+'{0:03d}'.format(iSec)+filePostfix)
        print('Reading Sector {0:d} 2min target table'.format(iSec))
        #print(url2Min)
        try:
            reqData = req.urlopen(url2Min)
            with reqData as f:
                dataList = f.read().decode('utf-8').splitlines()
                print('{0:d} lines received'.format(len(dataList)))
                nLines = len(dataList)
                for i in range(nLines):
                    ln = dataList[i]
                    if not ln[0] == '#':
                        splitln = ln.split()
                        curtic = int(splitln[0])
                        if curtic in target_data_dict:
                            # tic already in dict extend the dictionary
                            target_data_dict[curtic].nSec = target_data_dict[curtic].nSec + 1
                            target_data_dict[curtic].sectorList.append(iSec)
                        else:
                            # new tic
                            newData = target_data()
                            newData.tic = curtic
                            newData.nSec = 1
                            newData.sectorList = [iSec]
                            newData.ra = float(splitln[4])
                            newData.dec = float(splitln[5])
                            newData.tmag = float(splitln[3])
                            target_data_dict[curtic] = newData
            #print('Found {0:d} unique targets'.format(len(target_data_dict)))
            errorcount = 0
        except:
            errorcount = errorcount + 1
            #print('Error when trying to read sector {0:d} 2min target list'.format(iSec))
            if errorcount > 1:
                break
        
    # Read in 20 second target tables
    for iSec in range(27,1000):
        url2Min = os.path.join(urlPath,filePrefix20Sec+'{0:03d}'.format(iSec)+filePostfix)
        #print(url2Min)
        print('Reading Sector {0:d} 20 sec target table'.format(iSec))
        try:
            reqData = req.urlopen(url2Min)
            with reqData as f:
                dataList = f.read().decode('utf-8').splitlines()
                print('{0:d} lines received'.format(len(dataList)))
                nLines = len(dataList)
                for i in range(nLines):
                    ln = dataList[i]
                    if not ln[0] == '#':
                        splitln = ln.split()
                        curtic = int(splitln[0])
                        if curtic in target_data_dict:
                            # tic already in dict extend the dictionary
                            target_data_dict[curtic].nSec20 = target_data_dict[curtic].nSec20 + 1
                            target_data_dict[curtic].sectorList20.append(iSec)
                        else:
                            # new tic
                            newData = target_data()
                            newData.tic = curtic
                            newData.nSec = 1
                            newData.sectorList = [iSec]
                            newData.ra = float(splitln[4])
                            newData.dec = float(splitln[5])
                            newData.tmag = float(splitln[3])
                            target_data_dict[curtic] = newData
            #print('Found {0:d} unique targets'.format(len(target_data_dict)))
            errorcount = 0
        except:
            errorcount = errorcount + 1
            #print('Error when trying to read sector {0:d} 20 sec target list'.format(iSec))
            if errorcount > 1:
                break
        
    # open output
    fo = open(outputFile, 'w')
    fo.write('# TIC RA Dec Tmag NSectors Nsectors_20Sec SecList2Min SecList20Sec\n')
    # Now sort the tics and print them out
    all_tics = np.sort([x for x in target_data_dict.keys()])
    for curtic in all_tics:
        cD = target_data_dict[curtic]
        slist2mstr = ','.join([str(x) for x in cD.sectorList])
        slist2sstr = ','.join([str(x) for x in cD.sectorList20])
        fo.write('{0:d} | {1:10.6f} | {2:10.6f} | {3:6.3f} | {4:d} | {5:d} | {6} | {7}\n'.format(cD.tic, \
                 cD.ra, cD.dec, cD.tmag, cD.nSec,\
                 cD.nSec20, slist2mstr, slist2sstr)  )
        
    fo.close()
    