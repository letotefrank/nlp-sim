import pandas as pd
import config
from app_rank.algorithm.bar import bar
import json
from flask import request
from app_rank.utils.utils import date_deal

'''
季节计算方法:通过下面三个参数，为商品确定所属季节
a:季节均值
b:季节个数
ab: a+b

return: {   
            1:夏季
            2:春秋
            3:冬
            4:初夏（春秋夏）
            5:初冬（春秋冬）
        }
'''


def set_season(a, b, ab):
    if ab == 3:
        return 1
    elif ab == 2 or ab == 4:
        return 2
    elif a == 4 and b == 1:
        return 3
    elif a == 2 and b == 3:
        return 4
    else:
        return 5


# 设置商品所属季节
def get_season_df(p_base):
    season_df = p_base[['product_id', 'season_id']].drop_duplicates()
    season_df = season_df.reset_index(drop=True)
    season = season_df['product_id'].drop_duplicates()
    season = season.reset_index(drop=True)
    a = season_df.groupby(['product_id']).mean()['season_id']
    a.name = 'a'
    a = a.reset_index(drop=True)
    b = season_df.groupby(['product_id']).count()['season_id']
    b.name = 'b'
    # b.rename(index={'season_id': 'season_id1'}, inplace=True)
    b = b.reset_index(drop=True)
    frames = [season, a, b]
    p_season = pd.concat(frames, axis=1)

    # 剔除四季装
    p_season = p_season[p_season['b'] < 4]

    p_season['ab'] = p_season['a'] + p_season['b']

    p_season['season'] = p_season.apply(lambda x: set_season(x.a, x.b, x.ab), axis=1)

    p_season = p_season[['product_id', 'season']]
    p_season = p_season.reset_index(drop=True)
    return p_season


