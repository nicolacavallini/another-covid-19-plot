import io
import json
from pprint import pprint

from datetime import datetime

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import column

from bokeh.models import HoverTool



import numpy as np


def prepare_data_dictionary(data,data_list):
    for d in data_list:
        entry_values = {"date":[],
                        "total_positive":[],
                        "dayly_new_positvie":[]}
        if d["codice_provincia"] < 900:
            data[d["denominazione_provincia"]] = entry_values

def plot_data(province_data):

    date  = province_data["date"]
    total = province_data["total_positive"]
    daily = province_data["dayly_new_positvie"]


    source = ColumnDataSource(data=dict(date=date,
                                        total=total,
                                        daily=daily))


    f1 = figure(plot_width=900, plot_height=200,title="daily new positive",
               x_range=date)
    f1.add_tools(HoverTool(tooltips=[("date", "@date"), ("daily", "@daily")]))

    f1.vbar(x='date', top='daily', width=0.9, source=source,
           line_color='white')
    f1.xaxis.major_label_orientation = np.pi/6.

    f2 = figure(plot_width=900, plot_height=200,title="total positive",
               x_range=province_data["date"])

    f2.vbar(x='date', top='total', width=0.9, source=source,
           line_color='white')
    f2.add_tools(HoverTool(tooltips=[("date", "@date"), ("total", "@total")]))
    f2.xaxis.major_label_orientation = np.pi/6.

    show(column(f1,f2))



if __name__ == "__main__":

    filename = "COVID-19/dati-json/dpc-covid19-ita-province.json"

    data = ""

    with io.open(filename, 'r', encoding='utf-8-sig') as f:
        for line in f:
            data+=line

    data_list = json.loads(data)

    data = {}

    prepare_data_dictionary(data,data_list)

    for d in data_list:
        if d["codice_provincia"] < 900:
            data[d["denominazione_provincia"]]["total_positive"].append(d["totale_casi"])
            data[d["denominazione_provincia"]]["date"].append(d['data'][:10])
            if len(data[d["denominazione_provincia"]]["total_positive"]) == 1:
                data[d["denominazione_provincia"]]["dayly_new_positvie"].append(0)
            else:
                yesterday = data[d["denominazione_provincia"]]["total_positive"][-2]
                today = data[d["denominazione_provincia"]]["total_positive"][-1]
                data[d["denominazione_provincia"]]["dayly_new_positvie"].append(today-yesterday)

    province_data = data["Vicenza"]

    plot_data(province_data)
