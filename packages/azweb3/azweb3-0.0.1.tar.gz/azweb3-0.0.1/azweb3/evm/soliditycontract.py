import sys
import json
import os
from server import Server,Web3Message
# from solc import compile_source #pip3 install py-solc
from solcx import compile_source #pip3 install py-solc-x

class SolidityContract:
    def __init__(self,netWork,Web3Obj:Server = None) -> None:
        if Web3Obj:
            self.Web3Object = Web3Obj
        else:
            self.Web3Object = Web3Base(netWork)
        self.ERC20Source = self.__getERC20()
        self.ERC721Source = self.__getERC721()
    
    def deployByFile(self,contractName,address,gasPrice,sourceFileName):
        self.contractSourceCcode = ''
        with open(sourceFileName) as f:
            for line in f:
                self.contractSourceCcode += line + '\n'
        # self.__deploy(contractName,address,gasPrice)
    
    def deployERC20(self,contractName,tokenName,tokenSymbol,tokenAmount:int,address,privateKey):
        sourceCode =  self.ERC20Source.replace('CONTRACT_NAME', contractName)
        constructorArgs  = {'name_':tokenName, 'symbol_':tokenSymbol,'amount':int(tokenAmount) * (10**18) }
        return self.__deploy(contractName=contractName,address=address,sourceCode=sourceCode,privateKey=privateKey,**constructorArgs)
 
    def deployERC721(self,contractName,tokenName,tokenSymbol,address,privateKey):
        sourceCode =  self.ERC721Source.replace('CONTRACT_NAME', contractName)
        constructorArgs  = {'name_':tokenName, 'symbol_':tokenSymbol }
        return self.__deploy(contractName=contractName,address=address,sourceCode=sourceCode,privateKey=privateKey,**constructorArgs)
                    
    # 部署合约
    def __deploy(self,contractName,address,sourceCode,privateKey,**kwargs):
        retMsg = Web3Message()
        signRet = Web3Message()
        sendTran = Web3Message()
        txRec = Web3Message()
        args=[]
# txn_receipt = web3.eth.get_transaction_receipt(deploy_txn)
# txn_receipt['contractAddress']

        compiledSol = compile_source(sourceCode,output_values=["abi","bin"])
        contractInterface = compiledSol['<stdin>:' +contractName]
        contABI =contractInterface['abi']
        contBIN =contractInterface['bin']
        contract = self.Web3Object.web3.eth.contract(abi=contABI, bytecode=contBIN)
        # txParam = contract.constructor(name,symbol,totalAmount).buildTransaction({
        txParam = contract.constructor(*args,**kwargs).buildTransaction({
            'from': address,
            'nonce':self.Web3Object.getTransactionCount(address) ,
            'gasPrice': self.Web3Object.gasPrice,
            # 'gas':self.Web3Object.GAS_LIMITED,
            }
        )
        signRet = self.Web3Object.signTransaction(txParam,privateKey) #contract.deploy(transaction=txParam)
        if signRet.status:
            # self.Web3Object.web3.eth.send_transaction()
            sendTran = self.Web3Object.sendRawTransaction(signRet.content)
        else:
            retMsg.message = signRet.message
            retMsg.messageTrace = signRet.messageTrace
            
        if sendTran.status:
            retMsg.hash = sendTran.hash
            retMsg.status = True
            txRec = self.Web3Object.getTransactionReceipt(sendTran.hash)
            if txRec.status:
               retMsg.content = txRec.content
               retMsg.value = txRec.content.get('contractAddress')
            else:
                retMsg.message = txRec.message
                retMsg.messageTrace = txRec.messageTrace
            # print(retMsg.value)
            # retMsg.value = retMsg.content.get('contractAddress')
        else:
            retMsg.message = sendTran.message
            retMsg.messageTrace = sendTran.messageTrace
        return retMsg
    
    def __getERC20(self):
        current_file_path = os.path.abspath(__file__)
        current_path = os.path.dirname(current_file_path)
        erc20file =  os.path.join(current_path, 'ERC20.sol')
        with open(erc20file,'r',encoding='UTF-8') as f:
            str = f.read()
        return str
    
    def __getERC721(self):
        current_file_path = os.path.abspath(__file__)
        current_path = os.path.dirname(current_file_path)
        erc721file =  os.path.join(current_path, 'ERC721.sol')
        with open(erc721file,'r',encoding='UTF-8') as f:
            str = f.read()
        return str
    
