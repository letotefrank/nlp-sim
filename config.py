# -*- coding: utf-8 -*-

"""
    作者:     Frank
    版本:     1.0
    日期:     2018/08/31
    文件名:    config.py
    功能：     配置文件

"""

import os


def get_root():
    return os.path.dirname(os.path.abspath(__file__))


# 数据集路径
data_path = get_root() + '/data/'

# 停用词路径
stop_words_path = get_root() + '/stopwords/'

# model路径
model_path = get_root() + '/model/'

# jieba处理后，数据保存路径
jb_path = get_root() + '/jb_deal_data/'
if not os.path.exists(jb_path):
    os.makedirs(jb_path)

# 相似结果，数据保存路径
sim_path = get_root() + '/sim_data/'
if not os.path.exists(sim_path):
    os.makedirs(sim_path)

# sql字典
sql_dict = {
    'collection': "SELECT p.id,ph.id,ph.image,p.description,p.title,GROUP_CONCAT(d.description) as FFCGO,b.name,CONCAT('https://qimg-staging.letote.cn/uploads/photo/', ph.id, '/full_', ph.image) as url" \
                  " FROM   products p,details d,brands b,(select ph.product_id,ph.image,ph.id from photos ph where ph.type='CataloguePhoto') ph" \
                  " WHERE  p.id = d.product_id AND p.brand_id = b.id and p.id = ph.product_id" \
                  " group by p.id,p.description,p.title,b.name,url order by p.id,ph.id;"

}
