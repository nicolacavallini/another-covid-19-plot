import io
import json
from pprint import pprint

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

    for province_name, province_data in data.items():
        tls.plot_data(province_data,province_name,zone_key  )
