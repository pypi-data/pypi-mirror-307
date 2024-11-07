from futu import *
from time import sleep
from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame
from ks_trade_api.utility import extract_vt_symbol, generate_vt_symbol
from ks_trade_api.constant import (
    CHINA_TZ, US_EASTERN_TZ,
    Exchange as KsExchange, Product as KsProduct, SubscribeType as KsSubscribeType,
    RetCode as KsRetCode, RET_OK as KS_RET_OK, RET_ERROR as KS_RET_ERROR, ErrorCode as KsErrorCode,
    Interval as KsInterval, Adjustment as KsAdjustment
)
from ks_trade_api.object import (
    ErrorData, ContractData, MyTickData, MyBookData, MyRawTickData, QuoteData, BarData
)
from ks_utility import datetimes
from decimal import Decimal
from dateutil.parser import parse
from ks_trade_api.base_market_api import BaseMarketApi
from typing import Optional, Union, List
from logging import DEBUG, INFO, WARNING, ERROR
from futu.common.open_context_base import ContextStatus

PRODUCT_MY2KS = {
    SecurityType.STOCK: KsProduct.EQUITY,
    SecurityType.DRVT: KsProduct.OPTION
}

RET_KS2MY = {
    KS_RET_OK: RET_OK,
    KS_RET_ERROR: RET_ERROR
}

RET_MY2KS = { v:k for k,v in RET_KS2MY.items() }

MARKET_KS2MY = {
    KsExchange.SEHK: TrdMarket.HK,
    KsExchange.SMART: TrdMarket.US 
}

MARKET_MY2KS = { v:k for k,v in MARKET_KS2MY.items() }

PRODUCT_KS2MY = {
    KsProduct.EQUITY: SecurityType.STOCK,
    KsProduct.OPTION: SecurityType.DRVT,
    KsProduct.ETF: SecurityType.ETF
}
PRODUCT_MY2KS = { v:k for k,v in PRODUCT_KS2MY.items() }

def symbol_ks2my(vt_symbol: str):
    if not vt_symbol:
        return ''
    symbol, ks_exchange = extract_vt_symbol(vt_symbol)
    return f'{MARKET_KS2MY.get(ks_exchange)}.{symbol}'

def symbol_my2ks(my_symbol: str):
    if not my_symbol:
        return ''
    symbol, ks_exchange = extract_my_symbol(my_symbol)
    return generate_vt_symbol(symbol, ks_exchange)

SUBTYPE_KS2MY = {
    KsSubscribeType.USER_ORDER: KsSubscribeType.USER_ORDER,
    KsSubscribeType.USER_TRADE: KsSubscribeType.USER_TRADE,
    KsSubscribeType.USER_POSITION: KsSubscribeType.USER_POSITION,
    KsSubscribeType.TRADE: SubType.TICKER,
    KsSubscribeType.BOOK: SubType.ORDER_BOOK,
    
    KsSubscribeType.K_MINUTE: SubType.K_1M,
    KsSubscribeType.K_HOUR: SubType.K_60M,
    KsSubscribeType.K_DAILY: SubType.K_DAY
}

ADJUSTMENT_KS2MY = {
    KsAdjustment.BACKWARD_ADJUSTMENT: AuType.QFQ,
    KsAdjustment.FORWARD_ADJUSTMENT: AuType.HFQ,
    KsAdjustment.NONE: AuType.NONE
}

INTERVAL_KS2MY = {
    KsInterval.MINUTE: KLType.K_1M,
    KsInterval.HOUR: KLType.K_60M,
    KsInterval.DAILY: KLType.K_DAY,
    KsInterval.WEEKLY: KLType.K_WEEK
}

EXCHANGE2TZ = {
    KsExchange.SEHK: CHINA_TZ,
    KsExchange.SMART: US_EASTERN_TZ
}

def extract_my_symbol(my_symbol: str):
    items = my_symbol.split('.')
    return '.'.join(items[1:]), MARKET_MY2KS.get(items[0])

