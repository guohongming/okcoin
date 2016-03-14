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
                # print('login succeed!')
                return 1
            else:
                # print('login failed!')
                return 0
        except requests.RequestException as e:
            # print(e)
            # print('login failed!')
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

    def borrow_lend_info(self):
        my_borrow_info = {}
        borrow_lend_cny_url = self.__url+'/lend/borrows.do?symbol=3&rd=1&status=1'
        bs_cny = BeautifulSoup(self.__session.get(borrow_lend_cny_url,headers=self.__header).text)
        borrow_lend_btc_url = self.__url+'/lend/borrows.do?symbol=1&rd=1&status=0'
        bs_btc = BeautifulSoup(self.__session.get(borrow_lend_btc_url,headers=self.__header).text)
        borrow_lend_ltc_url = self.__url+'/lend/borrows.do?symbol=2&rd=1&status=0'
        bs_ltc = BeautifulSoup(self.__session.get(borrow_lend_ltc_url,headers=self.__header).text)

        # cny borrow

        bs_cny_borrow = bs_cny.find('div',{'class':"borrowInfo"})
        borrows_cny = bs_cny_borrow.find_all('p')
        # print(borrows_cny)
        borrow_done = borrows_cny[0].span.string.strip()
        borrow_apply = borrows_cny[1].span.string.strip()
        borrow_available = borrows_cny[2].span.string.strip()
        borrow_danger = borrows_cny[3].get_text().strip()
        daliyRade = bs_cny.find('span',{'id':"loanFixedRate",'style':"display: "}).string
        cny_borrow = {}
        cny_borrow['borrow_done'] = borrow_done
        cny_borrow['borrow_apply'] = borrow_apply
        cny_borrow['borrow_available'] = borrow_available
        cny_borrow['borrow_danger'] = borrow_danger
        cny_borrow['daliyRade'] = daliyRade
        my_borrow_info['cny_borrow'] = cny_borrow


        # btc borrow

        bs_btc_borrow = bs_btc.find('div',{'class':"borrowInfo"})
        borrows_btc = bs_btc_borrow.find_all('p')
        # print(borrows_btc)
        borrow_done = borrows_btc[0].span.string.strip()
        borrow_apply = borrows_btc[1].span.string.strip()
        borrow_available = borrows_btc[2].span.string.strip()
        borrow_danger = borrows_btc[3].get_text().strip()
        daliyRade = bs_btc.find('span',{'id':"loanFixedRate",'style':"display: "}).string
        btc_borrow = {}
        btc_borrow['borrow_done'] = borrow_done
        btc_borrow['borrow_apply'] = borrow_apply
        btc_borrow['borrow_available'] = borrow_available
        btc_borrow['borrow_danger'] = borrow_danger
        btc_borrow['daliyRade'] = daliyRade
        my_borrow_info['btc_borrow'] = btc_borrow


        # ltc borrow

        bs_ltc_borrow = bs_ltc.find('div',{'class':"borrowInfo"})
        borrows_ltc = bs_ltc_borrow.find_all('p')
        # print(borrows_ltc)
        borrow_done = borrows_ltc[0].span.string.strip()
        borrow_apply = borrows_ltc[1].span.string.strip()
        borrow_available = borrows_ltc[2].span.string.strip()
        borrow_danger = borrows_ltc[3].get_text().strip()
        daliyRade = bs_ltc.find('span',{'id':"loanFixedRate",'style':"display: "}).string
        ltc_borrow = {}
        ltc_borrow['borrow_done'] = borrow_done
        ltc_borrow['borrow_apply'] = borrow_apply
        ltc_borrow['borrow_available'] = borrow_available
        ltc_borrow['borrow_danger'] = borrow_danger
        ltc_borrow['daliyRade'] = daliyRade
        my_borrow_info['ltc_borrow'] = ltc_borrow

        return my_borrow_info

    def borrow_cny_apply(self,amount):  # 人民币申请借款
        borrow_cny_url = self.__url+'/lend/submitLend.do'
        try:
            rate = self.borrow_lend_info().get('cny_borrow').get('daliyRade').replace('%','')
            print(rate)
            data = {
                'amount':amount,
                'rate':rate,
                'ratefee':"0",
                'days':"2",
                'type':"1",
                'symbol':"3",
                'ispre':"0"
            }
            response = self.__session.get(borrow_cny_url)
            response = self.__session.post(borrow_cny_url,data = data,headers = self.__header)
            # print(response.text)
            if response.text != '':
                return 1
            else:
                return 0
        except:
            return 0

    def back_cny(self):        # 人民币还款
        back_cny_url = self.__url+ '/lend/borrows.do?symbol=3&rd=2&status=1'
        back_cny_url_post = self.__url+'/lend/backPayLend.do'
        try:
            rep = BeautifulSoup(self.__session.get(back_cny_url).text).find('div',{'class':"Record"})
            id = rep.find('td').get_text()
            # print(id)
            money = rep.find('td',{'style':"font-weight: bold;"}).get_text().replace('￥','')
            # print(money)
            data = {
                'id':id,
                'symbol':"3",
                'money':money,
                'type':"1"
            }
            response = self.__session.get(back_cny_url_post)
            response = self.__session.post(back_cny_url_post,data = data,headers = self.__header)
            # print(response.text)
            if response.text == '0':
                return 1
            else:
                return 0
        except:
            return 0

    def trade_value(self):      # 当前交易价格
        trade_value_url = self.__url+'/trade/btc.do'
        response = self.__session.get(trade_value_url,headers=self.__header)
        trade_value_bs = BeautifulSoup(response.text)
        trade_value_bs = trade_value_bs.find('ul',{'style':'padding-left:0px;'})
        # print(trade_value_bs)
        bannerBtcLast = trade_value_bs.find('span',{'id':'bannerBtcLast'}).get_text()
        bannerLtcLast = trade_value_bs.find('span',{'id':'bannerLtcLast'}).get_text()

        bannerBtcVol = trade_value_bs.find('span',{'id':'bannerBtcVol'}).get_text()
        bannerLtcVol = trade_value_bs.find('span',{'id':'bannerLtcVol'}).get_text()

        trade_value = {}
        last_value = {}
        trade_amount_24 = {}
        last_value['bannerBtcLast'] = bannerBtcLast
        last_value['bannerLtcLast'] = bannerLtcLast
        trade_amount_24['bannerBtcVol'] = bannerBtcVol
        trade_amount_24['bannerLtcVol'] = bannerLtcVol
        trade_value['last_value'] = last_value
        trade_value['trade_amount_24'] = trade_amount_24
        # print(trade_value)
        return  trade_value

    def buy_ltc(self, tradeAmount = 0, tradepassword = None ):   # 买入莱特币，参数（数量，交易密码）
        buy_ltc_url = self.__url+'/trade/buyBtcSubmit.do'
        tradeCnyPrice = self.trade_value().get('last_value').get('bannerLtcLast')
        data = {
            'tradeAmount':tradeAmount,
            'tradeCnyPrice':tradeCnyPrice,
            'tradePwd':tradepassword,
            'symbol':"1",
            'limited':"0"
        }
        response = self.__session.get(buy_ltc_url)
        response = self.__session.post(buy_ltc_url, data=data, headers=self.__header)
        response_code = json.loads(response.text)

        resultCode = response_code.get('resultCode')
        errorNum = response_code.get('errorNum')
        if resultCode == 0 and errorNum == 0:
            # print('trade succeed!')
            return 1
        else:
            # print('trade failed')
            return 0

    def sell_ltc(self,tradeAmount = 0, tradepassword = None ):  #卖出ｌｔｃ 参数：卖出数量，交易密码
        sell_ltc_url = self.__url + '/trade/sellBtcSubmit.do'
        tradeCnyPrice = self.trade_value().get('last_value').get('bannerLtcLast')
        data = {
            'tradeAmount':tradeAmount,
            'tradeCnyPrice':tradeCnyPrice,
            'tradePwd':tradepassword,
            'symbol':"1",
            'limited':"0"

        }
        response = self.__session.get(sell_ltc_url)
        response = self.__session.post(sell_ltc_url,data = data, headers = self.__header)
        response_code = json.loads(response.text)
        resultCode = response_code.get('resultCode')
        errorNum = response_code.get('errorNum')
        if resultCode == 0 and errorNum == 0:
            # print('trade succeed!')
            return 1
        else:
            # print('trade failed')
            return 0














