#! /usr/bin/env python3

## RailwayPacriman
## Last-modified:2024/10/27 18:36:04.
## Author: Ippei KISHIDA
##
## st_cds   : station_cd list
## st_names : station names. E.g., 梅田

## DONE: ■ユーザデータのおきばしょを ~/.rp とかに書く？当面カレントディレクトリの使用で十分。
## DONE: バージョン番号の管理
## DONE: デバグ出力の整理
## DONE: company name 指定で正しい会社名じゃないときにエラーになるのを防ぐ。
## DONE: 線形表示のときに会社ソートして表示。
## TODO: JR函館本線が一筆書できないので描画できない問題。路線図を見て確認。 1110105 あたりにエラー？むりやり描かせたらよさそう。
## TODO: JR西日本 -c で描くと博多とか飛び地がある。wrong data?
## TODO: 駅データjp の有料データをユーザディレクトリに置けるように
## TODO: rpline, rpstation, rpadd を統合して rpinfo
## TODO: インストーラをつけて、コマンドとし使えるようにする。
## TODO: spacing が 0 とか、幅、高さの差が0のときの0除算対策

#__version__ = '0.1' # [2024-08-29] in progress

import sys
import graphviz
import pandas   as pd
import networkx as nx
import math
from   pathlib     import Path

import railwaypacriman.config as cfg
import railwaypacriman.logger as lggr
import railwaypacriman.ekidatajp as ekidata
from railwaypacriman.line import *
from railwaypacriman.progress import *

import argparse

def rpprogress():
    user_csv = './userdata.csv'

    ld = ekidata.LineData
    sd = ekidata.StationData
    jd = ekidata.JoinData

    parser = argparse.ArgumentParser(description=
            "rpprogress: RailwayPacriman makes a graph of progress."
            'When executed, this script needs "userdata.csv" in the current dir.')
    #parser.add_argument('user_csv', help='user data')
    #parser.add_argument('-a', '--all-line', help='all lines in Japan, taking long time.', action='store_true')
    parser.add_argument('-o', '--out-gv', help='output gv filename')
    parser.add_argument('-g', '--geological', help='geological plot of stations', action='store_true')
    parser.add_argument('-s', '--spacing', help='spacing latitude and longitude when -g option')
    parser.add_argument('-l', '--letter', help='number of letters for station')
    parser.add_argument('-c', '--company', help='company names instead of line name', action='store_true')
    parser.add_argument('--debug', help='verbose output for debug', action='store_true')
    parser.add_argument('-u', '--user-csv', help='indicate userdata.csv')
    parser.add_argument('lines', nargs='*', help='output lines')
    args = parser.parse_args()

    # デバッグモードの設定
    if args.debug:
        cfg.DEBUG_MODE = True

    if args.user_csv:
        user_csv = args.user_csv

    ## ユーザの記録を読み込み、各要素で繰り返し。
    progress = Progress()
    lggr.log("# Load user_csv")
    #ud = pd.read_csv(args.user_csv) ## ud: user data
    ud = pd.read_csv(user_csv) ## ud: user data

    ## データを元にして踏破データ処理
    for index, row in ud.iterrows():
        lggr.log("## " + row['date'])
        progress.proceed(
                row['date'],
                row['line_cd'],
                row['from_station_cd'],
                row['to_station_cd'],
                row['activity'],
                row['inout'])

    ## 描画
    lggr.log("# Draw progress")
    lggr.log("## Lines in history: ")
    for key in progress.lines.keys():
        lggr.log(progress.lines[key].line_name)

    lggr.log("## arguments for target: " + str(args.lines))
    tgt_line_cds = []
    #print(args.lines)
    if args.company:
        cd = ekidata.CompanyData
        company_cds = []
        if len(args.lines) == 0:
            print("--company option needs at least one company name. Exit.")
            sys.exit()
            #for i in list(progress.lines):
            #    company_cds.append(int(ld.loc[ld['line_cd'] == i, 'company_cd'].values[0]))
        else:
            company_cds = []
            for i in args.lines:
                tmp = cd[cd['company_name'].str.contains(i)]
                if len(tmp) == 0:
                    print("Not found: " + str(args.lines))
                    sys.exit()
                for index, row in tmp.iterrows():
                    company_cds.append(row['company_cd'])
        company_cds = list(set(company_cds)) ##uniq
        for c in company_cds:
            tgt_line_cds += list(ld.loc[ld['company_cd'] == c, 'line_cd'])
    else:
        if len(args.lines) == 0:
            tgt_line_cds = list(progress.lines)
        elif '*' in args.lines:
            tgt_line_cds = ld['line_cd'].to_list()
        else:
            for i in args.lines:
                tmp = ld[ld['line_name'].str.contains(i)]
                for index, row in tmp.iterrows():
                    tgt_line_cds.append(row['line_cd'])

    lggr.log("## target candidates with string: " )
    if args.out_gv:
        output_file = args.out_gv
    else:
        output_file = 'rpprogress.gv'

    lggr.log("# Draw graph")
    data = {'outfile': output_file,
            'tgt_line_cds': tgt_line_cds,
            'geological': args.geological,
            }
    if args.spacing:
        #data['spacing'] = int(args.spacing)
        data['spacing'] = float(args.spacing)
        #print(data['spacing'])
    if args.letter:
        data['num_letter'] = int(args.letter)
    #print(data); sys.exit()
    progress.draw_graph(** data)

if __name__=="__main__":
    rpprogress()
