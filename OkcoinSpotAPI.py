# codding: utf-8

import requests
from bs4 import BeautifulSoup
import json
#  OKCoinSpot类，提供各种功能的接口。
class OKCoinSpot(object):

    def __init__(self,url,username,password):
        self.__url = url                           # https://www.okcoin.cn
        self.__username =username
        self.__password = password
        self.__session = requests.session()
        self.__header = {
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding':"gzip, deflate, sdch",
            'Accept-Language':"zh-CN,zh;q=0.8",
            'Connection':'keep-alive',
            'Host':"www.okcoin.cn",
            'Referer':"https://www.okcoin.cn/",
            'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36"
        }

    def login(self):  # 登录
        data = {
            'loginName': self.__username,
            'password': self.__password
        }

        try:
            login_url = self.__url+'/user/login/index.do'                          # login url
            self.__session.get(login_url, headers=self.__header)                      # 先get一下，获得一下cookie
            rep = self.__session.post(login_url, data=data, headers=self.__header)    # post 表单
            get_code = json.loads(rep.text)                                           # 返回的数据：{'resultCode': 0, 'errorNum': 0}都是0表示成功，其他都是失败哦！
            # print(get_code)

            resultCode = get_code.get('resultCode')
            errorNum = get_code.get('errorNum')
            if resultCode == 0 and errorNum == 0:
                print('login succeed!')
                return 1
            else:
                print('login failed!')
                return 0
        except requests.RequestException as e:
            print(e)
            print('login failed!')
            return 0

    def account_info(self):  # 账户信息
        trade_url = self.__url + '/trade/btc.do'
        response = self.__session.get(trade_url, headers= self.__header)
        trade_bs = BeautifulSoup(response.text)
        account_info_bs = trade_bs.find('div',{'class': 'accountinfo1'})
        account_info_bs_all = account_info_bs.find('table',{'style': 'border-radius:5px 0 0 0;'})

        asset_net = account_info_bs_all.find('span',{'id':'uNetValue'}).get_text()  # 净资产
        asset_total = account_info_bs_all.find('span',{'id':'tradeValue'}).get_text()  # 总资产
        # print(asset_net,asset_total)

        # {'info': {'funds': {'freezed': {'cny': '0', 'ltc': '0', 'btc': '0'}, 'free': {'cny': '0', 'ltc': '0', 'btc': '0.001'}, 'asset': {'total': '2.81', 'net': '2.81'}}}, 'result': True}
        account_info_bs_details = account_info_bs.find('table',{'class': 'fontsize-12'})
        trs = account_info_bs_details.find_all('tr')
        tr1 = trs[1]   # 可用
        tr2 = trs[2]  # 冻结
        # tr3 = trs[3]
        # tr4 = trs[4]
        # print(tr1)
        free_cny = tr1.find('span',{'id':'trade.available.cny'}).get_text()
        free_btc = tr1.find('span',{'id':'trade.available.btc'}).get_text()
        free_ltc = tr1.find('span',{'id':'trade.available.ltc'}).get_text()
        # print(free_cny,free_btc,free_ltc)
        frozen_cny = tr2.find('span',{'id':'trade.frozen.cny'}).get_text()
        frozen_btc = tr2.find('span',{'id':'trade.frozen.btc'}).get_text()
        frozen_ltc = tr2.find('span',{'id':'trade.frozen.ltc'}).get_text()
        # print(frozen_btc,frozen_cny,frozen_ltc)

        info = {}
        asset = {}
        asset['total'] = asset_total
        asset['net'] = asset_net
        free = {}
        free['cny'] = free_cny
        free['btc'] = free_btc
        free['ltc'] = free_ltc
        frozen = {}
        frozen['cny'] = frozen_cny
        frozen['btc'] = frozen_btc
        frozen['ltc'] = frozen_ltc
        info['asset'] = asset
        info['free'] = free
        info['frozen'] = frozen
        # print(info)
        return info

    def financing_info(self):   # 融资融币信息
        financing_url = self.__url + '/lend/borrows.do?symbol=3&status=1'
        response = self.__session.get(financing_url, headers= self.__header)
        financing_bs = BeautifulSoup(response.text)

        financing_borrow_bs = financing_bs.find('table', {'style':'margin-top:10px;'})
        trs = financing_borrow_bs.find_all('tr')

        financing_top_ten = {} #  存放 借款CNY深度前十名，和 放款CNY深度前十名，
        i = 0
        borrow_top_ten  = {}   #  借款CNY深度前十名，
        for tr in trs:
            i += 1
            top = {}
            if i!= 1:
                tds = tr.find_all('td')
                short_day = tds[0].string
                day_rate = tds[1].string
                borrow_money = tds[2].string
                counts = tds[3].string

                top['short_day'] = short_day
                top['day_rate'] = day_rate
                top['borrow_money'] = borrow_money
                top['counts'] = counts

                borrow_top_ten['top'+str(i-1)] = top
                # print(borrow_top_ten)

        financing_lend_bs = financing_bs.find('div', {'class':'borrowLendBody lendLocation'})
        trs = financing_lend_bs.find_all('tr')
        i = 0

        lend_top_ten = {}   #  放款CNY深度前十名
        for tr in trs:
            i += 1
            top = {}
            if i != 1:
                tds = tr.find_all('td')
                long_day = tds[0].string
                day_rate = tds[1].string
                lend_money = tds[2].string
                counts = tds[3].string
                top['long_day'] = long_day
                top['day_rate'] = day_rate
                top['lend_money'] = lend_money
                top['counts'] = counts

                lend_top_ten['top'+str(i-1)] = top
        # print(lend_top_ten)

        financing_top_ten['borrow_top_ten'] = borrow_top_ten
        financing_top_ten['lend_top_ten']= lend_top_ten
        # print(financing_top_ten)
        return financing_top_ten




if __name__ == '__main__':
    url = 'https://www.okcoin.cn'
    username = '*****@qq.com'
    password = '*******'
    OKCoin_spot = OKCoinSpot(url,username,password)
    OKCoin_spot.login()
    info = OKCoin_spot.account_info()
    print(info)
    # OKCoin_spot.financing_info()



