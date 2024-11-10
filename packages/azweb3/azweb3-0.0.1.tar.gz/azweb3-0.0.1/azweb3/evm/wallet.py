from eth_account.hdaccount.mnemonic import Mnemonic
import os
from eth_account import Account
from eth_utils import (
    is_address,
    is_checksum_address,
    to_checksum_address,
)
    
from eth_account.hdaccount import (
    ETHEREUM_DEFAULT_PATH,
    generate_mnemonic,
    key_from_seed,
    seed_from_mnemonic,
)

class Wallet:
            
    def __init__(self):
       pass
    
    @staticmethod
    def getWordList():
        wordlist = []

        #文件所在的路径(绝对路径)
        current_path = os.path.split(os.path.realpath(__file__))[0]
        wordlistfile  =  os.path.join(current_path, 'wordlist.txt')
        with open(wordlistfile,'r',encoding='UTF-8') as f:
            wordlist = f.readlines()
        wordList=[i.strip() for i in wordlist]
        return wordList        
    
    #私密转地址
    @staticmethod
    def getAccountFromPrivateKey(privateKey):
        address = None   
        try:
            accObj = Account.from_key(privateKey) #.privateKeyToAccount(privateKey)
            address = accObj.address
        except:
            address = None
        return address
    
    #助记返回地址和正确的助记词
    @classmethod
    def createAccountWithMnemonic(cls,_passphrase):
        address = None
        seedsPhrase = None
        privateKey = None
        try:
            if not Account._use_unaudited_hdwallet_features:
                Account.enable_unaudited_hdwallet_features()
            (accObj, seedsPhrase) = Account.create_with_mnemonic(passphrase = _passphrase)
            address,privateKey = cls.getAccountFromPhrase(seedsPhrase)
        except:
            address = None
            privateKey = None 
            seedsPhrase = None
        return address,privateKey,seedsPhrase #accObj(address)
    
   
    #助记转地址，如果助记错误，返回None
    @classmethod
    def getAccountFromPhrase(cls,_Phrase):
        address = None
        privateKey = None
       
        if not cls.isMnemonic(_Phrase):
            return None,None
        try:
            if not Account._use_unaudited_hdwallet_features:
                Account.enable_unaudited_hdwallet_features()
            localAccount = Account.from_mnemonic(_Phrase)
            address = localAccount.address 
            privateKey=localAccount.key.hex() 
        except:
            address = None
            privateKey=None
        return address,privateKey

    
    
    @staticmethod
    def isMnemonic(_phrase):
        mn = Mnemonic(raw_language="english")
        return mn.is_mnemonic_valid(_phrase)
    
    @staticmethod    
    def getPrivateKeyFromPhrase(_phrase):
        seed = seed_from_mnemonic(_phrase, '')
        private_key = key_from_seed(seed, ETHEREUM_DEFAULT_PATH)
        # bytes.hex
        return '0x'+private_key.hex()

    # 创建新地址
    @staticmethod
    def createAccount():
        acct = {}
        localAccount = Account.create()
        address = localAccount.address
        privateKey = localAccount.key 
        acct={
            'address':address,
            'privateKey': privateKey.hex(),
        }
        return acct
        

    # 创建新地址加密PK
    @classmethod
    def createAccountWithEncrypt(cls,password):
        acct = {}
        result = {}
        acct = cls.createAccount()
        result = {
            'address':acct['address'],
            'privateKey':cls.encrypt(acct['privateKey'],password),
        }
        return result
        
    
     #助记返回地址和正确的助记词
    @classmethod
    def createAccountWithMnemonicEncrypt(cls,password,_passphrase=''):
        address = None
        seedsPhrase = None
        privateKey = None
        privateKey1 = None
        try:
            if not Account._use_unaudited_hdwallet_features:
                Account.enable_unaudited_hdwallet_features()
            (accObj, seedPhrase) = Account.create_with_mnemonic(passphrase = _passphrase)
            address,privateKey = cls.getAccountFromPhrase(seedPhrase)
            privateKey1 = cls.encrypt(privateKey,password)
            seedsPhrase = cls.encrypt(privateKey,password)
        except:
            address = None
            privateKey1 = None
            seedsPhrase = None 
        return address,privateKey1,seedsPhrase  
        
    @staticmethod
    def encrypt(_inStr,_password = '9adm'):
        return Account.encrypt(_inStr, _password)  
        
    @staticmethod
    def decrypt(_inStr,_password = '9adm'):
        depk = Account.decrypt(_inStr, _password)   
        return depk.hex()   
    
    def toAddress(self,_address):
        return self.toChecksumAddress(_address)
        
    @staticmethod
    def toChecksumAddress(address):
        try:
            add = to_checksum_address(address)
        except:
            add = None
        return add
    
    @staticmethod
    def isChecksumAddress(address):
        return is_checksum_address(address)
    

        
      