#! /usr/bin/env python3

## module Line, indicating rail line.
## Last-modified:2024/10/26 03:03:08.
## Author: Ippei KISHIDA

from   collections import defaultdict
import networkx as nx
import unittest
import sys

import railwaypacriman.ekidatajp as ekidata
import railwaypacriman.logger as lggr
from railwaypacriman.join import *

ld = ekidata.LineData
sd = ekidata.StationData
jd = ekidata.JoinData

class Line:
    # ld: line data from ekidata.jp
    def __init__(self, line_cd):
        #self.line_cd = line_cd

        data = ld.loc[ld['line_cd'] == line_cd]
        #print(data)
        self.line_cd      = int(data['line_cd'].values[0])
        self.company_cd   = int(data['company_cd'].values[0])
        self.line_name    = str(data['line_name'].values[0])
        self.line_name_k  = str(data['line_name_k'].values[0])
        self.line_name_h  = str(data['line_name_h'].values[0])
        self.line_color_c = str(data['line_color_c'].values[0])
        self.line_color_t = str(data['line_color_t'].values[0])
        self.line_type    = str(data['line_type'].values[0])
        self.lon          = float(data['lon'].values[0])
        self.lat          = float(data['lat'].values[0])
        self.zoom         = int(data['zoom'].values[0])
        self.e_status     = int(data['e_status'].values[0])
        self.e_sort       = int(data['e_sort'].values[0])

        #TODO: self.name -> self.line_name
        self.line_name = str(ld.loc[ld['line_cd'] == line_cd, 'line_name'].values[0])

        counts = defaultdict(int)

        ## Generate node list with order of rank in graph
        join_lst = jd.loc[jd['line_cd'] == line_cd, ['station_cd1', 'station_cd2']].values.tolist()
        try:
            G = nx.Graph()
            G.add_edges_from(join_lst)
            edges = list(nx.eulerian_path(G))
        except nx.exception.NetworkXError:
            print("No Eulerian path:" + self.line_name)
            #print(join_lst)
            edges = join_lst
        except nx.exception.NetworkXPointlessConcept :
            print("Error: networkx.exception.NetworkXPointlessConcept. skip.")
            #JR北陸本線のばあい、たぶん join にデータがない。新幹線扱い？
            edges = []

        self.st_cds = []
        self.joins = {}

        for u, v in edges:
            ## make a list of st_cds
            if not self.st_cds:
                self.st_cds.append(u)
            self.st_cds.append(v)

            idx0 = [idx for idx, value in enumerate( self.st_cds ) if value == u]
            idx1 = [idx for idx, value in enumerate( self.st_cds ) if value == v]
            #print(idx0[0], idx1[0])
            self.joins[(idx0[0], idx1[0])] = Join()

        ## For loop line
        if self.st_cds[0] == self.st_cds[-1]:
            self.st_cds.pop()

        self.st_names = [str(sd.loc[sd['station_cd'] == x, 'station_name'].values[0]) for x in self.st_cds]
        #self.arrows = []

        if self.line_name == False:
            print(line_cd + " is not found in line.yaml")
            sys.exit()

    def __str__(self): # print() に放り込んだときに表示される文字列
        result = str(self.line_name)
        result += ',' + str(self.line_cd      )
        result += ',' + str(self.company_cd   )
        result += ',' + str(self.line_name    )
        result += ',' + str(self.line_name_k  )
        result += ',' + str(self.line_name_h  )
        result += ',' + str(self.line_color_c )
        result += ',' + str(self.line_color_t )
        result += ',' + str(self.line_type    )
        result += ',' + str(self.lon          )
        result += ',' + str(self.lat          )
        result += ',' + str(self.zoom         )
        result += ',' + str(self.e_status     )
        result += ',' + str(self.e_sort       )
        result += ',' + "{joins:"
        for key, val in self.joins.items():
            result += str(key) + ':' + str(val) + ','
        result += ',' + "}"
        return result

    # direction: 'up' or 'down'
    def tread(self, f_idx, t_idx, activity, inout = False):
        # isnan() で判定？
        #f_idx: はしりはじめ from index
        #t_idx: はしりおわり to index
        #upper_end: 区間の上流端
        #lower_end: 区間の下流端
        #record_f:
        if inout == 'out':
            direction = 'down'
            upper_end = f_idx
            lower_end = t_idx
        elif inout == 'in':
            direction = 'up'
            lower_end = f_idx
            upper_end = t_idx
        elif f_idx < t_idx:
            direction = 'down'
            upper_end = f_idx
            lower_end = t_idx
        elif t_idx < f_idx:
            direction = 'up'
            lower_end = f_idx
            upper_end = t_idx
        else:
            print(f_idx, t_idx, activity, inout)
            print("Not assumed.") # happen when inout == False and f_idx == t_idx
            sys.exit()

        t = len(self.st_cds) # total number of stations in line
        n = (lower_end - upper_end) % t # number of stations in progress

        for i in range(0, n):
            upper = (upper_end + i     ) % t
            lower = (upper_end + i + 1 ) % t
            self.joins[(upper, lower)].add(direction, activity)

