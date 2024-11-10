from server import Server ,Web3Message
from wallet import Wallet
from contract import Contract,ContractERC721
from web3 import Web3   
import traceback

class Account():
    def __init__(self, _web3Obj:Server,_accountAddress) -> None:
        self.web3 = _web3Obj.web3
        self.web3Object = _web3Obj
        self.address = Wallet.toChecksumAddress(_accountAddress)

    # 显示ETH余额
    def getBalanceOfEth(self):
        balance = self.web3Object.getBalanceOfEth(self.address) 
        return balance

    # 代币余额
    def getBalanceOfToken(self,_contractAddress):
        if self.web3Object.isConnected:
            web3contractObj = Contract(self.web3Object,_contractAddress)
            web3contractObj.getBalanceOfAccount(self.address)
            # tokenContract = web3contractObj.contract
            balance = web3contractObj.getBalanceOfAccount(self.address)
            # Web3.fromWei(tokenContract.functions.balanceOf(self.address).call(), "ether")
            return balance
        else:
            return 0

    # Eth 转账
    # _gasPrice = self.Web3object.gasPrice
    def transferEth(self,_targetAddress, _amount, _gasPrice= Server.GAS_DEFAULT_PRICE, _gasLimit=Server.GAS_LIMITED,_privateKey = '',_nonce = 0)->Web3Message:
        retmsg = Web3Message()
        signRet = Web3Message()
        sendTran = Web3Message()
        if self.web3Object.isConnected:
            try:
                if _nonce == 0:
                    nonce = self.web3.eth.get_transaction_count(self.address)
                else:
                    nonce = _nonce
                retmsg.nonce =  nonce
                params = {
                    'nonce': nonce,
                    'to':    _targetAddress,
                    'value': Web3.toWei(_amount, 'ether'),
                    'gas':   _gasLimit,
                    'gasPrice': _gasPrice,
                    'from': self.address,
                }
                # signedTx = self.web3.eth.account.sign_transaction(params, _privateKey)
                # signedTx = self.web3Object.signTransaction(params, _privateKey)
                signRet = self.web3Object.signTransaction(params, _privateKey)
                if signRet.status:
                    signedTx = signRet.content
                    sendTran = self.web3Object.sendRawTransaction(signedTx)
                    if sendTran.status:
                        retmsg.status = True
                        retmsg.hash = sendTran.hash
                        retmsg.value = sendTran.hash
                        retmsg.content = retmsg.value
                    else:
                        retmsg.message = sendTran.message
                        retmsg.messageTrace = sendTran.messageTrace
                else:
                    retmsg.message = signRet.message
                    retmsg.messageTrace = signRet.messageTrace
                           
            except Exception as e:
                retmsg.message = str(e)
                retmsg.messageTrace = traceback.format_exc()
        else:
            retmsg.message = '服务器连接状态未知'
        return retmsg

    def transferEthBatch(self,_toAddress:list, _transQty, _gasPrice=5, _gasLimit=500000,_privateKey = ''):
        results = []
        retmsg =  Web3Message()
        toAddresses=[]
        fromAddress = self.web3Object.toAddress(self.address)
        for tads in _toAddress:
            toadd = self.web3Object.toAddress(tads)
            if toadd != None and fromAddress != toadd :
                toAddresses.append(toadd)
        if  len(toAddresses) == 0:
            retmsg.status = False
            retmsg.message = '接受地址空'
            result = {'toaddress': None,
                      'msgobj':retmsg}
            results.append(result)
            return results
           
        if fromAddress == None:
            retmsg.status = False
            retmsg.message = '发地址有误'
            result = {'toaddress': None,
                      'msgobj':retmsg}
            results.append(result)
            return results
        
        locNonce  = self.web3Object.web3.eth.get_transaction_count(self.address)
        for toAddress in toAddresses:
            txstatus = self.transferEth(toAddress,_transQty,_gasPrice,_gasLimit,_privateKey,locNonce)
            result = {
                'toaddress':toAddress,
                'msgobj':txstatus, #web3Obj.getTransactionReceipt(txstatus.hash)
                }
            results.append(result)
            locNonce += 1
        return results


    def getTransactionReceipt(self,txHash):
        return self.web3Object.getTransactionReceipt(txHash)

    def getTransaction(self,txHash):
        return self.web3Object.getTransactionByHash(txHash)
    
    def getTransactionCount(self):
        return self.web3Object.getTransactionCount(self.address)
 

    # 代币转账
    def transferToken(self,_tokenAddress,_targetAddress, _amount, _gasPrice=Server.GAS_DEFAULT_PRICE, _gasLimit=Server.GAS_LIMITED,_privateKey = ''):
        retmsg = Web3Message()
        if self.web3Object.isConnected:
            web3contractObj = Contract(self.web3Object,_tokenAddress)
            retmsg = web3contractObj.transferToken(self.address,_targetAddress,_amount,_gasPrice,_gasLimit,_privateKey)
        else:
            retmsg.message = '服务器连接状态未知'
        return retmsg