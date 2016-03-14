# codding: utf-8
from OkcoinSpotAPI import OKCoinSpot

url = 'https://www.okcoin.cn'
username = '1006575211@qq.com'
password = 'guo1006575211'
trade_pwd = 'guohongming03'
OKCoin_spot = OKCoinSpot(url,username,password)
if OKCoin_spot.login() == 1:
    print('login success!')
else:
    print('login failed!')

# account_info = OKCoin_spot.account_info() # 账户信息
# print(account_info)

# financing_info = OKCoin_spot.financing_info() # 融资融币借放款深度前10名。
# print(financing_info)

# borrow_info = OKCoin_spot.borrow_lend_info() # 借款信息（人民币，btc，ltc）
# print(borrow_info)

trade_value = (OKCoin_spot.trade_value()) # 最新交易价格
print(trade_value)

# borrow_cny_apply = OKCoin_spot.borrow_cny_apply(100) # 申请人民币借款
# print(borrow_cny_apply)

# back_cny = OKCoin_spot.back_cny()      # 人民币还款
# print(back_cny)

# 买入ltc
'''
buy_ltc_result = OKCoin_spot.buy_ltc(1,trade_pwd)
if buy_ltc_result == 1:
    print('buy ltc trade success!')
else:
    print('buy ltc trade failed!')
'''

# 卖出ltc
'''
sell_ltc_result = OKCoin_spot.sell_ltc(0.1,trade_pwd)
if sell_ltc_result == 1:
    print('sell ltc trade success!')
else:
    print('sell ltc trade failed!')
'''