import pandas as pd
import config
from local_code.bar import bar
import json
from flask import request
from app_rank.utils.utils import date_deal


# clothing排序，save 1个json文件
def clothing_rank():
    date1 = request.args.get("date1")
    date1 = date_deal(date1)
    date2 = request.args.get("date2")
    date2 = date_deal(date2)
    heat_rank_all = pd.read_csv('{}/heat_rank_data.csv'.format(config.rank_data_path))
    product_base = pd.read_csv('{}/product_base.csv'.format(config.rank_data_path))
    id_url_df = pd.read_csv('{}/id_url.csv'.format(config.rank_data_path))
    heat_rank_all['timestamp'] = pd.to_datetime(heat_rank_all['timestamp'])
    heat_rank_all = heat_rank_all[heat_rank_all['timestamp'] > date1]
    heat_rank_all = heat_rank_all[heat_rank_all['timestamp'] < date2]

    bar_data = heat_rank_all[['product_id', 'ratingMean']]
    rank_all_df = bar(bar_data)
    rank_type = rank_all_df.merge(product_base, left_on='product_id', right_on='product_id', how='inner')
    rank_type = rank_type[['product_id', 'rank', 'type']].drop_duplicates()
    rank = rank_type[rank_type['type'] == 'Clothing']
    rank = rank.reset_index(drop=True)
    clothing_r_u = rank.merge(id_url_df, left_on='product_id', right_on='id', how='inner')
    clothing_r_u.reset_index(drop=True)
    clothing_r_u = clothing_r_u[['type', 'product_id', 'rank', 'url']]
    clothing_r_u.to_dict('records')
    clothing_r_u = clothing_r_u.to_dict('records')
    with open('{}/clothing_rank.json'.format(config.rank_result_path), 'w') as outfile:
        json.dump(clothing_r_u, outfile)
    print('clothing_rank success')
    return '1'
