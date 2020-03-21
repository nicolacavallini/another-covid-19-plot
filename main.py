import json
from pprint import pprint

import numpy as np

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column

from bokeh.io import export_svgs
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool

import codecs
import io



def my_plot(f,date,count):

    date  = date
    count = count


    source = ColumnDataSource(data=dict(date=date,
                                        count=count))


    f.add_tools(HoverTool(tooltips=[("date", "@date"), ("count", "@count")]))

    f.vbar(x='date', top='count', width=0.9, source=source,
           line_color='white')
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

    f1 = figure(plot_width=900, plot_height=200,title="positive/tests",x_range=date)


    my_plot(f1,date,discover_ratio)

    f2 = figure(plot_width=900, plot_height=200,title='tests per day',x_range=date)

    my_plot(f2,date,tamponi_per_day)

    f3 = figure(plot_width=900, plot_height=200,title='daily new positives',x_range=date)

    my_plot(f3,date,infetti_per_day)

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
