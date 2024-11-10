from web3 import Web3, HTTPProvider
from web3.gas_strategies import time_based
from eth_abi import encode
from eth_utils import (
    is_address,
    is_checksum_address,
    to_checksum_address,
)
import traceback
class Web3Message:
    def __init__(self,status = False) -> None:
        self.status = status
        self.value = None
        self.hash = None
        self.code = None
        self.message = None
        self.nonce = 0
        self.content=None
        self.messageTrace = None #traceback.format_exc() 
    def __repr__(self):
        str = f'status:{self.status},value:{self.value},hash:{self.value},message:{self.message},content:{self.content}'
        str +=f'messageTrace:{self.messageTrace}'   
        return str    
    
class Server:
    GAS_DEFAULT_PRICE =  2 * ( 10 ** 9 ) #5GWEI 
    GAS_LIMITED = 500000 #wei
    MAX_PRIORITY_FEE_PER_GAS = 2 * ( 10 ** 9 ) #2GWEI
    MAX_BASE_FEE_MULTIPLIER = 2
    
        
    def __init__(self,netWork,rpcAddress):
        self.rpcsCurrent = []
        self.chainRpcsList =[]
        self.rpcsConnected = None
        self.netWorkName = netWork
        self.connected = False
        self.web3 = None
        rpc = rpcAddress
        self.web3 = Web3(HTTPProvider(rpc))
        print(f'{netWork},Connected:{self.web3.is_connected()},RPC:{rpc}' )
        if self.web3.is_connected() is True:
            self.rpcsConnected = rpc
            self.connected = True  #连接状态
            return
    
    def connect(self,rpcAddress):
        self.web3 = Web3(HTTPProvider(rpcAddress))
        if self.web3.is_connected() is True:
            self.rpcsConnected = rpcAddress
            self.connected = True  #连接状态
            return True
        else:
            return False
        
    def disconnect(self):
        self.web3 = None
        self.connected = False  #连接状态
        self.rpcsConnected = None
        return True
    
    @property
    def isConnected(self):
        if self.web3 == None:
            return False
        return self.web3.is_connected()
        
    def set_gas_price_strategy(self, price_strategy_version="自定义"):
        
        # https://web3py.readthedocs.io/en/stable/gas_price.html#gas-price-api
        # 即用型版本:
        # web3.gas_strategies.time_based.fast_gas_price_strategy：交易在 60 秒内开采。
        # web3.gas_strategies.time_based.medium_gas_price_strategy: 交易在 5 分钟内开采。
        # web3.gas_strategies.time_based.slow_gas_price_strategy: 交易在 1 小时内开采。
        # web3.gas_strategies.time_based.glacial_gas_price_strategy: 交易在 24 小时内开采。

    # 生成价格策略：即 GasPriceStrategy 对象
        if price_strategy_version == "fast":
            price_strategy = time_based.fast_gas_price_strategy
        elif price_strategy_version == "medium":
            price_strategy = time_based.medium_gas_price_strategy  # 120个区块，线下跑时阻塞了110秒
        elif price_strategy_version == "slow":
            price_strategy =time_based.slow_gas_price_strategy
        elif price_strategy_version == "glacial":
            price_strategy = time_based.glacial_gas_price_strategy
        else:
            # 自定义
            price_strategy =  time_based.construct_time_based_gas_price_strategy(  # 10个区块，线下跑时阻塞了10秒
                max_wait_seconds=60,  # 交易所需的最大秒数。
                sample_size=10,  # 要采样的最近的块的数量
                probability=98,  # 交易将在 max_wait_seconds 内挖掘的所需概率的整数。0 表示 0%，100 表示 100%。
                # weighted=True  # 时间加权到最近开采的块上。在某些计算机上（pgq）无法时间加权。
            )
        self.web3.eth.setGasPriceStrategy(price_strategy)
        # # 使用缓存解决方案来减少每个请求需要重新获取的链数据量。
        # self.w3.middleware_onion.add(middleware.time_based_cache_middleware)
        # self.w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
        # self.w3.middleware_onion.add(middleware.simple_cache_middleware)


    
    def getGasPrice(self):
        if self.isConnected:
            return self.web3.eth.gas_price #.generate_gas_price()            
        else:
            return 0


    def gasPriceEIP1559(self):
        """
        EIP-1559 标准的Gas Estimator 推荐 Max Fee = (2 * Base Fee) + Max Priority Fee
        maxFeePerGas 和 baseFeePerGas+maxPriorityFeePerGas 之间的差额将退还给用户。
        """
        baseFeePerGas = self.web3.eth.getBlock("pending").baseFeePerGas  # 即时的base，只用于预估的，最后不一定是这个值，所以一般计算max时会乘以一个系数2。
        if isinstance(baseFeePerGas, str):
            baseFeePerGas = int(baseFeePerGas, 16)

        maxPriorityFeePerGas = self.MAX_PRIORITY_FEE_PER_GAS # 支付给矿工的那部分费用，一般为2gwei，2000000000
        maxFeePerGas = baseFeePerGas * self.MAX_BASE_FEE_MULTIPLIER + maxPriorityFeePerGas  # 最多愿意支付

    def generate_gas_price(self, tx_params):
        """
        计算gas价格
        :param tx_params: 交易参数
        :return: gas_price （单位：wei）
        """
        # 使用预设的gas价格策略，会阻塞。有点久！！！！
        gas_price = self.web3.eth.generate_gas_price(tx_params)  # 使用预设的gas价格策略，会阻塞（单位：wei）
        return gas_price


    def getEstimateGas(self,txParams):
        if self.isConnected:
            return self.web3.eth.estimate_gas(txParams)
        else:
            return 0
           
    
    # 显示ETH余额
    def getBalanceOfEth(self,_address):
        if self.isConnected:
            balance = Web3.fromWei(self.getBalanceOfEthWei(_address), "ether")
            return float(balance)
        else:
            return 0
    
    # 显示ETH余额
    def getBalanceOfEthWei(self,_address):
        if self.isConnected:
            balance =  self.web3.eth.get_balance(_address) 
            # print(balance)
            return balance 
        else:
            return 0
    
    def isContractAddress(self,_address):
        if self.isConnected:
            code = self.web3.eth.get_code(_address)
            if code == '0x' or code == b'' :
                return False
            else:
                return True
        else:
            return False
            
    def getBlockIdByDate(self,timestamp):
       if self.isConnected:
            pass

    @property    
    def gasPrice(self):
        livePrice = self.getGasPrice() 
        if livePrice != 0:
            return livePrice
        else:
            return self.GAS_DEFAULT_PRICE
    
    @staticmethod
    def toAddress(address):
        try:
            add = to_checksum_address(address)
        except:
            add = None
        return add
    def signTransaction(self,params,privateKey):
        retmsg = Web3Message()
        try:
            # estGas = self.getEstimateGas(params)
            # gasPrice = params.get('gasPrice')
            # if not gasPrice:
            #     gasPrice = self.gasPrice
            # gasFee = Web3.fromWei(estGas*gasPrice,'ether')
            # print(f'gas:{estGas},Price:{gasPrice},gasFee:{gasFee}')
            signedTx = self.web3.eth.account.sign_transaction(params, private_key=privateKey)
            retmsg.status = True
            retmsg.value =  signedTx
            retmsg.content = signedTx
        except Exception as e :
            retmsg.message = str(e)
            retmsg.messageTrace = traceback.format_exc()
        return retmsg
    
    def sendRawTransaction(self,signedTxn):
        retmsg = Web3Message()
        try:
            txHash = self.web3.eth.send_raw_transaction(signedTxn.rawTransaction)
            if txHash is None:
                retmsg.message = '哈希不存在'
            else:
                retmsg.status = True
                retmsg.hash =  txHash.hex()
                retmsg.value =  txHash.hex()
                retmsg.content = retmsg.value
        except Exception as e :
            retmsg.message = str(e)
            retmsg.messageTrace = traceback.format_exc()
        return retmsg

                    
    # 显示交易数量
    def getTransactionCount(self,_address):
        if self.isConnected:
            nonce =  self.web3.eth.get_transaction_count(_address) 
            # print(balance)
            return nonce 
        else:
            return 0
    

    def getTransactionReceipt(self,txHash):
    # #准备接收发送回执
        retmsg = Web3Message()
        try:
            tx_receipt = dict(self.web3.eth.wait_for_transaction_receipt(txHash)) #.get_transaction_receipt(txHash)
            if tx_receipt is None:
                retmsg.message = '哈希不存在'
            else:
                retmsg.status = True
                # retmsg.hash = tx_receipt
                retmsg.value = tx_receipt.get('transactionHash')
                retmsg.content = tx_receipt
        except Exception as e :
            retmsg.message = str(e)
            retmsg.messageTrace = traceback.format_exc()
        return retmsg
            
        
    def getTransactionByHash(self,txHash):
    # #准备接收发送回执
        retmsg = Web3Message()
        try:
            tx = self.web3.eth.get_transaction(txHash)
            if tx is None:
                retmsg.message = '哈希不存在'
            else:
                retmsg.status = True
                # retmsg.hash = tx
                # retmsg.value = tx
                retmsg.content = tx
        except Exception as e :
            retmsg.message = str(e)
            retmsg.messageTrace = traceback.format_exc()
        return retmsg
    
    def getTransactionLog(self,walletAddress):
        encoded_wallet = (self.web3.to_hex(encode(['address'], [walletAddress]))) # encoding
        # 该方法返回一个web3.utils.filters.Filter对象
        # event_filter = self.web3.eth.filter({'topics': [transferEventSignature, None, encoded_wallet]}) # setting up a filter with correct parametrs
        
        event_filter = self.web3.eth.filter({'address': walletAddress}) # setting up a filter with correct parametrs
        print(event_filter)
        for event in event_filter.get_all_entries():
            print(event)
            # while True:
            #     for event in event_filter.get_new_entries():
            #         decoded_address = decode_abi(['address'], HexBytes(event.topics[2])) # decoding wallet 
            #         value = decode_abi(['uint256'], HexBytes(event.data)) # decoding event.data
            #         tokenContractAddress = event.address
            #         # contractInstance = web3.eth.contract(address=tokenContractAddress, abi=jsonAbi) # jsonAbi is standart erc-20 token abi 
                    # name = contractInstance.functions.name().call() 
                    # decimals = contractInstance.functions.decimals().call()
                    # symbol = contractInstance.functions.symbol().call()
                        