def get_tz(vt_symbol: str):
    symbol, exchange = extract_vt_symbol(vt_symbol)
    return EXCHANGE2TZ.get(exchange)

class TimeoutException(Exception):
    def __init__(self, message: str, timeout: int):
        super().__init__(message)
        self.timeout = timeout


class KsFutuMarketApi(BaseMarketApi):
    gateway_name: str = 'KS_FUTU'

    def __init__(self, setting: dict):
        security_firm = setting.get('security_firm')
        self.port = setting.get('port', 11111)
        self.timeout = setting.get('timeout', 60)
        gateway_name = setting.get('gateway_name', self.gateway_name)
        dd_secret = setting.get('dd_secret')
        dd_token = setting.get('dd_token')
        super().__init__(gateway_name=gateway_name, dd_secret=dd_secret, dd_token=dd_token)

        self.init_handlers(security_firm)


    # 初始化行回调和订单回调
    def init_handlers(self, security_firm):
        trade = self

        connect_start = datetime.now()
        self.quote_ctx = quote_ctx = OpenQuoteContext(host='127.0.0.1', port=self.port, is_async_connect=True)
        while True:
            if self.quote_ctx._status == ContextStatus.READY:
                self.log('Futu OpenD连接成功')
                break
            if (datetime.now() - connect_start).seconds > self.timeout:
                self.quote_ctx.close()
                raise TimeoutException('OpenQuoteContext连接超时，请检查Futu OpenD是否打开', self.timeout)
            sleep(0.1)
        # self.trd_ctx = trd_ctx = OpenSecTradeContext(host='127.0.0.1', port=11111, filter_trdmarket=TrdMarket.NONE, security_firm=security_firm)  # 创建交易对象

        # 盘口 callback
        class OrderBookHandler(OrderBookHandlerBase):
            def on_recv_rsp(self, rsp_pb):
                ret_code, data = super(OrderBookHandler,self).on_recv_rsp(rsp_pb)
                if ret_code != RET_OK:
                    trade.log({'msg': data}, level=ERROR, name='on_order_book')
                    return ret_code, data
                
                book: MyBookData = trade.book_my2ks(data)
                # symbol, exchange = extract_my_symbol(data['code'])
                # book: MyBookData = MyBookData(
                #     symbol=symbol,
                #     exchange=exchange,
                #     datetime=datetimes.now(),
                #     name=symbol,
                #     gateway_name=trade.gateway_name
                # )

                # for index, bid_item in enumerate(data['Bid']):
                #     i = index + 1
                    
                #     bid_price = Decimal(str(bid_item[0]))
                #     bid_volume = Decimal(str(bid_item[1]))
                    
                #     setattr(book, f'bid_price_{i}', bid_price)
                #     setattr(book, f'bid_volume_{i}', bid_volume)
                   
                #     if data['Ask']:
                #         ask_item = data['Ask'][index]
                #         ask_price = Decimal(str(ask_item[0]))
                #         ask_volume = Decimal(str(ask_item[1]))
                #         setattr(book, f'ask_price_{i}', ask_price)
                #         setattr(book, f'ask_volume_{i}', ask_volume)

                trade.on_book(book)
                return RET_OK, data
        handler = OrderBookHandler()
        quote_ctx.set_handler(handler)
        
        # 分笔 callback
        class TickerHandler(TickerHandlerBase):
            def on_recv_rsp(self, rsp_pb):
                ret_code, data_df = super(TickerHandler,self).on_recv_rsp(rsp_pb)
                if ret_code != RET_OK:
                    trade.log({'msg': data_df}, level=ERROR, name='on_tick')
                    return RET_ERROR, data_df
                
                if not len(data_df):
                    return ret_code, data_df
                
                data = data_df.to_dict('records')[0]
                # trade.log(data, name='on_ticker')
                
                symbol, exchange = extract_my_symbol(data['code'])
                tz = CHINA_TZ if exchange == KsExchange.SEHK else US_EASTERN_TZ
                dt: datetime = tz.localize(parse(data['time'])).astimezone(CHINA_TZ)
                tick: MyRawTickData = MyRawTickData(
                    symbol=symbol,
                    exchange=exchange,
                    datetime=dt,
                    name=symbol,
                    volume=Decimal(str(data['volume'])),
                    turnover=Decimal(str(data['turnover'])),
                    last_price=Decimal(str(data['price'])),
                    gateway_name=trade.gateway_name
                )
                tick.last_volume = tick.volume
                trade.on_tick(tick)
                return RET_OK, data_df
        handler = TickerHandler()
        quote_ctx.set_handler(handler)

        

    # 订阅行情
    def subscribe(self, vt_symbols, vt_subtype_list, extended_time=True) -> tuple[KsRetCode, Optional[ErrorData]]:
        if not vt_symbols:
            return KS_RET_OK, None
        
        if isinstance(vt_symbols, str):
            vt_symbols = [vt_symbols]

        my_symbols = [symbol_ks2my(x) for x in vt_symbols]
        my_subtype_list = [SUBTYPE_KS2MY.get(x) for x in vt_subtype_list]

        trade = self
        if KsSubscribeType.USER_ORDER in my_subtype_list:
            my_subtype_list.remove(KsSubscribeType.USER_ORDER)     

        if KsSubscribeType.USER_TRADE in my_subtype_list:
            my_subtype_list.remove(KsSubscribeType.USER_TRADE)

        # futu没有持仓回调
        if KsSubscribeType.USER_POSITION in my_subtype_list:
            my_subtype_list.remove(KsSubscribeType.USER_POSITION)

        # 剩下的是订阅行情
        if my_subtype_list:
            ret, data = self.quote_ctx.subscribe(my_symbols, my_subtype_list, extended_time=extended_time)   # 订阅 K 线数据类型，FutuOpenD 开始持续收到服务器的推送
            if ret == RET_ERROR:
                error = self.get_error(vt_symbols, vt_subtype_list, extended_time, code=KsErrorCode.SUBSCRIPTION_ERROR, msg=data)
                self.send_dd(error.msg, f'订阅行情错误')
                return KS_RET_ERROR, error
            return KS_RET_OK, data

        return KS_RET_OK, None
    
    def unsubscribe(self, vt_symbols, vt_subtype_list) -> tuple[KsRetCode, Optional[ErrorData]]:
        if not vt_symbols:
            return KS_RET_OK, None
        
        if isinstance(vt_symbols, str):
            vt_symbols = [vt_symbols]

        my_symbols = [symbol_ks2my(x) for x in vt_symbols]
        my_subtype_list = [SUBTYPE_KS2MY.get(x) for x in vt_subtype_list]


        # 剩下的是订阅行情
        if my_subtype_list:
            ret, data = self.quote_ctx.unsubscribe(my_symbols, my_subtype_list)   # 订阅 K 线数据类型，FutuOpenD 开始持续收到服务器的推送
            if ret == RET_ERROR:
                error = self.get_error(vt_symbols, vt_subtype_list, code=KsErrorCode.SUBSCRIPTION_ERROR, msg=data)
                self.send_dd(error.msg, f'反订阅行情错误')
                return KS_RET_ERROR, error
            return KS_RET_OK, data

        return KS_RET_OK, None

              
    def get_error(self, *args, **kvargs):
        method = sys._getframe(1).f_code.co_name
        error = ErrorData(
            code=kvargs.get('code'),
            msg=kvargs.get('msg'),
            method=method,
            args=args,
            kvargs=kvargs,
            traceback=traceback.format_exc(),
            gateway_name=self.gateway_name
            
        )
        self.log(error, tag=f'api_error.{method}', level=ERROR)
        return error

    # 获取静态信息
    def query_contract(self, vt_symbol: str) -> tuple[KsRetCode, ContractData]:
        symbol, exchange = extract_vt_symbol(vt_symbol)
        my_symbol = symbol_ks2my(vt_symbol)
        ret, data = self.quote_ctx.get_stock_basicinfo(MARKET_KS2MY.get(exchange), code_list=[my_symbol])
        if ret == RET_ERROR:
            error = self.get_error(vt_symbol, data, msg=data)
            return KS_RET_ERROR, error
        
        contract_data = data.iloc[0]
        product: KsProduct = PRODUCT_MY2KS.get(contract_data.stock_type)
        lot_size: Decimal = Decimal(str(contract_data.lot_size))
        size: int = Decimal('1') if product == KsProduct.EQUITY else lot_size
        min_volume: int = lot_size if product == KsProduct.EQUITY else Decimal('1')
        contract = ContractData(
            symbol=symbol,
            exchange=exchange,
            product=product,
            size=size,
            min_volume=min_volume,
            # pricetick=Decimal('0.01'), # todo! 低价股是0.001这里以后要处理
            name=contract_data.get('name'),
            gateway_name=self.gateway_name
        )
        return KS_RET_OK, contract
    
    # 获取静态信息 # todo! ks_trader_wrapper中使用到df=False要修正那边
    def query_contracts(
            self,
            vt_symbols: Optional[List[str]] = None,
            exchanges: Optional[list[KsExchange]] = None,
            products: Optional[List[KsProduct]] = None,
            df: bool = True
        ) -> tuple[KsRetCode, Union[list[ContractData], DataFrame]]:
        if vt_symbols:
            my_symbols = [symbol_ks2my(x) for x in vt_symbols]
            ret, data = self.quote_ctx.get_stock_basicinfo('US', code_list=my_symbols) # futu接口如果指定code_list，会忽略exchange
            if ret == RET_ERROR:
                error = self.get_error(vt_symbols, data, msg=data)
                return KS_RET_ERROR, error
        else:
            data = pd.DataFrame()
            my_products = [PRODUCT_KS2MY.get(x) for x in products]
            my_exchanges = [MARKET_KS2MY.get(x) for x in exchanges]
            for product in my_products:
                for exchange in my_exchanges:
                    ret, data1 = self.quote_ctx.get_stock_basicinfo(market=exchange, stock_type=product)
                    if ret == RET_ERROR:
                        error = self.get_error(vt_symbols, exchanges, products, df, msg=data1)
                        return KS_RET_ERROR, error
                    data = pd.concat([data, data1], ignore_index=True)

        if len(data):
            # 过滤掉退市标的
            data = data[data.delisting==False]
        
        if df:
            data['vt_symbol'] = [symbol_my2ks(x) for x in data['code']]
            data['product'] = [PRODUCT_MY2KS.get(x).value for x in data['stock_type']]
            data['size'] = '1'
            data['min_volume'] = data['lot_size'].astype(str)
            data['gateway'] = self.gateway_name
            data['sub_exchange'] = data['exchange_type']
            return KS_RET_OK, data[['vt_symbol', 'name', 'product', 'size', 'min_volume', 'sub_exchange', 'gateway']]
        
        contracts: list[ContractData] = []
        for index, contract_data in data.iterrows():
            symbol, exchange = extract_my_symbol(contract_data.code)
            contract = ContractData(
                symbol=symbol,
                exchange=exchange,
                sub_exchange=contract_data.exchange_type,
                product=KsProduct.EQUITY,
                size=Decimal('1'),
                min_volume=Decimal(str(contract_data.lot_size)),
                # pricetick=Decimal('0.01'), # todo! 低价股是0.001这里以后要处理
                name=contract_data.get('name'),
                gateway_name=self.gateway_name
            )
            contract.exchange_type = contract_data.exchange_type
            contracts.append(contract)
        return KS_RET_OK, contracts
    
    def query_book(self, vt_symbol: str) -> tuple[KsRetCode,  MyBookData]:
        my_symbol = symbol_ks2my(vt_symbol)
        ret_sub, sub_data = self.quote_ctx.subscribe([my_symbol], [SubType.ORDER_BOOK], subscribe_push=False)
        # 先订阅买卖摆盘类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
        ret_code = RET_ERROR
        ret_data = None
        if ret_sub == RET_OK:  # 订阅成功
            ret, data = self.quote_ctx.get_order_book(my_symbol, num=5)  # 获取一次 3 档实时摆盘数据
            if ret == RET_OK:
                ret_code = KS_RET_OK
                ret_data = self.book_my2ks(data)
            else:
                ret_data = ret_data
        else:
            ret_data = sub_data
        return ret_code, ret_data
    
    def book_my2ks(self, data) -> MyBookData:
        symbol, exchange = extract_my_symbol(data['code'])
        book: MyBookData = MyBookData(
            symbol=symbol,
            exchange=exchange,
            datetime=datetimes.now(),
            name=symbol,
            gateway_name=self.gateway_name
        )

        for index, bid_item in enumerate(data['Bid']):
            i = index + 1
            
            bid_price = Decimal(str(bid_item[0]))
            bid_volume = Decimal(str(bid_item[1]))
            
            setattr(book, f'bid_price_{i}', bid_price)
            setattr(book, f'bid_volume_{i}', bid_volume)
            
            if data['Ask']:
                ask_item = data['Ask'][index]
                ask_price = Decimal(str(ask_item[0]))
                ask_volume = Decimal(str(ask_item[1]))
                setattr(book, f'ask_price_{i}', ask_price)
                setattr(book, f'ask_volume_{i}', ask_volume)
        return book
    
    # todo! ks_trader_rapper没有适配好
    def query_quotes(self, vt_symbols: list[str], df: bool = True) -> Union[KsRetCode, list[QuoteData]]:
        if not vt_symbols:
            return KsRetCode, []
        
        my_symbols = [symbol_ks2my(x) for x in vt_symbols]
        ret, data = self.quote_ctx.get_market_snapshot(my_symbols)

        if ret == RET_OK:
            if df:
                tz = get_tz(vt_symbols[0])
                data['vt_symbol'] = [symbol_my2ks(x) for x in data['code']]
                data['datetime'] = pd.to_datetime(data['update_time']).dt.tz_localize(tz)
                data['volume'] = data['volume'].astype(str)
                data['turnover'] = data['turnover'].astype(str)
                data['turnover_rate'] = data['turnover_rate'].astype(str)
                data['last_price'] = data['last_price'].astype(str)
                data['open_price'] = data['open_price'].astype(str)
                data['high_price'] = data['high_price'].astype(str)
                data['low_price'] = data['low_price'].astype(str)
                data['pre_close'] = data['prev_close_price'].astype(str)
                data['circular_market_cap'] = data['circular_market_val'].astype(str)
                data['total_market_cap'] = data['total_market_val'].astype(str)
                data['pre_close'] = data['prev_close_price'].astype(str)

                if data['trust_valid']:
                    data['circular_market_cap'] = data['trust_aum'].astype(str)
                    data['total_market_cap'] = data['trust_aum'].astype(str)

                return KS_RET_OK, data[['vt_symbol', 'datetime', 'volume', 'turnover', 'turnover_rate', 'last_price', 'open_price', 'high_price', 'low_price', 'pre_close', 'circular_market_cap', 'total_market_cap']]
            else:
                quotes = []
                for index, quote in data.iterrows():
                    symbol, exchange = extract_my_symbol(quote.code)
                    tz = CHINA_TZ if exchange == KsExchange.SEHK else US_EASTERN_TZ
                    dt = tz.localize(parse(f'{quote.data_date} {quote.data_time}')).astimezone(CHINA_TZ)
                    quotes.append(QuoteData(
                        gateway_name=self.gateway_name,
                        symbol=symbol,
                        exchange=exchange,
                        datetime=dt,
                        volume=Decimal(quote.volume),
                        turnover=Decimal(quote.turnover),
                        turnover_rate=Decimal(quote.turnover_rate),
                        last_price=quote.last_price,
                        open_price=quote.open_price,
                        high_price=quote.high_price,
                        low_price=quote.low_price,
                        pre_close=quote.prev_close_price,
                        circular_market_cap=quote.circular_market_val if not quote.trust_valid else quote.trust_aum,
                        total_market_cap=quote.total_market_val if not quote.trust_valid else quote.trust_aum,
                        localtime=datetimes.now()
                    ))
                return KS_RET_OK, quotes
        else:
            return KS_RET_ERROR, self.get_error(vt_symbols=vt_symbols, msg=data)
        
    def query_ticks(self, vt_symbol: str, length: int = 1) -> Union[KsRetCode, list[MyRawTickData]]:
        if not vt_symbol:
            return KsRetCode, []
        
        my_symbol = symbol_ks2my(vt_symbol)
        ret_sub, data_sub = self.quote_ctx.subscribe([my_symbol], [SubType.TICKER], subscribe_push=False, extended_time=True)
        # 先订阅 K 线类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
        if ret_sub == RET_OK:  # 订阅成功
            ret_quote, data_quote = self.quote_ctx.get_rt_ticker(my_symbol, length)  # 获取订阅股票报价的实时数据
            quotes: list[QuoteData] = []
            if ret_quote == RET_OK:
                for index, quote in data_quote.iterrows():
                    symbol, exchange = extract_my_symbol(quote.code)
                    tz = CHINA_TZ if exchange == KsExchange.SEHK else US_EASTERN_TZ
                    dt = tz.localize(parse(f'{quote.time}')).astimezone(CHINA_TZ)
                    quotes.append(MyRawTickData(
                        gateway_name=self.gateway_name,
                        symbol=symbol,
                        exchange=exchange,
                        datetime=dt,
                        volume=Decimal(str(quote.volume)),
                        last_price=Decimal(str(quote.price))
                    ))
                return KS_RET_OK, quotes
            else:
                return KS_RET_ERROR, self.get_error(vt_symbol=vt_symbol, msg=data_quote)
        else:
            return KS_RET_ERROR, self.get_error(vt_symbol=vt_symbol, msg=data_sub)
    
    # https://openapi.futunn.com/futu-api-doc/quote/get-kl.html
    # 由于实际上的历史k线获取收到额度限制，这里用实时K线来代替历史K线，实时K线需要先订阅行情，否则会出错

    # todo 这里默认先不管是不是df都返回df，后续在处理非df 
    def query_history_n(
            self,
            vt_symbol: str,
            n: int,
            interval: KsInterval,
            adjustment: KsAdjustment,
            df: bool = True
        ) -> tuple[KsRetCode, Union[list[BarData], DataFrame]]:
        """
        Query bar history data.
        """
        my_symbol = symbol_ks2my(vt_symbol)
        ret_k, data_k = self.quote_ctx.get_cur_kline(my_symbol, n, ktype=INTERVAL_KS2MY.get(interval), autype=ADJUSTMENT_KS2MY.get(adjustment))
        if not ret_k == RET_OK:
            return KS_RET_ERROR, self.get_error(vt_symbol=vt_symbol, n=n, interval=interval, adjustment=adjustment, msg=data_k)
        tz = get_tz(vt_symbol)
        data_k['vt_symbol'] = vt_symbol
        data_k['datetime'] = pd.to_datetime(data_k.time_key).dt.tz_localize(tz)
        data_k['interval'] = interval.value
        data_k['volume'] = data_k.volume.astype(str)
        data_k['turnover'] = data_k.turnover.astype(str)
        data_k['open'] = data_k.open.astype(str)
        data_k['high'] = data_k.high.astype(str)
        data_k['low'] = data_k.low.astype(str)
        data_k['close'] = data_k.close.astype(str)
        return KS_RET_OK, data_k[['vt_symbol', 'datetime', 'interval', 'volume', 'turnover', 'open', 'high', 'low', 'close']]

    # 关闭上下文连接
    def close(self):
        self.quote_ctx.close()


        