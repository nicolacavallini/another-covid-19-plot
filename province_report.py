import io
import json
from pprint import pprint

from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.layouts import layout
from bokeh.io import show, output_file, save

from pathlib import Path

import numpy as np


import tools as tls


if __name__ == "__main__":

    filename = "COVID-19/dati-json/dpc-covid19-ita-province.json"

    data = ""

    with io.open(filename, 'r', encoding='utf-8-sig') as f:
        for line in f:
            data+=line

    data_list = json.loads(data)

    data = {}

    tls.prepare_data_dictionary(data,data_list,"provincia")

    tls.populate_data(data,data_list,"provincia")

    n_total_positive = []
    region_names_ = []


    for pn, pd in data.items():
        n_total_positive.append(pd["total_positive"][-1])
        region_names_.append(pn)

    n_total_positive = np.array(n_total_positive)
    sort_id = np.argsort(n_total_positive)[::-1]

    region_names = [region_names_[id] for id in sort_id]


    figures = []

    #province_name = "Verona"

    #province_data = data[province_name]

    for province_name in region_names[:40]:

        province_data = data[province_name]


        f1 = figure(plot_width=900, plot_height=200,title=province_name+" daily new",
                   x_range=province_data["date"])

        f2 = figure(plot_width=900, plot_height=200,title=province_name+" total",
                   x_range=province_data["date"])

        tls.plot_data(f1,f2,province_data,province_name,"provincia")

        figures.append([f1])
        figures.append([f2])

    directory = "./results/"

    Path(directory).mkdir(parents=True, exist_ok=True)

    output_file(directory+"province-increment.html")

    show(layout(figures))
