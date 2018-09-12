import numpy as np
import config
from app.model.get_data import get_data_db
from app.utils.utils import stop_words, jb_text, del_sentence_with_word


def pre_process(data):
    # 处理nan,删除包含nan的行
    data_df = data.dropna()
    # 去掉单元格前后的空格
    data_df['description'] = data_df['description'].map(str.strip)
    data_df['title'] = data_df['title'].map(str.strip)
    data_df['FFCGO'] = data_df['FFCGO'].map(str.strip)
    data_df['name'] = data_df['name'].map(str.strip)
    data_df['url'] = data_df['url'].map(str.strip)

    # 每个商品只保留一个图片url,所以去重
    data_df = data_df.drop_duplicates(subset=['id'], keep='first')
    # 重新构建索引
    data_df = data_df.reset_index(drop=True)
    # 翻译color
    # color_df = translate_color(data_df['color'])
    # data_df['color'] = color_df
    data_df.to_csv('{}/data_df.csv'.format(config.data_path), index=False, encoding='utf-8')
    return data_df


def fit_data():
    # 连接mysql,得到数据
    data = get_data_db()

    # 数据预处理（去nan，去重，英文数据的翻译）
    data_df = pre_process(data)

    # 存放需nlp的字段数据
    pre_data = []
    del_dp_texts = []

    # 用于结果拼接的 dataframe
    id_url_df = data_df[['id', 'url', 'title', 'FFCGO', 'name', 'description']]
    id_url_df.to_csv('{}/id_url.csv'.format(config.data_path), index=False, encoding='utf-8')

    for index, row in data_df.iterrows():
        # 删除含有 '搭配'的短语
        del_dp_texts, description_deleted = del_sentence_with_word(row['id'], row['description'], del_dp_texts)

        text = row['title'] + row['FFCGO'] + row['name'] + row['url'] + description_deleted

        # 加载停用词表
        stopwords = stop_words()

        # jieba处理（分词，词性提取，去停用词)
        pre_data.append(jb_text(text, stopwords))

    # 待model训练的数据
    np.savetxt('{}del_dp_text_data.txt'.format(config.jb_path), np.array(del_dp_texts), fmt='%s')

    # 分词结果，并用于得到文本特征向量的输入
    np.savetxt('{}pre_data.txt'.format(config.jb_path), np.array(pre_data), fmt='%s')

    print('fit success!')
    # return 'fit success！！！'


fit_data()
