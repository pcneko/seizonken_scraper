import os
import time
from pathlib import Path
import datetime as dt

import requests
from requests.exceptions import Timeout

def download(url, file_name):
    if os.path.exists(str(file_name)):
        print("already exists")
    else:
        time.sleep(2)
        try:
            r = requests.get(url, timeout=(3.0, 7.5))
            print(r)
            if r.status_code == 200:
                with open(str(file_name), 'wb') as f:
                    f.write(r.content)
        except Timeout:
            print("Timeout!", url)



def main():
    SPATH = Path('/Volumes/data/nowcast')
    START_DATE = dt.datetime(2016, 11, 1)
    END_DATE = dt.datetime(2017, 7, 10)
    calc_date = START_DATE

    counta = 0

    while calc_date <= END_DATE:
        print(calc_date)

        dl_url = "http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/jma-radar/synthetic/original/" + \
                    calc_date.strftime('%Y/%m/%d') + "/" + "Z__C_RJTD_" + calc_date.strftime('%Y%m%d%H%M%S') + "_RDR_JMAGPV__grib2.tar"
        file_name = "Z__C_RJTD_" + calc_date.strftime('%Y%m%d%H%M%S') + "_RDR_JMAGPV__grib2.tar"

        p_dir = Path(SPATH / str(calc_date.year).zfill(2) / str(calc_date.day).zfill(2))
        if p_dir.exists() == False:
            p_dir.mkdir(parents=True)
#         p_dir.mkdir(parents=True, exist_ok=True)

        p = Path(p_dir / file_name)
        if p.exists():
            print('Already downloaded!')
            calc_date += dt.timedelta(minutes=10)
            continue

        download(dl_url, p)
        calc_date += dt.timedelta(minutes=10)
        counta += 1

        if counta == 6:
            print("I'm sleeping......")
            time.sleep(30)
            counta = 0




if __name__ == "__main__":
    main()
    # print(get_amedas_index()) # latlon, np.array(name_arr)
