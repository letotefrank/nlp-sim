import pandas as pd
import config
from app_rank.algorithm.bar import bar
import json
from flask import request
from app_rank.utils.utils import date_deal


def fit_city_rank():
    date1 = request.args.get("date1")
    date1 = date_deal(date1)
    date2 = request.args.get("date2")
    date2 = date_deal(date2)
    id_url_df = pd.read_csv('{}/id_url.csv'.format(config.rank_data_path))
    product_base = pd.read_csv('{}/product_base.csv'.format(config.rank_data_path))
    customer_base = pd.read_csv('{}/customer_base.csv'.format(config.rank_data_path))
    heat_rank_all = pd.read_csv('{}/heat_rank_data.csv'.format(config.rank_data_path))
    heat_rank_all['timestamp'] = pd.to_datetime(heat_rank_all['timestamp'])
    heat_rank_all = heat_rank_all[heat_rank_all['timestamp'] > date1]
    heat_rank_all = heat_rank_all[heat_rank_all['timestamp'] < date2]
    # 返回的商品个数
    rank_num = 10
    customer_base = customer_base[['customer_id', 'city']]

    c_p_r_c = heat_rank_all.merge(customer_base, left_on='customer_id', right_on='customer_id', how='inner')
    c_p_r_c = c_p_r_c[['customer_id', 'product_id', 'ratingMean', 'city']].drop_duplicates()

    # 需要排序的city数据
    rank_city = ['深圳市', '上海市', '北京市', '广州市']
    city_dict = {'深圳市': 1, '上海市': 2, '北京市': 3, '广州市': 4}
    c_p_r_c = c_p_r_c[c_p_r_c['city'].isin(rank_city)]

    cities = c_p_r_c['city'].drop_duplicates()

    # 获取 type
    product_type = product_base['type'].drop_duplicates()
    product_type = product_type.reset_index(drop=True)

    for index, city in cities.items():
        bar_data = c_p_r_c[c_p_r_c['city'] == city]
        bar_data = bar_data[['product_id', 'ratingMean']]

        # 分city全局热度排序
        city_top_heat_item = bar(bar_data)

        # 加city 使用转换词典city_dict
        city_top_heat_item['city'] = city_dict[city]

        # 加 type
        city_type = city_top_heat_item.merge(product_base, left_on='product_id', right_on='product_id', how='inner')
        city_type_rank = city_type[['product_id', 'rank', 'city', 'type', 'ancestry', 'name']].drop_duplicates()
        city_type_rank = city_type_rank.fillna(-1)

        # 加 url
        c_t_r_u = city_type_rank.merge(id_url_df, left_on='product_id', right_on='id', how='inner')
        c_t_r_u = c_t_r_u[['product_id', 'city', 'type', 'ancestry', 'name', 'rank', 'url']].drop_duplicates()

        # c_t_r_u.to_csv('{}/{}.csv'.format(config.rank_result_path, city), index=False)

        for i, p_type in product_type.items():
            rank = c_t_r_u[c_t_r_u['type'] == p_type]
            rank = rank.reset_index(drop=True)
            if p_type == 'Clothing':
                # 细分 ancestryType 和 displayType
                city_clothing_name = rank[rank['ancestry'] != -1]
                city_clothing_name = city_clothing_name.reset_index(drop=True)
                # 重命名 列名
                city_clothing_name.rename(columns={'ancestry': 'ancestryType', 'name': 'displayType'}, inplace=True)
                # 调整列名
                city_clothing_name = city_clothing_name[
                    ['city', 'type', 'ancestryType', 'displayType', 'product_id', 'rank', 'url']]
                # 2 json

                city_clothing_name = city_clothing_name.to_dict('records')
                with open('{}/{}city_clothing_displayType.json'.format(config.rank_result_path, city_dict[city]),
                          'w') as outfile:
                    json.dump(city_clothing_name, outfile)
                # city_clothing_name.to_json(
                #     path_or_buf='{}/{}_clothing_displayType.json'.format(config.rank_result_path, city),
                #     orient='records')

                city_clothing_ancestry = rank[rank['ancestry'] == -1]
                city_clothing_ancestry = city_clothing_ancestry.reset_index(drop=True)
                # 重命名 列名
                city_clothing_ancestry.rename(columns={'ancestry': 'ancestryType', 'name': 'displayType'}, inplace=True)
                # 调整列名
                city_clothing_ancestry = city_clothing_ancestry[
                    ['city', 'type', 'ancestryType', 'displayType', 'product_id', 'rank', 'url']]
                # 2 json
                city_clothing_ancestry = city_clothing_ancestry.to_dict('records')
                with open('{}/{}city_clothing_ancestryType.json'.format(config.rank_result_path, city_dict[city]),
                          'w') as outfile:
                    json.dump(city_clothing_ancestry, outfile)
                print('Clothing')
            elif p_type == 'Accessory':
                # 细分 ancestryType 和 displayType
                city_accessory_name = rank[rank['ancestry'] != -1]
                city_accessory_name = city_accessory_name.reset_index(drop=True)
                # 重命名 列名
                city_accessory_name.rename(columns={'ancestry': 'ancestryType', 'name': 'displayType'}, inplace=True)
                # 调整列名
                city_accessory_name = city_accessory_name[
                    ['city', 'type', 'ancestryType', 'displayType', 'product_id', 'rank', 'url']]
                # 2 json
                city_accessory_name = city_accessory_name.to_dict('records')
                with open('{}/{}city_accessory_displayType.json'.format(config.rank_result_path, city_dict[city]),
                          'w') as outfile:
                    json.dump(city_accessory_name, outfile)

                city_accessory_ancestry = rank[rank['ancestry'] == -1]
                city_accessory_ancestry = city_accessory_ancestry.reset_index(drop=True)
                city_accessory_ancestry.rename(columns={'ancestry': 'ancestryType', 'name': 'displayType'},
                                               inplace=True)
                city_accessory_ancestry = city_accessory_ancestry[
                    ['city', 'type', 'ancestryType', 'displayType', 'product_id', 'rank', 'url']]
                # 2 json
                city_accessory_ancestry = city_accessory_ancestry.to_dict('records')
                with open('{}/{}city_accessory_ancestryType.json'.format(config.rank_result_path, city_dict[city]),
                          'w') as outfile:
                    json.dump(city_accessory_ancestry, outfile)
                print('Accessory')
    return '1'