# 季节类别排序，save 2个json文件
def fit_season_rank():
    date1 = request.args.get("date1")
    date1 = date_deal(date1)
    date2 = request.args.get("date2")
    date2 = date_deal(date2)
    # product季节处理，1：夏  2：春秋  3：冬  4：初夏（春秋夏） 5：初冬（春秋冬）
    product_base = pd.read_csv('{}/product_base.csv'.format(config.rank_data_path))

    heat_rank_all = pd.read_csv('{}/heat_rank_data.csv'.format(config.rank_data_path))
    heat_rank_all['timestamp'] = pd.to_datetime(heat_rank_all['timestamp'])
    heat_rank_all = heat_rank_all[heat_rank_all['timestamp'] > date1]
    heat_rank_all = heat_rank_all[heat_rank_all['timestamp'] < date2]

    # 加载 pid+url数据
    id_url_df = pd.read_csv('{}/id_url.csv'.format(config.rank_data_path))

    # 返回的商品个数
    rank_num = 10

    # get p_season
    product_season = get_season_df(product_base)

    # 获取 type
    product_type = product_base['type'].drop_duplicates()
    product_type = product_type.reset_index(drop=True)

    # 存放 result
    s_frames_dict = {}

    bar_data = heat_rank_all[['product_id', 'ratingMean']]
    rank_all_df = bar(bar_data)

    # 返回 type-season-rank
    for index, p_type in product_type.items():
        # rank_all_df 加 type 字段
        rank_type = rank_all_df.merge(product_base, left_on='product_id', right_on='product_id', how='inner')
        rank_type = rank_type[['product_id', 'rank', 'type', 'ancestry', 'name']].drop_duplicates()
        rank_type = rank_type.fillna(-1)

        # 根据不同的 type 全局排序
        rank = rank_type[rank_type['type'] == p_type]
        rank = rank.reset_index(drop=True)

        # merge pid+season+rank+url,并降序排序
        p_s_r = product_season.merge(rank, left_on='product_id', right_on='product_id', how='inner')
        p_s_r_u = p_s_r.merge(id_url_df, left_on='product_id', right_on='id', how='inner')

        p_s_r_u = p_s_r_u[['product_id', 'season', 'rank', 'url', 'type', 'ancestry', 'name']]

        p_s_r_u = p_s_r_u.sort_values(by=['season', 'rank'])
        p_s_r_u = p_s_r_u.reset_index(drop=True)

        # 取每个季节的热度前十
        s1 = p_s_r_u[p_s_r_u['season'] == 1]
        s2 = p_s_r_u[p_s_r_u['season'] == 2]
        s3 = p_s_r_u[p_s_r_u['season'] == 3]
        s4 = p_s_r_u[p_s_r_u['season'] == 4]
        s5 = p_s_r_u[p_s_r_u['season'] == 5]

        # concat结果
        s_frame = [s1, s2, s3, s4, s5]
        s_frames_dict.setdefault(p_type, []).append(s_frame)
        if p_type == 'Clothing':
            season_clothing = pd.concat(s_frame, axis=0)
            season_clothing = season_clothing.reset_index(drop=True)
            season_clothing_name = season_clothing[season_clothing['ancestry'] != -1]
            season_clothing_name = season_clothing_name.reset_index(drop=True)
            # 重命名 列名
            season_clothing_name.rename(columns={'ancestry': 'ancestryType', 'name': 'displayType'}, inplace=True)
            # 调整列名
            season_clothing_name = season_clothing_name[
                ['season', 'type', 'ancestryType', 'displayType', 'product_id', 'rank', 'url']]
            # 2 json
            season_clothing_name = season_clothing_name.to_dict('records')
            with open('{}/season_clothing_displayType.json'.format(config.rank_result_path), 'w') as outfile:
                json.dump(season_clothing_name, outfile)

            season_clothing_ancestry = season_clothing[season_clothing['ancestry'] == -1]
            season_clothing_ancestry = season_clothing_ancestry.reset_index(drop=True)
            # 重命名 列名
            season_clothing_ancestry.rename(columns={'ancestry': 'ancestryType', 'name': 'displayType'}, inplace=True)
            # 调整列名
            season_clothing_ancestry = season_clothing_ancestry[
                ['season', 'type', 'ancestryType', 'displayType', 'product_id', 'rank', 'url']]
            # 2 json
            season_clothing_ancestry = season_clothing_ancestry.to_dict('records')
            with open('{}/season_clothing_ancestryType.json'.format(config.rank_result_path), 'w') as outfile:
                json.dump(season_clothing_ancestry, outfile)
            print('Clothing')
        elif p_type == 'Accessory':
            season_accessory = pd.concat(s_frame, axis=0)

            season_accessory_name = season_accessory[season_accessory['ancestry'] != -1]
            season_accessory_name = season_accessory_name.reset_index(drop=True)
            # 重命名 列名
            season_accessory_name.rename(columns={'ancestry': 'ancestryType', 'name': 'displayType'}, inplace=True)
            # 调整列名
            season_accessory_name = season_accessory_name[
                ['season', 'type', 'ancestryType', 'displayType', 'product_id', 'rank', 'url']]
            # 2 json
            season_accessory_name = season_accessory_name.to_dict('records')
            with open('{}/season_accessory_displayType.json'.format(config.rank_result_path), 'w') as outfile:
                json.dump(season_accessory_name, outfile)

            season_accessory_ancestry = season_accessory[season_accessory['ancestry'] == -1]
            season_accessory_ancestry = season_accessory_ancestry.reset_index(drop=True)
            # 重命名 列名
            season_accessory_ancestry.rename(columns={'ancestry': 'ancestryType', 'name': 'displayType'}, inplace=True)
            # 调整列名
            season_accessory_ancestry = season_accessory_ancestry[
                ['season', 'type', 'ancestryType', 'displayType', 'product_id', 'rank', 'url']]
            # 2 json
            season_accessory_ancestry = season_accessory_ancestry.to_dict('records')
            with open('{}/season_accessory_ancestryType.json'.format(config.rank_result_path), 'w') as outfile:
                json.dump(season_accessory_ancestry, outfile)
            print('Accessory')
    return '1'
