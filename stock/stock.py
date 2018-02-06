import tushare as ts

stock_list = ts.get_stock_basics()
stock_list.to_csv('stock_list.csv')

stock_code_list = list(stock_list.index)

for code in stock_code_list:
    his = ts.get_k_data(code, start='2018-01-01', end='2018-02-06')
    his.to_csv('./his/' + code + '.csv')

