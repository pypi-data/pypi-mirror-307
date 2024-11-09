#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" myCSVExporter

This module contains a custom class myCSVExporter that manages the format
of data export from plots to CSV file.
Contains class:
    * myCSVExporter - export plot data to custom csv file
and method:
    * dt_to_dec - convert a datetime to decimal year
"""

import datetime
import numpy as np

from pyqtgraph.exporters.Exporter import Exporter
from pyqtgraph.exporters import CSVExporter
from pyqtgraph import PlotItem
# from pyqtgraph.python2_3 import asUnicode


class myCSVExporter(CSVExporter):
    Name = "CSV from plot data (custom for insarviz)"

    def __init__(self, item):
        super().__init__(item)

    def export(self, fileName=None):
        if not isinstance(self.item, PlotItem):
            raise Exception("Must have a PlotItem selected for CSV export.")

        if fileName is None:
            self.fileSaveDialog(filter=["*.csv", "*.tsv"])
            return

        data = []
        header = []

        appendAllX = self.params['columnMode'] == '(x,y) per plot'

        for i, c in enumerate(self.item.curves):
            cd = c.getData()
            if cd[0] is None:
                continue

            data.append(cd)
            if hasattr(c, 'implements') and\
                c.implements('plotData') and\
                    c.name() is not None:
                name = str(c.name()).replace('"', '""') + '_'
                xName, yName = '"'+name+'x"', '"'+name+'y"'
            else:
                xName = 'x%04d' % i
                yName = 'y%04d' % i
            if appendAllX or i == 0:
                header.extend([xName, yName])
            else:
                if not header:
                    header.extend(['date_timestamp_x'])
                header.extend([yName])

        # add dates as decimal years and yyyy-mm-dd
        header.insert(0, '"date_decimal_year"')
        header.insert(0, '"date_YYYY-MM-DD"')

        if not appendAllX:
            header[header.index('"interactive_x"')] ='x_date_timestamp'

        timestamps = data[0][0]
        datetimes = [datetime.datetime.fromtimestamp(
            ts) for ts in timestamps]
        datetimes_str = [d.strftime('%Y-%m-%d') for d in datetimes]
        decimals = [np.round(dt_to_dec(dt), 3) for dt in datetimes]

        if self.params['separator'] == 'comma':
            sep = ','
        else:
            sep = '\t'

        with open(fileName, 'w') as fd:
            fd.write(sep.join(map(str, header)) + '\n')
            i = 0
            numFormat = '%%0.%dg' % self.params['precision']
            numRows = max([len(d[0]) for d in data])
            for i in range(numRows):
                for j, d in enumerate(data):
                    if j == 0:
                        fd.write(datetimes_str[i] + sep)
                        fd.write(numFormat % decimals[i] + sep)

                    # write x value if this is the first column, or if we want
                    # x for all rows
                    if appendAllX or j == 0:
                        if d is not None and i < len(d[0]):
                            fd.write(numFormat % d[0][i] + sep)
                        else:
                            fd.write(' %s' % sep)

                    # write y value
                    if d is not None and i < len(d[1]):
                        if j < len(data)-1:
                            fd.write(numFormat % d[1][i] + sep)
                        else:
                        # no separator at end of line, avoid empty last column
                            fd.write(numFormat % d[1][i])
                    else:
                        fd.write(' %s' % sep)
                fd.write('\n')

def dt_to_dec(dt):
    """Convert a datetime to decimal year. Time is at beginning of day.
    from https://stackoverflow.com/questions/29851357/python-datetime-to-decimal-year-one-day-off-where-is-the-bug"""
    year_start = datetime.datetime(dt.year, 1, 1)
    year_end = year_start.replace(year=dt.year+1)
    return dt.year + ((dt - year_start).total_seconds() /  # seconds so far
        float((year_end - year_start).total_seconds()))  # seconds in year


# myCSVExporter.register()
