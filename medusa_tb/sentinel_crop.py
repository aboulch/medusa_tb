"""
Medusa ToolBox.
Copyright (C) 2017 ONERA, Alexandre Boulch
This program is free software; you can redistribute it
and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation;
either version 3 of the License, or any later version.
This program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public
License along with this program; if not, write to the Free
Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
Boston, MA 02110-1301  USA
"""

import numpy as np
import json
import argparse
from zipfile import ZipFile
import shutil
import os
import subprocess

def sentinel1_process(args, zf, mini, maxi):

    print("searching for jp2 files")
    filelist = zf.namelist()
    for fname in filelist:
        if("measurement" in fname and ".tiff" in fname):
            print(fname)
            root_fname = fname.split("/")[-1].split(".")[0]
            infile = os.path.join("tmp",fname)
            outfile = os.path.join(args.dest, root_fname+".tif")
            cmd = ['/usr/bin/gdalwarp', "-t_srs", "EPSG:4326", "-te", str(mini[0]), str(mini[1]), str(maxi[0]), str(maxi[1]), infile, outfile]
            subprocess.call(cmd)

    # pass

def sentinel2_process(args, zf, mini, maxi):

    print("searching for jp2 files")
    filelist = zf.namelist()
    for fname in filelist:
        if("GRANULE" in fname and "IMG_DATA" in fname and ".jp2" in fname):
            print(fname)
            root_fname = fname.split("/")[-1].split(".")[0]
            infile = os.path.join("tmp",fname)
            outfile = os.path.join(args.dest, root_fname+".tif")
            # cmd = ['gdalwarp', "-t_srs", "EPSG:4326", "-te", str(mini[0]), str(mini[1]), str(maxi[0]), str(maxi[1]), "-ts", "1024", "1024", infile, outfile]
            cmd = ['/usr/bin/gdalwarp', "-t_srs", "EPSG:4326", "-te", str(mini[0]), str(mini[1]), str(maxi[0]), str(maxi[1]), infile, outfile]
            subprocess.call(cmd)


def main():
    parser = argparse.ArgumentParser(description='PyTorch sentinel crop')
    parser.add_argument('--sentinel', type=int, default=1, metavar='N',
                        help='1 for sentinel1 and 2 for sentinel 2')
    parser.add_argument('--archive', type=str, default="archive", metavar='N',
                        help='archive of sentinel')
    parser.add_argument('--geojson', type=str, default="map.geojson", metavar='N', help="footprint")
    parser.add_argument('--dest', type=str, default="crop_results", metavar='N', help="distination folder")
    args = parser.parse_args()


    print("loading footprint...")
    footprint = json.load(open(args.geojson))
    coordinates = np.array(footprint["features"][0]["geometry"]["coordinates"][0])
    mini = coordinates.min(axis=0)
    maxi = coordinates.max(axis=0)

    print("removing temp directory and creating destination...")
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")
    if not os.path.exists(args.dest):
        os.makedirs(args.dest)

    print("extracting the dataset to temp directory...")
    zf = ZipFile(args.archive, 'r')
    zf.extractall("tmp")

    print("Entering image function...")
    if args.sentinel == 1:
        print("SENITNEL1")
        sentinel1_process(args, zf, mini, maxi)
    elif args.sentinel == 2:
        print("SENTINEL2")
        sentinel2_process(args, zf, mini, maxi)

    print("removing tmp files")
    shutil.rmtree("tmp")

if __name__ == "__main__":
    main()
