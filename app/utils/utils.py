import numpy as np
import pandas as pd
import os, json
import re
import jieba.posseg as jp
import jieba
import config
from translate import Translator
import http.client
import hashlib
from urllib import parse
import random


def translate_baidu(text):
    translation_texts = []
    appid = '20180912000205859'
    secretKey = 'QwG4h94r1ugVXtfPlIF7'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    # q = 'black,hello'
    fromLang = 'en'
    toLang = 'zh'
    salt = random.randint(32768, 65536)

    text_list = text.split(',')
    for t in text_list:
        sign = appid + t + str(salt) + secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode(encoding='utf-8'))
        sign = m1.hexdigest()

        myurl = myurl + '?appid=' + appid + '&q=' + parse.quote(
            t) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            str1 = response.read().decode('utf-8')
            str1 = eval(str1)
            for line in str1['trans_result']:
                translated = line['dst']
                if translated == '金':
                    translated = '金色'
                elif translated == '银':
                    translated = '银色'
                elif translated == '奶油':
                    translated = '奶油色'
                else:
                    translated = translated

            translation_texts.append(translated)
        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()
    return translation_texts


def translate_google(text):
    translation_texts = []
    text_list = text.split(',')
    translator = Translator(to_lang="zh")
    for t in text_list:
        result = translator.translate(t)
        translation_texts.append(result)
    return translation_texts


def translate_color(color_df):
    translated_color = []
    for index, row in color_df.items():
        color = row.lower()
        trans_color = translate_baidu(color)
        translated_color.append(trans_color)
    color_df = pd.DataFrame(np.array(translated_color))
    return color_df


def jb_text(raw_line, stopwords):
    """
        处理文本数据
        返回分词结果
    """

    # 1. 使用正则表达式去除非中文字符
    filter_pattern = re.compile('[^\u4E00-\u9FD5]+')
    chinese_only = filter_pattern.sub('', raw_line)

    # 2. 结巴分词+词性标注
    jieba.add_word('无弹力')
    word_list = jp.cut(chinese_only)

    # 3. 去停用词，保留有意义的词性
    used_flags = ['a', 'n', 'nr', 'v', 'nz', 'x', 't']
    meaninful_words = []
    for word, flag in word_list:
        if (word not in stopwords) and (flag in used_flags):
            meaninful_words.append(word)

    # 去重复的词语
    # duplicate_list = list(set(meaninful_words))
    # duplicate_list.sort(key=meaninful_words.index)

    return ' '.join(meaninful_words)  # 分词后，词语连接方式为空格 ' '
    # return ' '.join(duplicate_list)  # 分词后，词语连接方式为空格 ' '


def stop_words():
    # 加载停用词表
    stopwords1 = [line.rstrip() for line in open(os.path.join(config.stop_words_path, '中文停用词库.txt'), 'r',
                                                 encoding='utf-8')]
    stopwords2 = [line.rstrip() for line in open(os.path.join(config.stop_words_path, '哈工大停用词表.txt'), 'r',
                                                 encoding='utf-8')]
    stopwords3 = [line.rstrip() for line in
                  open(os.path.join(config.stop_words_path, '四川大学机器智能实验室停用词库.txt'), 'r', encoding='utf-8')]
    return stopwords1 + stopwords2 + stopwords3


def similarity(v1, v2):
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    return np.dot(v1, v2) / n1 / n2


def get_vectors(model1):
    vectors = []
    with open(os.path.join('{}pre_data.txt'.format(config.jb_path))) as f:
        for line in f:
            line = line.replace('\n', '')
            vector = model1.get_sentence_vector(line)
            vectors.append(vector.tolist())
    return vectors


def get_sims(id_vec_dict1, id_url_df1, sim_num, pid):
    sims = []
    for iv in id_vec_dict1:
        sim = similarity(id_vec_dict1[pid], id_vec_dict1[iv])
        sims.append(sim)
    dict_d = {'sim_data': sims}
    sims_df = pd.DataFrame(dict_d)
    df = id_url_df1.join(sims_df)
    df = df.sort_values(by=['sim_data'], ascending=False)
    df = df.reset_index(drop=True)
    pids = df.iloc[0:sim_num]['id'].values.tolist()
    urls = df.iloc[0:sim_num]['url'].values.tolist()
    results = [pids, urls]
    return results


def del_sentence_with_word(id_row, desc_row, del_dp_texts):
    # def del_sentence_with_word(id_row, desc_row, color_row, del_dp_texts):
    word = '搭配'
    del_sentence = re.findall(r'[^，。]*?{}[^，。]*?，'.format(word), desc_row)
    # description_deleted = str(id_row) + str(color_row) + desc_row
    description_deleted = str(id_row) + desc_row
    if del_sentence.__len__():
        for i in range(len(del_sentence)):
            del_sentence_str = del_sentence[i]
            description_deleted = description_deleted.replace(del_sentence_str, '')

        del_dp_texts.append(description_deleted)
    else:
        del_dp_texts.append(description_deleted)

    return del_dp_texts, description_deleted


def del_sentence_word(texts):
    word = '搭配'
    del_sentence = re.findall(r'[^，。]*?{}[^，。]*?，'.format(word), texts)
    text_deleted = texts
    if del_sentence.__len__():
        for i in range(len(del_sentence)):
            del_sentence_str = del_sentence[i]
            text_deleted = text_deleted.replace(del_sentence_str, '')
    else:
        text_deleted = texts
    return text_deleted
