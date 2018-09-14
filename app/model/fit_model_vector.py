from fastText import train_unsupervised
import config
import os
import json
import itertools
from app.model.data_process import data_process


def fit():
    '''
    fastText训练语料库,save:local_model.bin；利用 预处理和分词 后的pre_data.txt 训练 sentence-vector
    :return: fit result
    '''
    # 数据预处理。返回 id_url_df 用于结果拼接（id,url）
    id_url_df = data_process()
    print('fit 数据预处理，分词完成')

    # fastText fit
    model = train_unsupervised(
        # input=os.path.join(config.jb_path, 'pre_data.txt'),
        input=os.path.join(config.jb_path, 'del_dp_text_data.txt'),
        model='skipgram',
        epoch=10,
        dim=300,
        # pretrainedVectors="{}/wiki.zh.vec".format(config.model_path),
        minCount=1
    )

    model.save_model("{}/local_model.bin".format(config.model_path))
    print('local_model.bin  saved')

    vector_list = []
    with open(os.path.join('{}pre_data.txt'.format(config.jb_path))) as f:
        for line in f:
            line = line.replace('\n', '')
            vector = model.get_sentence_vector(line)
            vector_list.append(vector.tolist())

    # 组装 pid + vec 字典
    pid = id_url_df['id'].values
    pid_list = pid.tolist()
    id_vec_dict = dict(itertools.zip_longest(pid_list, vector_list))

    # pid,vector持久化为json
    with open('{}id_vec_dict.json'.format(config.model_path), 'w') as outfile:
        json.dump(id_vec_dict, outfile)
        print('id_vec_dict.json 持久化完成')

    return 'fit success!!!'
