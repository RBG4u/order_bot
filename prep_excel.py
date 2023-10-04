import pandas as pd
import dataframe_image as dfi
from PIL import Image
import requests

import config


def color_rows(row):
    if row.name % 2 == 0:
        return ['background-color: lightblue'] * len(row)
    else:
        return ['background-color: white'] * len(row)


def rotate_image(png_name):
    image = Image.open(png_name)

    rotated_image = image.transpose(Image.ROTATE_90)

    rotated_image.save(png_name)


def geo_determining(df_order):
    adress_df = df_order[9:10].dropna(axis=1)
    adress = adress_df.iloc[0, 1]

    url = "http://www.mapquestapi.com/geocoding/v1/address"
    params = {"key": config.KEY_MAPQUEST, "location": adress}

    response = requests.get(url, params=params)

    data = response.json()
    coords = data['results'][0]['locations'][0]['latLng']
    if float(coords['lat']) > config.BASE:
        return f'{adress}\n\nСевер'
    else:
        return f'{adress}\n\nЮг'


def excel_to_geo_png(file_name, png_name):
    df_order = pd.read_excel(file_name)

    cardinal_direction = geo_determining(df_order)

    df_order = df_order.dropna(axis=1, how='all')
    df_order = df_order[11:].dropna(subset=['Unnamed: 11'])
    df_order.reset_index(drop=True, inplace=True)
    df_order.columns = df_order.iloc[0]
    df_order = df_order[1:]
    df_order.dropna(axis=1, inplace=True)
    df_order.drop("№", axis=1, inplace=True)

    styled_df = df_order.style.apply(color_rows, axis=1)

    dfi.export(styled_df,
               png_name,
               table_conversion="matplotlib",
               dpi=300)

    rotate_image(png_name)

    return cardinal_direction
