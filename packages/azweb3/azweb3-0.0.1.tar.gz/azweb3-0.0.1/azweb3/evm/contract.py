import json
from server import Server ,Web3Message
from web3 import Web3
import traceback

class ethABIBase:
        # Dex Name ID 
    BNB_PANCAKE_V2 = 'BNB_PanCake_V2'
    ETH_UNISWAP_V2 = 'ETH_UniSwap_V2'
    ETH_UNISWAP_V3 = 'ETH_UniSwap_V3'
    BNB_PANCAKE_V2_TEST = 'BNB_PanCake_V2_TEST'
    
    __ERC20ABI = '[{"inputs": [{"internalType": "string", "name": "name_", "type": "string"}, {"internalType": "string", "name": "symbol_", "type": "string"}], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "spender", "type": "address"}, {"indexed": false, "internalType": "uint256", "name": "value", "type": "uint256"}], "name": "Approval", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "from", "type": "address"}, {"indexed": true, "internalType": "address", "name": "to", "type": "address"}, {"indexed": false, "internalType": "uint256", "name": "value", "type": "uint256"}], "name": "Transfer", "type": "event"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}]'
    # __ERC721ABI = '[{"inputs": [{"internalType": "string", "name": "name_", "type": "string"}, {"internalType": "string", "name": "symbol_", "type": "string"}], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "approved", "type": "address"}, {"indexed": true, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Approval", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "operator", "type": "address"}, {"indexed": false, "internalType": "bool", "name": "approved", "type": "bool"}], "name": "ApprovalForAll", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "from", "type": "address"}, {"indexed": true, "internalType": "address", "name": "to", "type": "address"}, {"indexed": true, "internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "Transfer", "type": "event"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "approve", "outputs": [], "stateMutability": "nonpayable", "type": "function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "getApproved", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "operator", "type": "address"}], "name": "isApprovedForAll", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "ownerOf", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "safeTransferFrom", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "safeTransferFrom", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "operator", "type": "address"}, {"internalType": "bool", "name": "approved", "type": "bool"}], "name": "setApprovalForAll", "outputs": [],"stateMutability": "nonpayable","type":"function"},{"inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}], "name": "supportsInterface", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"},{"inputs":[{"internalType": "address", "name": "owner", "type": "address" }, {"internalType": "uint256", "name": "index", "type": "uint256" } ], "name": "tokenOfOwnerByIndex", "outputs": [ {  "internalType": "uint256", "name": "",  "type": "uint256" }], "stateMutability": "view",  "type": "function" }, {"inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "tokenURI", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "tokenId", "type": "uint256"}], "name": "transferFrom", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]'
    __ERC721ABI = '[{"inputs": [{"internalType": "string","name": "name_","type": "string"},{"internalType": "string","name": "symbol_","type": "string"}],"stateMutability": "nonpayable","type": "constructor"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "owner","type": "address"},{"indexed": true,"internalType": "address","name": "approved","type": "address"},{"indexed": true,"internalType": "uint256","name": "tokenId","type": "uint256"}],"name": "Approval","type": "event"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "owner","type": "address"},{"indexed": true,"internalType": "address","name": "operator","type": "address"},{"indexed": false,"internalType": "bool","name": "approved","type": "bool"}],"name": "ApprovalForAll","type": "event"},{"inputs": [{"internalType": "address","name": "to","type": "address"},{"internalType": "uint256","name": "tokenId","type": "uint256"}],"name": "approve","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "uint256","name": "tokenId","type": "uint256"}],"name": "burn","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "to","type": "address"}],"name": "mint","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "nonpayable","type": "function"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "previousOwner","type": "address"},{"indexed": true,"internalType": "address","name": "newOwner","type": "address"}],"name": "OwnershipTransferred","type": "event"},{"inputs": [],"name": "pause","outputs": [],"stateMutability": "nonpayable","type": "function"},{"anonymous": false,"inputs": [{"indexed": false,"internalType": "address","name": "account","type": "address"}],"name": "Paused","type": "event"},{"inputs": [],"name": "renounceOwnership","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "to","type": "address"}],"name": "safeMint","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "from","type": "address"},{"internalType": "address","name": "to","type": "address"},{"internalType": "uint256","name": "tokenId","type": "uint256"}],"name": "safeTransferFrom","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "from","type": "address"},{"internalType": "address","name": "to","type": "address"},{"internalType": "uint256","name": "tokenId","type": "uint256"},{"internalType": "bytes","name": "data","type": "bytes"}],"name": "safeTransferFrom","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "operator","type": "address"},{"internalType": "bool","name": "approved","type": "bool"}],"name": "setApprovalForAll","outputs": [],"stateMutability": "nonpayable","type": "function"},{"anonymous": false,"inputs": [{"indexed": true,"internalType": "address","name": "from","type": "address"},{"indexed": true,"internalType": "address","name": "to","type": "address"},{"indexed": true,"internalType": "uint256","name": "tokenId","type": "uint256"}],"name": "Transfer","type": "event"},{"inputs": [{"internalType": "address","name": "from","type": "address"},{"internalType": "address","name": "to","type": "address"},{"internalType": "uint256","name": "tokenId","type": "uint256"}],"name": "transferFrom","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"internalType": "address","name": "newOwner","type": "address"}],"name": "transferOwnership","outputs": [],"stateMutability": "nonpayable","type": "function"},{"inputs": [],"name": "unpause","outputs": [],"stateMutability": "nonpayable","type": "function"},{"anonymous": false,"inputs": [{"indexed": false,"internalType": "address","name": "account","type": "address"}],"name": "Unpaused","type": "event"},{"inputs": [{"internalType": "address","name": "owner","type": "address"}],"name": "balanceOf","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "uint256","name": "tokenId","type": "uint256"}],"name": "getApproved","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "address","name": "operator","type": "address"}],"name": "isApprovedForAll","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "name","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "owner","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "uint256","name": "tokenId","type": "uint256"}],"name": "ownerOf","outputs": [{"internalType": "address","name": "","type": "address"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "paused","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "bytes4","name": "interfaceId","type": "bytes4"}],"name": "supportsInterface","outputs": [{"internalType": "bool","name": "","type": "bool"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "symbol","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "uint256","name": "index","type": "uint256"}],"name": "tokenByIndex","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "owner","type": "address"},{"internalType": "uint256","name": "index","type": "uint256"}],"name": "tokenOfOwnerByIndex","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "address","name": "owner","type": "address"}],"name": "tokensOfOwner","outputs": [{"internalType": "uint256[]","name": "","type": "uint256[]"}],"stateMutability": "view","type": "function"},{"inputs": [{"internalType": "uint256","name": "tokenId","type": "uint256"}],"name": "tokenURI","outputs": [{"internalType": "string","name": "","type": "string"}],"stateMutability": "view","type": "function"},{"inputs": [],"name": "totalSupply","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"stateMutability": "view","type": "function"}]'
    # __ERC721ABI = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"_name","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"name":"_approved","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_tokenId","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"implementsERC721","outputs":[{"name":"_implementsERC721","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"_totalSupply","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"name":"_tokenId","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"name":"_owner","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_tokenId","type":"uint256"}],"name":"tokenMetadata","outputs":[{"name":"_infoUrl","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"_balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_owner","type":"address"},{"name":"_tokenId","type":"uint256"},{"name":"_approvedAddress","type":"address"},{"name":"_metadata","type":"string"}],"name":"mint","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"_symbol","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_tokenId","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"numTokensTotal","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"getOwnerTokens","outputs":[{"name":"_tokenIds","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_to","type":"address"},{"indexed":true,"name":"_tokenId","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_approved","type":"address"},{"indexed":false,"name":"_tokenId","type":"uint256"}],"name":"Approval","type":"event"}]'
    __PanCakeBNBFactoryABI = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
    __PanCakeBNBPairABI = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
    __PanCakeBNBRouterABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
    __UniSwapEthFactoryABI = ''
    __UniSwapEthPairABI = ''
    __UniSwapEthRouterABI = ''
    __UniSwapEthFactoryV3ABI = ''
    __UniSwapEthPairV3ABI = ''
    __UniSwapEthRouterV3ABI = ''
    def __init__(self) -> None:
        pass

    # 返回合约ABI
    @staticmethod
    def getABIbyFile(_ABIJsonFile):
        if _ABIJsonFile:
            with open(_ABIJsonFile,'r',encoding='UTF-8') as f:
                ABI = f.read()                
        # ABI = json.load(open(_ABIJsonFile))
        return ABI

    @staticmethod
    def getBnbABIbyApi(_contractAddress, _APIKey):
        pass
        # bscContract = bscAPIContractBase(_contractAddress, _APIKey)
        # ABI = bscContract.getABI()
        # return ABI    
    
    @classmethod
    def getERC721ABI(cls):
        return cls.__ERC721ABI
    
    @classmethod
    def getERC20ABI(cls):
        return cls.__ERC20ABI
    
    @classmethod
    def getSwapFactoryABI(cls,DexID):
        if DexID == cls.ETH_UNISWAP_V2:
            return cls.__UniSwapEthFactoryABI
        elif DexID == cls.ETH_UNISWAP_V3: 
            return cls.__UniSwapEthFactoryV3ABI
        else: #'BNB_PanCake_V2'
             return cls.__PanCakeBNBFactoryABI


    @classmethod
    def getSwapRouterABI(cls,DexID):
        if DexID == cls.ETH_UNISWAP_V2:
            return cls.__UniSwapEthRouterABI
        elif DexID == cls.ETH_UNISWAP_V3: 
            return cls.__UniSwapEthRouterV3ABI
        else: #'BNB_PanCake_V2'
            return cls.__PanCakeBNBRouterABI

    @classmethod
    def getSwapPairABI(cls,DexID):
        if DexID == cls.ETH_UNISWAP_V2:
            return cls.__UniSwapEthPairABI
        elif DexID == cls.ETH_UNISWAP_V3: 
            return cls.__UniSwapEthPairV3ABI
        else: #'BNB_PanCake_V2'
            return cls.__PanCakeBNBPairABI
        
    @classmethod
    def getPanCakeFactoryABI(cls):
        return cls.getSwapFactoryABI(cls.BNB_PANCAKE_V2)
        # return cls.__PanCakeFactoryABI
    
    @classmethod
    def getPanCakeRouterABI(cls):
        return cls.getSwapRouterABI(cls.BNB_PANCAKE_V2)
        # return cls.__PanCAkeRouterABI

    @classmethod
    def getPanCakePairABI(cls):
        return cls.getSwapPairABI(cls.BNB_PANCAKE_V2)
        # return cls.__PanCakePairABI

    # 分析ABI
    @classmethod
    def studyABI(cls,_ABIJson):
        interfaces = []
        ABIList = json.loads(_ABIJson) 
        for elemt in ABIList:
            inputstr = 'inputs:'
            outputstr = 'outputs:'
            if elemt.get('inputs'):
                for ipt in elemt['inputs']:
                    inputstr += ipt['name'] + ','
            
            if elemt.get('outputs'):
                for opt in elemt['outputs']:
                    outputstr += opt['name'] + ','
            inputstr = inputstr[:-1] 
            outputstr = outputstr[:-1]        
            cont =  { 'type': elemt['type'],
                    'full':f'{elemt.get("name")}:<{inputstr}> <{outputstr}>',
                    'name':elemt.get('name'),
                    'inputs':f'<{inputstr}>',
                    'outputs':f'<{outputstr}>',
            }
            
            interfaces.append(cont)
        return interfaces

    # 打印ABI接口
    @classmethod
    def printABIInterface(cls,_ABIJsonfile = '',_ABIStr = ''):
        if _ABIJsonfile:
            abiStr = cls.getABIbyFile(_ABIJsonfile)
        else:
            abiStr = _ABIStr
        restList = ethABIBase.studyABI(abiStr)
        for cont in restList:
            print(f"Types:{cont['type']}: {cont['full']}")
            

