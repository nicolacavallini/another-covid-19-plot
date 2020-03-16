from bokeh.io import show, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral3
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import column

from bokeh.models import HoverTool

from pathlib import Path
import numpy as np


def prepare_data_dictionary(data,data_list,key):

    denominazione = "denominazione_"+key
    codice = "codice_"+key


    for d in data_list:
        entry_values = {"date":[],
                        "total_positive":[],
                        "dayly_new_positvie":[],
                        "dayly_increment":[],}
        if d[codice] < 900:
            data[d[denominazione]] = entry_values

def populate_data(data,data_list,key):

    denominazione = "denominazione_"+key
    codice = "codice_"+key

    for d in data_list:
        if d[codice] < 900:
            data[d[denominazione]]["total_positive"].append(d["totale_casi"])
            data[d[denominazione]]["date"].append(d['data'][:10])
            if len(data[d[denominazione]]["total_positive"]) == 1:
                data[d[denominazione]]["dayly_new_positvie"].append(0)
                data[d[denominazione]]["dayly_increment"].append(0)
            else:
                yesterday = data[d[denominazione]]["total_positive"][-2]
                today = data[d[denominazione]]["total_positive"][-1]
                data[d[denominazione]]["dayly_new_positvie"].append(today-yesterday)
                yesterday = data[d[denominazione]]["dayly_new_positvie"][-2]
                today = data[d[denominazione]]["dayly_new_positvie"][-1]
                if yesterday==0:
                    data[d[denominazione]]["dayly_increment"].append(0)
                else:
                    data[d[denominazione]]["dayly_increment"].append(100.*(today/yesterday-1.))



def plot_data(f1,f2,province_data,province_name,key):

    province_name = province_name.lower().replace(" ", "-")
    province_name = province_name.replace("'", "-")
    province_name = province_name.replace(".", "-")

    date  = province_data["date"]
    total = province_data["total_positive"]
    daily = province_data["dayly_new_positvie"]

    source = ColumnDataSource(data=dict(date=date,
                                        total=total,
                                        daily=daily))


    f1.add_tools(HoverTool(tooltips=[("date", "@date"), ("daily", "@daily")]))

    f1.vbar(x='date', top='daily', width=0.9, source=source,
           line_color='white')
    f1.xaxis.major_label_orientation = np.pi/6.



    f2.vbar(x='date', top='total', width=0.9, source=source,
           line_color='white')
    f2.add_tools(HoverTool(tooltips=[("date", "@date"), ("total", "@total")]))
    f2.xaxis.major_label_orientation = np.pi/6.
    #show(column(f1,f2))

    #save(column(f1,f2))

def plot_increment(f2,province_data,province_name,key):

    threshold = 20.

    fancy_name = province_name

    province_name = province_name.lower().replace(" ", "-")
    province_name = province_name.replace("'", "-")
    province_name = province_name.replace(".", "-")

    date  = province_data["date"]
    increment = np.array(province_data["dayly_increment"])
    daily = province_data["dayly_new_positvie"]

    increment_label = np.zeros(increment.shape,dtype=np.int32)
    increment_label[np.where(increment<-threshold)] = 0
    increment_label[np.where(np.abs(increment)<threshold)] = 1
    increment_label[np.where(increment>threshold)] = 2

    slabel = np.array2string(increment_label)[1:-1].split()

    cmap = {'0':"#8DFFC0",
            '1':"#FFE973",
            '2':"#FF7366"}

    palette = [cmap[e] for e in slabel]

    source = ColumnDataSource(data=dict(date=date,
                                        increment=increment,
                                        daily=daily,
                                        increment_label=increment_label,
                                        slabel=slabel))

    f2.vbar(x='date', top='increment', width=0.9, source=source,
           line_color='white',
           fill_color=factor_cmap('slabel', palette=palette, factors=slabel))
    f2.add_tools(HoverTool(tooltips=[("date", "@date"), ("increment", "@increment")]))
    f2.xaxis.major_label_orientation = np.pi/6.
