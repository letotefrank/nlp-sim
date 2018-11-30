import pandas as pd
import config
from local_code.bar import bar

id_url_df = pd.read_csv('{}/id_url.csv'.format(config.rank_data_path))
product_base = pd.read_csv('{}/product_base.csv'.format(config.rank_data_path))
customer_base = pd.read_csv('{}/customer_base.csv'.format(config.rank_data_path))
heat_rank_all = pd.read_csv('{}/heat_rank_data.csv'.format(config.rank_data_path))

customer_base = customer_base[['customer_id', 'city']]

c_p_r_c = heat_rank_all.merge(customer_base, left_on='customer_id', right_on='customer_id', how='inner')
c_p_r_c = c_p_r_c[['customer_id', 'product_id', 'ratingMean', 'city']].drop_duplicates()

# 需要排序的city数据
rank_city = ['深圳市', '上海市', '北京市', '广州市']
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

    # 加city
    city_top_heat_item['city'] = city

    # 加 type
    city_type = city_top_heat_item.merge(product_base, left_on='product_id', right_on='product_id', how='inner')
    city_type_rank = city_type[['product_id', 'rank', 'city', 'type', 'ancestry', 'name']].drop_duplicates()
    city_type_rank = city_type_rank.fillna(-1)

    # 加 url
    c_t_r_u = city_type_rank.merge(id_url_df, left_on='product_id', right_on='id', how='inner')
    c_t_r_u = c_t_r_u[['product_id', 'city', 'type', 'ancestry', 'name', 'rank', 'url']].drop_duplicates()

    c_t_r_u.to_csv('{}/{}.csv'.format(config.rank_result_path, city), index=False)

    for i, p_type in product_type.items():
        rank = c_t_r_u[c_t_r_u['type'] == p_type][0:20]
        rank = rank.reset_index(drop=True)
        name = city + '_' + p_type
        name = name + '1'
        rank.to_csv('{}/{}.csv'.format(config.rank_result_path, name), index=False)

print('111')
