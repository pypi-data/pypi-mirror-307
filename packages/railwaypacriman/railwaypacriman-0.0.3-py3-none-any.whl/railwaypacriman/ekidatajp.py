#! /usr/bin/env python3

import pandas as pd
import railwaypacriman.logger as lggr
import os
import pkg_resources

#cur_dir = os.path.dirname(os.path.abspath(__file__))
#EKIDATA_DIR = os.path.join(cur_dir, "ekidatajp")

EKIDATA_DIR = pkg_resources.resource_filename('railwaypacriman', 'ekidatajp')


COMPANY_CSV_PATH = EKIDATA_DIR + "/company20240328.csv"
JOINT_CSV_PATH   = EKIDATA_DIR + "/join20240426.csv"
LINE_CSV_PATH    = EKIDATA_DIR + "/line20240426free.csv"
STATION_CSV_PATH = EKIDATA_DIR + "/station20240426free.csv"

CompanyData = pd.read_csv(COMPANY_CSV_PATH )
JoinData    = pd.read_csv(JOINT_CSV_PATH   )
LineData    = pd.read_csv(LINE_CSV_PATH    )
StationData = pd.read_csv(STATION_CSV_PATH )

if __name__=="__main__":
    pass