class Contract:
    def __init__(self,_web3Obj:Server,_contractAddress,_ABI= ethABIBase.getERC20ABI()) -> None:
        self.__tokenName = None
        self.__tokensymbol =  None
        self.__totalSupply = 0
        self.__decimals = 0
        self.contract = None
        self.web3Object = _web3Obj
        self.address = self.web3Object.toAddress(_contractAddress)
        if not self.address:
            return
        if not self.web3Object:
            return 
        if not self.web3Object.isConnected:
            return
        
        self.web3 = self.web3Object.web3
        self.code = self.web3.eth.get_code(self.address)
        if self.code != '0x' and not self.code == b'' :
            # self.ABIObject = ABIBase(self.web3Object.netWorkName,self.address)
            self.ABIString = _ABI #self.ABIObject.ABI
            self.contract = self.__getContract(self.ABIString )
        
        if self.isContractLive:
            self.functionList = self.contract.all_functions()


    def __isFunctionExists(self,functionName):
        if self.web3Object.isConnected:
            fun = None
            try:
                if self.isContractLive:
                    fun = self.contract.get_function_by_name(functionName)
                if fun :
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

     #根据地址返回合约对象
    def __getContract(self,_stringABI) :
        if self.web3Object.isConnected:
            # 返回带有EIP55校验和给定地址
            ContractAddress = self.web3Object.toAddress(self.address)
            tokenContract = self.web3.eth.contract(address=ContractAddress, abi=_stringABI)
            return tokenContract
        else:
            return None

    @property
    def name(self):
        if self.__isFunctionExists('name'):    
            name = self.contract.functions.name().call()
            return name
        else:
            None

    @property
    def symbol(self):          
        if self.__isFunctionExists('symbol'):  
            symbol = self.contract.functions.symbol().call()
            return symbol
        else:
            return None
            
            
    @property
    def totalSupply(self):
        if self.__isFunctionExists('totalSupply'):
            decimals = self.decimals
            totalSupply = self.contract.functions.totalSupply().call()
            if decimals !=0:
                totalSupply = totalSupply /10**decimals
            # totalSupply = Web3.fromWei(self.contract.functions.totalSupply().call(),'ether')
            return totalSupply
        else:
            0

    @property
    def decimals(self):             
        if self.__isFunctionExists('decimals'):  
            decimals = self.contract.functions.decimals().call()
            return decimals
            # else:
            #     self.tokenName = 'Address is not a Contract'
            
    @property
    def isContractLive(self):
        if self.contract:
            return True
        else:
            return False
    
    def getBalanceOfAccount(self,_accountAddress):
        if self.web3Object.isConnected and self.isContractLive:
            decimals = self.decimals
            balance =self.contract.functions.balanceOf(_accountAddress).call()
            if decimals != 0:
                balance = balance / 10**decimals
            # balance = Web3.fromWei(self.contract.functions.balanceOf(_accountAddress).call(), "ether")
            return float(balance)
        else:
            return 0

    # 代币转账
    # _gasPrice = self.Web3object.gasPrice
    def transferToken(self,_fromAddress,_toAddress, _amount, _gasPrice= Server.GAS_DEFAULT_PRICE, _gasLimit=Server.GAS_LIMITED,_privateKey = '',_nonce=0):
        retmsg = Web3Message()
        signRet = Web3Message()
        sendTran = Web3Message()
        if self.web3Object.isConnected and self.isContractLive:
            try:
                if _nonce == 0:
                    nonce = self.web3.eth.get_transaction_count(_fromAddress)
                else:
                    nonce = _nonce
                retmsg.nonce =  nonce
                params = {
                    "from": _fromAddress,
                    "value": 0, #Web3.toWei(_amount,'ether'),
                    'gasPrice': _gasPrice,
                    "gas": _gasLimit,
                    "nonce": nonce,
                    # "'type': '0x2'"
                }
                func = self.contract.functions.transfer(_toAddress, Web3.toWei(_amount, "ether"))
                tx = func.buildTransaction(params)
                # signedTx = self.web3.eth.account.sign_transaction(tx, private_key=_privateKey)
                signRet = self.web3Object.signTransaction(tx, _privateKey)
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
                # txHash = self.web3.eth.sendRawTransaction(signedTx.rawTransaction)
                # return txHash.hex()
            except Exception as e:
                retmsg.message = str(e)
                retmsg.messageTrace = traceback.format_exc()
        else:
            retmsg.message = '服务器连接状态未知'
        return retmsg        


    def transferTokenBatch(self,_fromAddress,_toAddress:list, _transQty, _gasPrice=5, _gasLimit=500000,_privateKey = '')->list:
        results = []
        retmsg =  Web3Message()
        toAddresses=[]
        fromAddress = self.web3Object.toAddress(_fromAddress)
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
        
        locNonce  = self.web3Object.web3.eth.get_transaction_count(fromAddress)
        for toAddress in toAddresses:
            txstatus = self.transferToken(fromAddress,toAddress,_transQty,_gasPrice,_gasLimit,_privateKey,locNonce)
            result = {
                'toaddress':toAddress,
                'msgobj':txstatus, #web3Obj.getTransactionReceipt(txstatus.hash)
                }
            results.append(result)
            locNonce += 1
        return results
            
    def approve(self,accountAddress,toAddress,Qty,privateKey)->Web3Message:
        retmsg = Web3Message()
        QtyWei = Web3.toWei(Qty,'ether')
        approvedQty = self.queryAllowance(accountAddress,toAddress)
        approveQty = QtyWei - approvedQty 
        if approveQty <= 0:
            retmsg.status = True
            retmsg.message = '不需要'
            return retmsg
        try:
            approveToAddress = self.web3Object.toAddress(toAddress)
            approveParam = self.contract.functions.approve(approveToAddress, approveQty).build_transaction({
                    'from': accountAddress,
                    'gasPrice':self.web3Object.gasPrice,
                    'nonce': self.web3Object.getTransactionCount(accountAddress),
                    })

            signedTxn = self.web3Object.signTransaction(approveParam,privateKey) 
            txApprove = self.web3Object.sendRawTransaction(signedTxn)
            retmsg.status = True
            # retmsg.hash = txApprove
            retmsg.value = txApprove
            retmsg.content = retmsg.value
            return retmsg 
            # return txApprove
        except Exception as e :
            retmsg.message = str(e)
            retmsg.messageTrace = traceback.format_exc()
            return retmsg 

    # 取消授权
    def unApprove(self,accountAddress,toAddress,privateKey):
        return self.approve(accountAddress,toAddress,0,privateKey)

    # 查看授权余额
    def queryAllowance(self,accountAddress,toAddress):
        allowQty = self.contract.functions.allowance(accountAddress,toAddress).call()
        return Web3.from_wei(allowQty,'ether')
    
