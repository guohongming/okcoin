 # def borrow_lend_info(self):参数  无
 # 返回值说明 （人民币借款（已借款，正在申请的借款，可申请的借款，借款风险），btc借款（同前），ltc借款（同前））
# 示例：
{
    'cny_borrow':  # 人民币借款
        {
            'borrow_done': '0',       #已借款
            'borrow_danger': '暂无', # 正在申请的借款
            'borrow_apply': '0',       # 可申请的
            'borrow_available': '401.55',# 风险
            'daliyRade':'0.1%'
        },
    'ltc_borrow': # btc 借款
        {
            'borrow_done': '0',
            'borrow_danger': '暂无',
            'borrow_apply': '0',
            'borrow_available': '19.51',
            'daliyRade':'0.1%'
        },
    'btc_borrow': # ltc借款
        {
            'borrow_done': '0',
            'borrow_danger': '暂无',
            'borrow_apply': '0',
            'borrow_available': '0.15',
            'daliyRade':'0.1%'
        }
}
