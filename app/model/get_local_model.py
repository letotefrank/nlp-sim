from fastText import train_unsupervised
import config
import os
import json
import itertools
import pandas as pd
from app.utils.utils import get_vectors

id_url_df = pd.read_csv(os.path.join(config.data_path, 'id_url.csv'))
# fit
model = train_unsupervised(
    # input=os.path.join(config.jb_path, 'pre_data.txt'),
    input=os.path.join(config.jb_path, 'del_dp_text_data.txt'),
    model='skipgram',
    minCount=1
)

model.save_model("{}/local_model.bin".format(config.model_path))

# -------------------为get_with_text服务提供id_vec_dict.json------------
# 得到文本vec
vectors_list = get_vectors(model)
# 组装 id + vec 字典
product_id = id_url_df['id'].values
product_id_list = product_id.tolist()
id_vec_dict = dict(itertools.zip_longest(product_id_list, vectors_list))

# 商品ID,vector持久化为json
with open('{}id_vec_dict.json'.format(config.model_path), 'w') as outfile:
    json.dump(id_vec_dict, outfile)
# -------------------为get_with_text服务提供完毕------------
