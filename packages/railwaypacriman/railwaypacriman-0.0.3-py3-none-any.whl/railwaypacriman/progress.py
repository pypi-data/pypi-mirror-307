#! /usr/bin/env python3

## module Progress, to show progress
## Last-modified:2024/11/08 19:22:05.
## Author: Ippei KISHIDA

#lggr.log("■■■■HERE■■■■")

import graphviz
import math
import unittest
import sys
import copy
from railwaypacriman.line import *
import railwaypacriman.logger as lggr

nc = '#000000ff' #nc: node color with alpha channel
fc = '#f0f0f0ff' #fc: fill color for node with alpha channel
fontname = 'Noto Sans CJK JP' #fontname: font name
fs = '7' #fs: font size. String is given to node of graphviz
mb = 20 # base multiplier, フォントと図のサイズ調整のための倍率
dpi = 300 #300 #72
h_inch = 4 #6.0 
w_inch = 4 #4.0

def linefeed_square(string):
    width = math.ceil( math.sqrt(len(string))) # width == height
    ary = []
    for i in range(0, width):
        if (width * (i+1)) > len(string):
            end = len(string)
        else:
            end = (width * (i+1)) 
        ary.append( string[(width * i) : end])
    return "\n".join(ary).strip()

class Progress:
    def __init__(self):
        self.lines = {}

    def __str__(self):
        result = '{'
        for key, val in self.lines.items():
            result += str(key) + ':' + str(val) + ','

        result += '}'
        return result

    def set_lon_min(self, val):
        self.lon_min = val

    def set_lon_max(self, val):
        self.lon_max = val

    def set_lat_min(self, val):
        self.lat_min = val

    def set_lat_max(self, val):
        self.lat_max = val

    def edge_style(self, direction, activity):
        options = { 'arrowsize': '0.5'}
        if direction == 'both' and activity == 'run':
            options.update({'color': '#000000', 'dir': 'both', 'penwidth': '2'})
            return options
        r = "00"; g = "00"; b = "00"
        if activity == "bike":
            g = 'd0'
        if direction == "up":
            r = 'ff'
            options['dir'] = 'back'
        elif direction == "down":
            b = 'ff'
            options['dir'] = 'forward'
        else:
            r = "d0" ; g = "d0" ; b = "d0"
            options['arrowhead'] = 'none'
        options['color'] = '#' + r + g + b
        return options

    #def latitude2y(self, latitude):
    #    y = dpi * w_inch * (latitude - self.lat_min) / (self.lat_max - self.lat_min)
    #    return y

    ## 経度:緯度の倍率として、緯度35度を仮定。
    #def longitude2x(self, longitude):
    #    ml = math.cos(35.0/360.0 * (2*math.pi))
    #    x = dpi * w_inch * (longitude - self.lon_min) / (self.lon_max - self.lon_min) * ml
    #    return x

    # Return pixel coordinates in canvas from geological coordinates
    def geological2canvas(self, lon, lat): 
        w_pix = w_inch * dpi
        self.lon_min
        self.lon_max
        x_pix = w_pix * (lon - self.lon_min) / (self.lon_max - self.lon_min)

        h_pix = h_inch * dpi
        self.lat_min
        self.lat_max
        y_pix = h_pix * (lat - self.lat_min) / (self.lat_max - self.lat_min)

        return x_pix, y_pix

    def distance(self, e1, n1, e2, n2): #e1, e2: east longitude, n1, n2: north latitude
        h = (n2 - n1)
        w1 = (e2 - e1) * math.cos(n1/360.0 * (2*math.pi))
        w2 = (e2 - e1) * math.cos(n2/360.0 * (2*math.pi))
        w = (w1 + w2) / 2.0
        degree = math.sqrt(h**2 + w**2)
        return 40000.0 * degree / 360.0

    def draw_grid(self, graph, spacing, tgt_line_cds):
        lggr.log("## Draw grid")
        lon_list = []
        lat_list = []
        for line_cd in tgt_line_cds:
            for scd in sd.loc[sd['line_cd'] == line_cd, 'station_cd']:
                lon_list.append(float(sd.loc[sd['station_cd'] == scd, 'lon'].values[0]))
                lat_list.append(float(sd.loc[sd['station_cd'] == scd, 'lat'].values[0]))
        lon_min = min(lon_list) #lon_max: longitude max 
        lon_max = max(lon_list) #lon_min: longitude min 
        lon_cen = (lon_min + lon_max) / 2.0
        lat_min = min(lat_list) #lat_max: latitude max  
        lat_max = max(lat_list) #lat_min: latitude min  
        lat_cen = (lat_min + lat_max) / 2.0

        lggr.log("lon_min: " + str(lon_min) )
        lggr.log("lon_max: " + str(lon_max) )
        lggr.log("lat_min: " + str(lat_min) )
        lggr.log("lat_max: " + str(lat_max) )

        w_geo = self.distance(lon_min, lat_cen, lon_max, lat_cen)
        h_geo = self.distance(lon_cen, lat_min, lon_cen, lat_max)
        a_geo = w_geo / h_geo           #aspect ratio of geological
        a_cvs = w_inch / h_inch #aspect ratio of canvas
        rar = a_geo / a_cvs #ratio of aspect ratio
        lggr.log("w_geo: " + str(w_geo) )
        lggr.log("h_geo: " + str(h_geo) )
        lggr.log("a_geo: " + str(a_geo) )
        lggr.log("a_cvs: " + str(a_cvs) )
        lggr.log("rar  : " + str(rar  ) )
        if rar == 1:
            pass
        elif rar < 1:
            # 地理上の縦の方が描画領域の縦より張り出してる
            # latitude はそのままで longitude 補正
            d2 = (lon_cen - lon_min) / rar # displacement/2
            lon_min = lon_cen - d2
            lon_max = lon_cen + d2
        elif rar > 1:
            # 地理上の横の方が描画領域の横より張り出してる
            # longitude はそのままで latitude 補正
            d2 = (lat_cen - lat_min) * rar # displacement/2
            lat_min = lat_cen - d2
            lat_max = lat_cen + d2

        lggr.log("d2     : " + str(d2     ) )
        lggr.log("lon_min: " + str(lon_min) )
        lggr.log("lon_max: " + str(lon_max) )

        self.lon_min = lon_min
        self.lon_max = lon_max
        self.lat_min = lat_min
        self.lat_max = lat_max

        lggr.log("self.lon_min: " + str(self.lon_min) )
        lggr.log("self.lon_max: " + str(self.lon_max) )
        lggr.log("self.lat_min: " + str(self.lat_min) )
        lggr.log("self.lat_max: " + str(self.lat_max) )

        ## grid for longitude and latitude
        ## common for longitude and latitude
        args_base = {
                'style': 'filled',
                'color': '#ffffff80',
                'margin': '0.0,0.0',
                'fontsize': fs,
                'width': '0.3',
                'height': '0.3',
                'fillcolor': '#ffffff80',
                'fontname': fontname,
                }

        lggr.log("### longitude, vertical lines")
        i_lon_min = math.ceil(self.lon_min / spacing)
        i_lon_max = math.floor(self.lon_max / spacing)
        for i in range(i_lon_min, i_lon_max + 1):
            # common for top and bottom
            longitude = i * spacing
            args_t = copy.deepcopy(args_base)
            #x = self.longitude2x(longitude)
            #y = self.latitude2y(self.lat_max)
            x, y = self.geological2canvas(longitude, self.lat_max)
            lggr.log("longitude : " + str(longitude))
            lggr.log("x         : " + str(x))
            args_t['pos'] = str(x) + ',' + str(y) + '!'
            args_t['label'] = "{:.2f}".format(longitude)
            args_t['name'] = str(longitude) + '-t'
            lggr.log("args_t['pos']   : " + str(args_t['pos']))
            lggr.log("args_t['label'] : " + str(args_t['label']))
            lggr.log("args_t['name']  : " + str(args_t['name']))
            graph.node(** args_t)

            #y = self.latitude2y(self.lat_min)
            x, y = self.geological2canvas(longitude, self.lat_min)
            args_b = copy.deepcopy(args_base)
            args_b['pos'] = str(x) + ',' + str(y) + '!'
            args_b['label'] = "{:.2f}".format(longitude)
            args_b['name'] = str(longitude) + '-b'
            lggr.log("args_b['pos']   : " + str(args_b['pos']))
            lggr.log("args_b['label'] : " + str(args_b['label']))
            lggr.log("args_b['name']  : " + str(args_b['name']))
            graph.node(** args_b)

            options = {'color': "#d0d0d0", 'arrowhead': 'none'}
            graph.edge(args_t['name'], args_b['name'], **options)

        lggr.log("### latitude, horizontal lines")
        i_lat_min = math.ceil(self.lat_min / spacing)
        i_lat_max = math.floor(self.lat_max / spacing)
        for i in range(i_lat_min, i_lat_max + 1):
            # common for left and right
            latitude = i * spacing
            args_r = copy.deepcopy(args_base)
            #x = self.longitude2x(self.lon_max)
            #y = self.latitude2y(latitude)
            x, y = self.geological2canvas(self.lon_max, latitude)
            args_r['pos'] = str(x) + ',' + str(y) + '!'
            args_r['label'] = "{:.2f}".format(latitude)
            args_r['name'] = args_r['label'] + '-r'
            graph.node(** args_r)
            lggr.log("args_r['pos']   : " + str(args_r['pos']))
            lggr.log("args_r['label'] : " + str(args_r['label']))
            lggr.log("args_r['name']  : " + str(args_r['name']))

            #x = self.longitude2x(self.lon_min)
            x, y = self.geological2canvas(self.lon_min, latitude)
            args_l = copy.deepcopy(args_base)
            args_l['pos'] = str(x) + ',' + str(y) + '!'
            args_l['label'] = "{:.2f}".format(latitude)
            args_l['name'] = args_l['label'] + '-l'
            graph.node(** args_l)
            lggr.log("args_l['pos']   : " + str(args_l['pos']))
            lggr.log("args_l['label'] : " + str(args_l['label']))
            lggr.log("args_l['name']  : " + str(args_l['name']))

            options = {'color': "#d0d0d0", 'arrowhead': 'none'}
            graph.edge(args_l['name'], args_r['name'], **options)

    def proceed(self, date, line_cd, from_station_cd, to_station_cd, activity, inout):
        ## 初めてのアクセスで Line インスタンス作成
        if not self.lines.get(line_cd):
            self.lines[line_cd] = Line(line_cd)

        try:
            from_idx = self.lines[line_cd].st_cds.index(from_station_cd)
        except ValueError: 
            print("Not found {} in {}".format(from_station_cd, line_cd))
            return

        try:
            to_idx   = self.lines[line_cd].st_cds.index(to_station_cd)
        except ValueError: 
            print("Not found {} in {}".format(to_station_cd, line_cd))
            return

        l = self.lines[line_cd]
        l.tread(from_idx, to_idx, activity, inout)

    # num_char: number of characters for station name. 0 means unlimited
    def draw_graph(self, outfile, tgt_line_cds, geological, spacing=1.0, num_letter=9999):
        ## 描画対象の路線を整理
        for i in tgt_line_cds:
            if not i in list(self.lines.keys()):
                self.lines[i] = Line(i)
            #try:
            #    if not i in list(self.lines.keys()):
            #        self.lines[i] = Line(i)
            #except IndexError:
            #    print("Not found in data: " + str(i))
            #    continue

        ## 描画順となる会社順に整理
        companies = defaultdict(list)
        for i in tgt_line_cds:
            companies[self.lines[i].company_cd].append(i)
        tgt_line_cds = []
        for c in sorted(companies.keys()):
            for i in sorted(companies[c]):
                tgt_line_cds.append(i)

        graph = graphviz.Digraph()
        graph.attr(bgcolor='#f8f8f8')
        if geological:
            graph.attr(engine='neato')
            #graph.attr(engine='neato', nslimit2='true')
            self.draw_grid(graph, spacing, tgt_line_cds)
        else:
            graph.attr(ranksep='0.5') #0.5 が default

        for line_cd in tgt_line_cds:
            line = self.lines[line_cd]
            if (not tgt_line_cds) or (not line.line_cd in tgt_line_cds):
                continue

            lggr.log("## " + line.line_name)
            with graph.subgraph(name = "cluster_" + line.line_name) as c:
                options = {'color': 'black', 'penwidth': '0'}
                if not geological:
                    options['label'] = linefeed_square(line.line_name)
                c.attr(** options)
                lggr.log("### nodes")
                for i in range(0, len(line.st_cds)):
                    scd = int(line.st_cds[i])
                    args = {
                            'name': str(line.line_cd) + '-' + str(i), #nn: node name
                            'label': linefeed_square(line.st_names[i][:num_letter]), #nl: node label
                            'style': 'filled',
                            'color': nc,
                            'margin': '0.0,0.0',
                            'fontsize': fs,
                            'width': '0.3',
                            'height': '0.3',
                            'fillcolor': fc}
                    if geological:
                        lon = float(sd.loc[sd['station_cd'] == scd, 'lon'].values[0])
                        lat = float(sd.loc[sd['station_cd'] == scd, 'lat'].values[0])
                        #x = self.longitude2x(lon)
                        #y = self.latitude2y(lat)
                        x, y = self.geological2canvas(lon, lat)
                        lggr.log("lon: " + str(lon) )
                        lggr.log("lat: " + str(lat) )
                        lggr.log("x  : " + str(x) )
                        lggr.log("y  : " + str(y) )
                        args['pos'] = str(x) + ',' + str(y) + '!'
                        args['fontname'] = fontname
                    if len(args['label']) <= 1:
                        args['shape'] = 'circle'
                        args['width'] = '0.1'
                        args['height'] = '0.1'
                        graph.attr(ranksep='0.3') #0.5 が default
                    c.node(** args)

                ##fscd: from station_cd
                ##tscd: to station_cd
                for key, value in line.joins.items():
                    (fscd, tscd) = key
                    fn = str(line.line_cd) + '-' + str(fscd) # fn: from_node
                    tn = str(line.line_cd) + '-' + str(tscd) # tn: to_node
                    tgt_edges = value.unique_arrows()
                    if not tgt_edges: # empty
                        tgt_edges = [('', '')] ## for just connection
                    elif (('up', 'run') in tgt_edges) and (('down', 'run') in tgt_edges):
                        tgt_edges = [('both', 'run')] ## for just connection

                    for edge in tgt_edges:
                        options = self.edge_style(* edge)
                        c.edge(fn, tn, **options)

        graph.attr(dpi=str(dpi))
        graph.attr(overlap='true')
        graph.attr(start='regular')
        graph.graph_attr['size'] = str(w_inch) + "," + str(h_inch)
        #graph.render(outfile, format='png')
        graph.save(outfile)

