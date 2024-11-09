#! /usr/bin/env python3

import unittest
import railwaypacriman.logger as lggr

class Join():
    def __init__(self):
        self.records = []

    def __str__(self):  # print() に放り込んだときに表示される文字列
        return self.records.__str__()

    def add(self, direction, activity):
        self.records.append([direction, activity])

    def unique_arrows(self):
        results = {}
        for i in self.records:
            results[tuple(i)] = 1
        return list(results.keys())

