import pandas as pd
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant
import time
import random

def add_stock_suffix(stock_code):
    """
    为给定的股票代码添加相应的后缀。
    """
    # 检查股票代码是否为6位数字
    if len(stock_code) != 6 or not stock_code.isdigit():
        raise ValueError("股票代码必须是6位数字")

    # 根据股票代码的前缀添加相应的后缀
    if stock_code.startswith("00") or stock_code.startswith("30") or stock_code.startswith("15") or stock_code.startswith("16") or stock_code.startswith("18") or stock_code.startswith("12"):
        return f"{stock_code}.SZ"  # 深圳证券交易所
    elif stock_code.startswith("60") or stock_code.startswith("68") or stock_code.startswith("11"):
        return f"{stock_code}.SH"  # 上海证券交易所
    elif stock_code.startswith("83") or stock_code.startswith("43"):
        return f"{stock_code}.BJ"  # 北京证券交易所
    
    return f"{stock_code}.SH"

class MyXtQuantTraderCallback(XtQuantTraderCallback):
    def on_disconnected(self):
        """
        连接状态回调
        :return:
        """
        print("connection lost")
    def on_stock_order(self, order):
        """
        委托信息推送
        :param order: XtOrder对象
        :return:
        """
        print(f"【委托】 订单编号:{order.order_id} 代码:{order.stock_code} 委托价格:{order.price} 委托数量:{order.order_volume} 委托时间:{order.order_time}")
    def on_stock_trade(self, trade):
        """
        成交信息推送
        :param trade: XtTrade对象
        :return:
        """
        print(f"【成交】 成交编号:{trade.order_id} 代码:{trade.stock_code} 成交价格:{trade.traded_price} 成交数量:{trade.traded_volume} 成交时间:{trade.traded_time}")

# 自定义函数处理格式不正确的行
def handle_bad_lines(bad_line):
    # 将 "新 和 成" 替换为 "新和成"
    stock_list = ['新 和 成', '五 粮 液']
    fixed_line = ' '.join(bad_line)
    for stock in stock_list:
        fixed_stock = stock.replace(' ', '')
        fixed_line = fixed_line.replace(stock, fixed_stock)
    
    # 检查修复后的行是否符合预期格式
    fields = fixed_line.split()
    if len(fields) == 8:
        return fields
    else:
        print(f"错误行: {' '.join(bad_line)}")
        return None  # 返回 None 表示跳过该行

def read_file(file_path):
    COLUMNS = ['code', 'name', 'date', 'time', 'price', 'rate', 'value', 'sign']
    try:
        # 检查文件是否为空
        with open(file_path, 'r', encoding='gb2312') as file:
            first_line = file.readline()
            if not first_line:  # 文件为空
                return pd.DataFrame(columns=COLUMNS)
        
        df = pd.read_csv(file_path, sep=r'\s+', header=None, encoding='gb2312', on_bad_lines=handle_bad_lines, engine='python', dtype={0: str})
        df.columns = COLUMNS
        return df
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None

def clear_file_content(file_path):
    try:
        with open(file_path, 'w', encoding='gb2312') as file:
            file.truncate(0)
        print("文件内容已清空")
    except Exception as e:
        print(f"清空文件内容时发生错误: {e}")

def create_trader(account_id, mini_qmt_path):
    # 创建session_id
    session_id = int(random.randint(100000, 999999))
    # 创建交易对象
    xt_trader = XtQuantTrader(mini_qmt_path, session_id)
    # 启动交易对象
    xt_trader.start()
    # 连接客户端
    connect_result = xt_trader.connect()

    if connect_result == 0:
        print('连接成功')

    # 创建账号对象
    account = StockAccount(account_id)
    # 订阅账号
    xt_trader.subscribe(account)
    # 注册回调类
    xt_trader.register_callback(MyXtQuantTraderCallback())

    return xt_trader, account

def start(account_id, mini_qmt_path, file_path, buy_sign, sell_sign, buy_event, sell_event, interval=1):

    xt_trader, account = create_trader(account_id, mini_qmt_path)

    print(xt_trader, account)

    previous_df = None

    # 启动前清空文件内容
    clear_file_content(file_path)

    while True:
        current_df = read_file(file_path)
        if current_df is not None:
            if previous_df is not None:
                # 比较前后两次读取的 DataFrame，找出新增的行
                new_rows = current_df[~current_df.index.isin(previous_df.index)]
                if not new_rows.empty:
                    for index, row in new_rows.iterrows():

                        stock_code = add_stock_suffix(row['code'])

                        price_type_map = {
                            '市价': xtconstant.LATEST_PRICE,
                            '限价': xtconstant.FIX_PRICE
                        }
                        
                        if row['sign'] == buy_sign:
                            buy_paload = buy_event(row, xt_trader)
                            xt_trader.order_stock_async(
                                account=account, 
                                stock_code=stock_code, 
                                order_type=xtconstant.STOCK_BUY, 
                                order_volume=buy_paload.get('size') or 100, 
                                price_type=price_type_map.get(buy_paload.get('type')) or xtconstant.LATEST_PRICE,
                                price=buy_paload.get('price') or -1,
                            )
                        elif row['sign'] == sell_sign:
                            position = xt_trader.query_stock_position(account, stock_code)
                            sell_paload = sell_event(row, position, xt_trader)
                            if position is not None:
                                xt_trader.order_stock_async(
                                    account=account, 
                                    stock_code=stock_code, 
                                    order_type=xtconstant.STOCK_SELL, 
                                    order_volume=sell_paload.get('size') or position.can_use_volume, 
                                    price_type=price_type_map.get(sell_paload.get('type')) or xtconstant.LATEST_PRICE,
                                    price=sell_paload.get('price') or -1,
                                )
                    
            previous_df = current_df
        
        time.sleep(interval)

if __name__ == '__main__':
    # 参数
    account_id = '55003152' # 账号ID
    mini_qmt_path = r'D:\国金QMT交易端模拟\userdata_mini' # mini_qmt 路径
    file_path = r'D:\new_tdx\sign.txt' # 预警文件路径
    interval = 1 # 轮询时间(秒)
    buy_sign = 'KDJ买入条件选股' # 买入信号
    sell_sign = 'KDJ卖出条件选股' # 卖出信号

    def buy_event(row, xt_trader):
        '''买入数量'''
        return 100
    
    def sell_event(row, position, xt_trader):
        '''卖出数量'''
        return 100 # position.can_use_volume


    start(
        account_id=account_id,
        mini_qmt_path=mini_qmt_path,
        file_path=file_path,
        interval=interval,
        buy_sign=buy_sign,
        sell_sign=sell_sign,
        buy_event=buy_event,
        sell_event=sell_event
    )