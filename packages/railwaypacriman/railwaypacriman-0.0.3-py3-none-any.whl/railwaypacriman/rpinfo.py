#! /usr/bin/env python3

import sys
#import ekidatajp
import pandas as pd
import argparse
import datetime
#from . import ekidatajp
import railwaypacriman.ekidatajp as ekidata
#from . import logger
import railwaypacriman.logger as lggr

## argument analysis
parser = argparse.ArgumentParser(description= 'rpline: RailwayPacriman Line')
parser.add_argument('-l', '--line-cd', help='indicate line_cd instead name.', action='store_true')
parser.add_argument('line_name')
parser.add_argument('from_station', nargs='?')
parser.add_argument('to_station', nargs='?')
parser.add_argument('-d', '--date', help='Set date')
parser.add_argument('-b', '--bike', help='Bike instead of run as activity.', action='store_true')
parser.add_argument('--inout', help='inner or outer in loop line.')
parser.add_argument('-n', '--note', help='Take note.')
parser.add_argument('-q', '--quiet', help='Quiet output except summary.', action='store_true')
args = parser.parse_args()

ld = ekidata.LineData #ld: line data
sd = ekidata.StationData #sd: station data 
#ld = railwaypacriman.ekidatajp.LineData #ld: line data
#sd = railwaypacriman.ekidatajp.StationData #sd: station data 
#ld = ekidatajp.LineData #ld: line data
#sd = ekidatajp.StationData #sd: station data 

def print_when_verbose(string):
    if args.quiet:
        return
    else:
        print(string)

def print_line_station_list(dataframe):
    for index, row in dataframe.iterrows():
        sc = row['station_cd']
        sn = sd.loc[sd['station_cd'] == sc, 'station_name'].values[0]
        lc = row['line_cd']
        ln = ld.loc[ld['line_cd'] == lc, 'line_name'].values[0]
        print_when_verbose('- ({}){:<20}({}){}'.format(lc, ln, sc, sn))

def rpinfo():
    ##lines: filtered_lines
    if args.line_name is not None: #No meaning but structure
        ln = args.line_name #ln: line_name
        if args.line_cd:
            lines = ld.loc[ld['line_cd'] == int(args.line_name) ]
        else:
            lines = ld[ld['line_name'].str.contains(ln, regex=False)]
        print_when_verbose("# Line candidates")
        for index, row in lines.iterrows():
            lc = row['line_cd']
            print_when_verbose('- ({}) {:<20}'.format(lc, ld.loc[ld['line_cd'] == lc, 'line_name'].values[0]))

    #if args.to_station is None:
    if len(lines) <= 1:
        for index, row in sd.loc[sd['line_cd'] == lc].iterrows():
            print_when_verbose('    - ({}) {}'.format(row['station_cd'], row['station_name']))

    if args.from_station is not None:
        print_when_verbose("\n# From-Station candidates")
        fss = (sd.loc[sd['station_name'].str.contains(args.from_station), ['line_cd', 'station_cd', 'station_name']])
        print_line_station_list(fss)
        fs_lines = fss['line_cd']
        fs_cds = fss['station_cd']

        ## filter
        if list(fs_lines):
            lines = lines[lines['line_cd'].isin(fs_lines)]
        else:
            lines = lines.DataFrame()

    if args.to_station is not None:
        print_when_verbose("\n# To-Station candidates")
        tss = (sd.loc[sd['station_name'].str.contains(args.to_station), ['line_cd', 'station_cd', 'station_name']])
        print_line_station_list(tss)
        ts_lines = tss['line_cd']
        ts_cds = tss['station_cd']

        ## filter
        if list(ts_lines):
            lines = lines[lines['line_cd'].isin(ts_lines)]
        else:
            lines = lines.Datatrame()
    else:
        sys.exit()

    print_when_verbose("\n# Summary")
    if args.date:
        date = args.date
    else:
        date = datetime.datetime.now().date()

    if args.bike:
        activity = "bike"
    else:
        activity = "run"

    note = args.note or ""

    for index, row in lines.iterrows():
        lc = row['line_cd'] #34007
        ln = row['line_name'] #阪急箕面線
        sc1 = fss.loc[fss['line_cd'] == lc, 'station_cd'].values[0]
        sn1 = fss.loc[fss['line_cd'] == lc, 'station_name'].values[0]
        sc2 = tss.loc[tss['line_cd'] == lc, 'station_cd'].values[0]
        sn2 = tss.loc[tss['line_cd'] == lc, 'station_name'].values[0]

        ## loop line であるとき
        loop_line_cd_list = [11623] # 11623 大阪環状線
        if lc in loop_line_cd_list: 
            if not args.inout: #指定されていなければ
                print("--in-out option is required. E.g. --in-out=in")
                sys.exit()
            else:
                inout = args.inout
        else:
            inout = ''

        out_str = "{},{},{},{},{},{},{},{},{},{}".format(date, lc, sc1, sc2, ln, sn1, sn2, activity, inout, note)
        print(out_str)


if __name__=="__main__":
    rpinfo()
