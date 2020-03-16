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

    data = ""

    filename = "COVID-19/dati-json/dpc-covid19-ita-regioni.json"

    zone_key = "regione"

    with io.open(filename, 'r', encoding='utf-8-sig') as f:
        for line in f:
            data+=line

    data_list = json.loads(data)

    data = {}

    tls.prepare_data_dictionary(data,data_list,zone_key)

    tls.populate_data(data,data_list,zone_key)

    n_total_positive = []
    region_names_ = []

    ita_total_positive = 0

    for pn, pd in data.items():
        n_total_positive.append(pd["total_positive"][-1])
        region_names_.append(pn)
        ita_total_positive+=pd["total_positive"][-1]

    n_total_positive = np.array(n_total_positive)
    sort_id = np.argsort(n_total_positive)[::-1]

    region_names = [region_names_[id] for id in sort_id]

    figures = []

    for pn in region_names:

        province_data = data[pn]

        local_positive = province_data["total_positive"][-1]

        local_ratio = 100*(local_positive/ita_total_positive)

        lrs = f'{local_ratio:.1f}'

        title = pn+", "+str(local_positive)+"  cases, "+lrs+'% of the Italian total.'

        print(title)

        f2 = figure(plot_width=900, plot_height=200,title=title,
                   x_range=province_data["date"],
                   y_axis_label ="increment %")

        tls.plot_increment(f2,province_data,pn,zone_key)

        figures.append([f2])

    directory = "./results/"

    Path(directory).mkdir(parents=True, exist_ok=True)

    output_file(directory+"linear-controll-report.html")

    save(layout(figures))

    #for province_name, province_data in data.items():
    #    print(province_name)
    #    tls.plot_data(province_data,province_name,zone_key)
