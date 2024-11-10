from account import *
from server import *
from contract import *

def newServer(network,rpc):
    return Server(network,rpc)

def balanceOfETH(address,server:Server):
    account = Account(address,server)
    return account.getBalanceOfEth(address)
    
def balanceOfToken(tokenAddress, address,server:Server):
    account = Account(address,server)
    return account.getBalanceOfToken(tokenAddress, address)

def transferETH(fromAddress,toAddress, amount,server:Server)->Web3Message:
    account = Account(fromAddress,server)
    return account.transferEth(toAddress, amount)
    
def transferToken(tokenAddress,fromAddress, toAddress:list, amount,server:Server)->list:
    token = Contract(server,tokenAddress)
    return token.transferTokenBatch(fromAddress, toAddress, amount)
    

def approveToken(tokenAddress, spenderAddress, amount,server:Server)->Web3Message:
    token = Contract(server,tokenAddress)
    return token.approve(spenderAddress, amount)
    
def balanceOfNFT(ntfAddress, address,server:Server):
    nft = ContractERC721(server,ntfAddress)
    return nft.getBalanceOfAccount(address)
    
def balanceOfNFTList(ntfAddress, address,server:Server)->list:
    nft = ContractERC721(server,ntfAddress)
    return nft.getTokenIDListOfAccount(address)

def transferNFT(ntfAddress, toAddress, tokenIds,server:Server)->list:
    nft = ContractERC721(server,ntfAddress)
    return nft.transferTokenBatch(toAddress, tokenIds)

