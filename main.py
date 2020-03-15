import json
from pprint import pprint

import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column

from bokeh.io import export_svgs
from bokeh.models import ColumnDataSource

import codecs
import io



def my_plot(f,x,y,label):

    f.segment(x, 0, x, y, line_width=2, line_color="blue", )

    f.circle(x, y,size=8, fill_color="white", line_color="blue" ,line_width=2)
    f.xaxis.major_label_overrides = label
    f.xaxis.major_label_orientation = np.pi/6.


def crunch_json_data(data_list):

    tamponi = 0
    infetti = 0

    discover_ratio = []

    tamponi_per_day = []

    date = []

    infetti_per_day = []

    for d in data_list:
        date.append(d['data'][:10])
        tpd = d['tamponi']-tamponi
        tamponi = d['tamponi']
        tamponi_per_day.append(tpd)
        ipd = d['nuovi_attualmente_positivi']
        discover_ratio.append(ipd/tpd)
        infetti_per_day.append(ipd)

    discover_ratio = np.array(discover_ratio)
    days = np.arange(1,discover_ratio.shape[0]+1)

    data_label = {}

    for d,dt in zip(days,date):
        data_label[int(d)] = dt
    print(data_label)

    output_file("covid-report.html")

    TOOLTIPS = [("y = ", "$y")]

    f1 = figure(plot_width=900, plot_height=200,title="positive/tests",
                x_axis_label='days', y_axis_label='discover ratio',
                tooltips=TOOLTIPS)

    my_plot(f1,days,discover_ratio,data_label)

    f2 = figure(plot_width=900, plot_height=200,title="tests",
                x_axis_label='days', y_axis_label='tests per day',
                tooltips=TOOLTIPS)

    my_plot(f2,days,tamponi_per_day,data_label)

    f3 = figure(plot_width=900, plot_height=200,title="daly new positives",
                x_axis_label='days', y_axis_label='daily new positives',
                tooltips=TOOLTIPS)

    my_plot(f3,days,infetti_per_day,data_label)

    p = column(f1,f2,f3)

    show(p)



if __name__ == "__main__":

    filename = 'COVID-19/dati-json/dpc-covid19-ita-andamento-nazionale.json'

    data = ""

    with io.open(filename, 'r', encoding='utf-8-sig') as f:
        for line in f:
            data+=line

    data_list = json.loads(data)
    pprint(data_list)

    crunch_json_data(data_list)
