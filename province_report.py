import io
import json
from pprint import pprint

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

    for province_name, province_data in data.items():
        tls.plot_data(province_data,province_name,"provincia")
