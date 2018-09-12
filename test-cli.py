import requests
import json, time

# # nlp_rec参数
req_data = {
    # 2880,3633，3661
    # 3560,3549
    'pid': 3633,
    'rec_num': 300,
    'end_flag': 0
}
#
req_text = {
    'text': '轻薄又亲肤的雪纺裙带有透视感，藕粉色的底色和花卉印花透着春天的气息。轻盈的材质让不规则的裙摆展现出它的飘逸多姿。腰间的束腰设计为你打造完美比例"'
            '"层叠下摆印花连衣裙""Fabric:100%聚酯纤维,Color: PinkPurpleFit:宽松微弹力,Origin: Imported"'
            '"SUMMER & SAGE","https://qimg-staging.letote.cn/uploads/photo/19333/full_559A3569.jpg_2x3.jpg',
    'rec_num': 100
}
#
start = time.time()
print('nlp_text 请求中。。。')
fit = requests.get(url='http://10.0.1.41:8081/fit_data')
# fit = requests.get(url='http://52.83.166.134:5000/query?image_name=13_1354_I03A7729.JPG_2x3.jpg&k=100')
# nr = requests.post(url='http://10.0.1.41:8081/sim_by_pid', data=json.dumps(req_data))
# nt = requests.post(url='http://10.0.1.41:8081/sim_by_text', data=json.dumps(req_text))
# print(fit.text)
# # print(nr.text)
# print(nt.text)
end = time.time()
print('request Running time: %s Seconds' % (end - start))
