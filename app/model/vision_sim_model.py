import requests
import pandas as pd
import os
import config
import re

# str_a = '4043_23455_BHLA185001.jpg'
# s = str_a.split('_')

data_df = pd.read_csv(os.path.join(config.data_path, 'data_df.csv'))


# pid = 13
# iid = data_df[data_df['id'] == pid].values.tolist()[0]
# image = data_df[data_df['id'] == pid].values.tolist()[0][2]


# http://52.83.166.134:5000/query?image_name=4043_23455_BHLA185001.jpg&k=100

def vision_sim(pid, sim_num):
    # pid = 13
    pids = []
    urls = []
    iid = data_df[data_df['id'] == pid].values.tolist()[0][1]
    image = data_df[data_df['id'] == pid].values.tolist()[0][2]
    address = 'http://52.83.166.134:5000/query' + '?' + 'image_name=' + str(pid) + '_' + str(
        iid) + '_' + image + '&' + 'k=' + str(sim_num)
    # print(address)

    print('vision_sim 请求中。。。')
    req_vision = requests.get(url=address)

    sim_str = req_vision.text
    sim_list = sim_str.split(',')
    # sim_list = ['4043_23455_59A3508.jpg_2x3.jpg'] * 100

    for image_name in sim_list:
        sp = image_name.split('_')
        # pid_str = sp[0]
        # pid = re.findall('\d+', pid_str)
        img_id = int(sp[1])
        print(img_id)
        find_result = data_df[data_df['iid'] == img_id].values.tolist()
        if find_result.__len__():
            pid = find_result[0][0]
            url = find_result[0][7]
            # print(url)
            pids.append(pid)
            urls.append(url)
        else:
            print(address)
            continue
    return pids, urls

# qst = vision_sim()