class ContractERC721():
    def __init__(self,_web3Obj:Server,_contractAddress,_ABI= ethABIBase.getERC721ABI()) -> None:
        self.tokenName = None
        self.tokensymbol =  None
        self.web3Object = _web3Obj
        self.address = self.web3Object.toAddress(_contractAddress) 
        if not self.web3Object.isConnected:
            return
        
        self.web3 = self.web3Object.web3
        self.code = self.web3.eth.get_code(self.address)
        if self.code != '0x' and not self.code == b'' :
            self.ABIString = _ABI #self.ABIObject.ABI
            self.contract = self.__getContract(self.ABIString )
        
        if self.isContractLive:
            self.functionList = self.contract.all_functions()
                # for fun in self.functionList:
                #     print(fun)
                #     print(type(fun))
            # if self.__isFunctionExists('name'):    
            #     self.tokenName = self.contract.functions.name().call()
            # if self.__isFunctionExists('symbol'):  
            #     self.tokensymbol = self.contract.functions.symbol().call()
            # if self.__isFunctionExists('totalSupply'):  
            #     self.totalSupply = self.contract.functions.totalSupply().call()
            # if self.__isFunctionExists('decimals'):  
            #     self.decimals = self.contract.functions.decimals().call()
            # else:
            #     self.tokenName = 'Address is not a Contract'
        
            

    def __isFunctionExists(self,functionName):
        if self.web3Object.isConnected:
            fun = None
            try:
                if self.isContractLive:
                    fun = self.contract.get_function_by_name(functionName)
                if fun :
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False

     #根据地址返回合约对象
    def __getContract(self,_stringABI) :
        if self.web3Object.isConnected:
            # 返回带有EIP55校验和给定地址
            ContractAddress = Web3.to_checksum_address(self.address)
            tokenContract = self.web3.eth.contract(address=ContractAddress, abi=_stringABI)
            return tokenContract
        else:
            return None

    @property
    def name(self):
        if self.__isFunctionExists('name'):    
            name = self.contract.functions.name().call()
            return name
        else:
            None

    @property
    def symbol(self):          
        if self.__isFunctionExists('symbol'):  
            symbol = self.contract.functions.symbol().call()
            return symbol
        else:
            return None
            
    @property
    def tokenURI(self):
        if self.__isFunctionExists('tokenURI'):  
            tokenURI = self.contract.functions.tokenURI().call()
            return tokenURI
        else:
            return None         
            
    @property
    def totalSupply(self):
        if self.__isFunctionExists('totalSupply'):
            totalSupply = self.contract.functions.totalSupply().call()
            return totalSupply
        else:
            return 0

    
    @property
    def isContractLive(self):
        if self.contract:
            return True
        else:
            return False
    
    def getBalanceOfAccount(self,_accountAddress):
        address = self.web3Object.toAddress(_accountAddress)
        if self.web3Object.isConnected: #"" and self.isContractLive:
            balance = self.contract.functions.balanceOf(address).call()
            return balance
        else:
            return 0

    def getownerOfTokenID(self,_tokenId:int):
        if self.web3Object.isConnected: # and self.isContractLive:
            return self.contract.functions.ownerOf(_tokenId).call()
        else:
            return None

    def getTokenIDOfAccountByIndex(self,_accountAddress,_index):
        address = self.web3Object.toAddress(_accountAddress)
        if self.web3Object.isConnected : #and self.isContractLive:
            if self.__isFunctionExists('tokenOfOwnerByIndex'):
                return self.contract.functions.tokenOfOwnerByIndex(address,_index).call()
            else:
                return None
        else:
            return None

    def getTokenIDListOfAccount(self,_accountAddress)->list:
        balance = self.getBalanceOfAccount(_accountAddress)
        tokenIdList=[]
        if balance > 0:
            for i in range(balance):
                tokenIdList.append(self.getTokenIDOfAccountByIndex(_accountAddress,i))
        return tokenIdList

    def transferTokenBatch(self,_fromAddress,_toAddress, _tokenIDs:list, _gasPrice=5, _gasLimit=500000,_privateKey = '',_indSaft=True)->list:
        results = []
        retmsg =  Web3Message()
        tokenIDs=[]
        for tid in _tokenIDs:
            if tid != None and tid != '' and tid !=0:
                tokenIDs.append(tid)
        if  len(tokenIDs) == 0:
            retmsg.status = False
            retmsg.message = 'TOKENID 空'
            result = {'tokenid': None,
                      'msgobj':retmsg}
            results.append(result)
            return results
           
        fromAddress = self.web3Object.toAddress(_fromAddress)
        toAddress = self.web3Object.toAddress(_toAddress)
        if fromAddress == toAddress or fromAddress == None or toAddress == None:
            retmsg.status = False
            retmsg.message = '收发地址有误'
            result = {'tokenid': None,
                      'msgobj':retmsg}
            results.append(result)
            return results
        
        locNonce  = self.web3Object.web3.eth.get_transaction_count(_fromAddress)
        for tokenid in tokenIDs:
            # print(tokenid)
            int_tokenid = int(tokenid)
            ownerOfTokenId = self.getownerOfTokenID(int_tokenid)
            if ownerOfTokenId == fromAddress:
                if _indSaft:
                    txstatus= self.saftTransferToken(_fromAddress,_toAddress,int_tokenid,_gasPrice,_gasLimit,_privateKey,locNonce)
                else:
                    txstatus = self.transferToken(_fromAddress,_toAddress,int_tokenid,_gasPrice,_gasLimit,_privateKey,locNonce)
                result = {
                'tokenid':tokenid,
                'msgobj':txstatus, #web3Obj.getTransactionReceipt(txstatus.hash)
                }
                results.append(result)
            else:
                retmsg.status = False
                retmsg.message = f"TokenId:{tokenid},所有者{ownerOfTokenId}"
                result = {'tokenid': tokenid,
                         'msgobj':retmsg}
                results.append(result)
            locNonce += 1
        return results
        
    # NFT转账
    def transferToken(self,_fromAddress,_toAddress, _tokenID:int, _gasPrice=5, _gasLimit=500000,_privateKey = '',_nonce = 0):
        retmsg = Web3Message()
        signRet = Web3Message()
        sendTran = Web3Message()
        if self.web3Object.isConnected and self.isContractLive:
            try:
                if _nonce == 0:
                    nonce = self.web3.eth.get_transaction_count(_fromAddress)
                else:
                    nonce = _nonce    
                params = {
                    "from": _fromAddress,
                    "value": 0,
                    'gasPrice': Web3.to_wei(_gasPrice, 'gwei'),
                    "gas": _gasLimit,
                    "nonce": nonce,
                }
                func = self.contract.functions.transferFrom(_fromAddress, _toAddress ,_tokenID)
                tx = func.buildTransaction(params)
                # signedTx = self.web3.eth.account.sign_transaction(tx, private_key=_privateKey)
                signRet = self.web3Object.signTransaction(tx, _privateKey)
                # txHash = self.web3.eth.sendRawTransaction(signedTx.rawTransaction)
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
 
     # NFT转账
    def saftTransferToken(self,_fromAddress,_toAddress, _tokenID:int, _gasPrice=5, _gasLimit=500000,_privateKey = '',_nonce = 0):
        retmsg = Web3Message()
        signRet = Web3Message()
        sendTran = Web3Message()
        if self.web3Object.isConnected and self.isContractLive:
            try:
                if _nonce == 0:
                    nonce = self.web3.eth.get_transaction_count(_fromAddress)
                else:
                    nonce = _nonce
                params = {
                    "from": _fromAddress,
                    "value": 0,
                    'gasPrice': _gasPrice,
                    "gas": _gasLimit,
                    "nonce": nonce,
                }
                func = self.contract.functions.safeTransferFrom(_fromAddress, _toAddress ,_tokenID)
                tx = func.buildTransaction(params)
                # signedTx = self.web3.eth.account.sign_transaction(tx, private_key=_privateKey)
                signRet = self.web3Object.signTransaction(tx, _privateKey)
                # txHash = self.web3.eth.sendRawTransaction(signedTx.rawTransaction)
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
   
        # NFT转账
    def saftMint(self,_fromAddress,_toAddress, _gasPrice=5, _gasLimit=500000,_privateKey = ''):
        retmsg = Web3Message()
        signRet = Web3Message()
        sendTran = Web3Message()
        gas = 800000
        if self.web3Object.isConnected and self.isContractLive:
            try:
                nonce = self.web3.eth.get_transaction_count(_fromAddress)
                params = {
                    "from": _fromAddress,
                    # "value": 0,
                    'gasPrice': _gasPrice,
                    "gas": _gasLimit,
                    "nonce": nonce,
                }
                func = self.contract.functions.safeMint(_toAddress)
                tx = func.buildTransaction(params)
                signRet = self.web3Object.signTransaction(tx, _privateKey)
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

    # setApprovalForAll
    # isApprovedForAll

    # 授权
    def approve(self,accountAddress,toAddress,tokenID,privateKey):
        retmsg = Web3Message()
        try:
            approveToAddress = self.web3Object.toAddress(toAddress)
            approveParam = self.contract.functions.approve(approveToAddress, tokenID).build_transaction({
                    'from': accountAddress,
                    'gasPrice':self.web3Object.gassPriceDefault,
                    'nonce': self.web3Object.getTransactionCount(accountAddress),
                    })
            signedTxn = self.web3Object.signTransaction(approveParam,privateKey) 
            txApprove = self.web3Object.sendRawTransaction(signedTxn) 
            retmsg.status = True
            # retmsg.hash = txApprove
            retmsg.value = txApprove
            retmsg.content = retmsg.value
        except Exception as e :
            retmsg.message = str(e)
            retmsg.messageTrace = traceback.format_exc()
            return retmsg 
            
    # 取消授权
    def unApprove(self,accountAddress,toAddress,privateKey):
        pass
        # return self.approve(accountAddress,toAddress,0,privateKey)

    # 查看授权
    def queryApproved(self,tokenID):
        return self.contract.functions.getApproved(tokenID).call()