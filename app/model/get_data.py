import pandas as pd
import pymysql
import config
from sshtunnel import SSHTunnelForwarder


def get_data_db():
    """
    连接数据库，获取初始数据集
    :return: data_list[]
    """
    global results
    with SSHTunnelForwarder(
            ('54.223.128.196', 11690),  # 指定ssh登录的跳转机的address
            ssh_username="ubuntu",  # 跳转机的用户
            ssh_pkey="/Users/letote/.ssh/id_rsa",
            ssh_private_key_password="qweasd",
            remote_bind_address=(
                    'staging-mysql.czqjl6kiyvxa.rds.cn-north-1.amazonaws.com.cn', 3306)) as server:  # A机器的配置

        db = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                             port=server.local_bind_port,
                             user='ltstaging',
                             passwd='Lt123456',
                             db='letote_staging')
        data_list = []

        with db:
            cursor = db.cursor()
            for sql_name, sql in config.sql_dict.items():
                # print(sql)
                try:
                    # 执行 SQL 查询
                    cursor.execute(sql)
                    # 获取所有记录列
                    results = cursor.fetchall()
                    data_df = pd.DataFrame(list(results),
                                           columns=['id', 'iid', 'image', 'description', 'title', 'FFCGO', 'name',
                                                    'url'])
                except Exception as e:
                    print(e)
        return data_df
