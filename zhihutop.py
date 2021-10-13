import requests
import json
import time
import pandas as pd
import schedule


class ZhihuTop(object):
    def __init__(self):
        # 知乎api地址
        self.url = 'https://api.zhihu.com/topstory/hot-lists/total?limit=10'
        self.headers = {
            'Host': 'api.zhihu.com',
            'User-Agent': 'com.zhihu.android/Futureve/7.30.0 Mozilla/5.0 (Linux; Android 10; MI 8 UD Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/93.0.4577.82 Mobile Safari/537.36'
        }

    def get_data(self):
        # 使用get方法获取数据
        response = requests.get(self.url, headers=self.headers, timeout=5).content.decode()
        # 转换为json格式
        tops = json.loads(response)['data']
        return tops

    def parse_data(self, tops):
        # 新建空列表准备存入数据
        top_list = []
        print('正在获取数据....请稍等')
        try:
            for top in tops:
                temp = {}
                # 转换成日期
                timestamp = top['target']['created']
                timearr = time.localtime(timestamp)
                time_date = time.strftime("%Y-%m-%d %H:%M:%S", timearr)
                # 信息
                temp['标题'] = top['target']['title']
                temp['回答数'] = top['target']['answer_count']
                temp['关注人数'] = top['target']['follower_count']
                temp['评论数'] = top['target']['comment_count']
                temp['热度'] = top['detail_text']
                temp['话题创建时间'] = str(time_date)
                top_list.append(temp)
            print('数据获取成功！')
        except Exception as ep:
            print('数据获取失败！' + '错误:' + str(ep))
        # 数据添加到pandas
        df = pd.DataFrame(top_list)
        return df

    def save(self, df):
        name = str(time.strftime("%Y%m%d%H%M%S"))
        try:
            df.index = (df.index + 1)
            df.index.name = 'Top'
            df.to_csv(name + '.csv', encoding='utf_8_sig')
            print('保存成功，文件名为:{}.csv'.format(name))
        except Exception as ep:
            print('数据获取失败！' + '错误:' + str(ep))

    def main(self):
        tops = self.get_data()
        self.parse_data(tops)
        df = self.parse_data(tops)
        self.save(df)


if __name__ == '__main__':
    zhihutop = ZhihuTop()
    zhihutop.main()
    schedule.every(1).day.do(zhihutop.main)
    while True:
        schedule.run_pending()
        time.sleep(1)