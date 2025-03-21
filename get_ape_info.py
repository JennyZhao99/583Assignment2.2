from web3 import Web3
from web3.providers.rpc import HTTPProvider
import requests
import json

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)

# You will need the ABI to connect to the contract
# The file 'abi.json' has the ABI for the bored ape contract
# In general, you can get contract ABIs from etherscan
# https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('ape_abi.json', 'r') as f:
    abi = json.load(f)

############################
# Connect to an Ethereum node
api_url = "https://mainnet.infura.io/v3/03016c3bbdb5494f962fcd2d8ac441f1"  # YOU WILL NEED TO PROVIDE THE URL OF AN ETHEREUM NODE
provider = HTTPProvider(api_url)
web3 = Web3(provider)

# load the Bored Ape contract
contract = web3.eth.contract(address=contract_address, abi=abi)

def get_ape_info(ape_id):
    assert isinstance(ape_id, int), f"{ape_id} is not an int"
    assert 0 <= ape_id, f"{ape_id} must be at least 0"
    assert 9999 >= ape_id, f"{ape_id} must be less than 10,000"

    data = {'owner': "", 'image': "", 'eyes': ""}

    # YOUR CODE HERE
    # step 1: get the owner of the ape
    owner = contract.functions.ownerOf(ape_id).call()
    data['owner'] = owner

    # step 2: get the tokenURI for the ape
    token_uri = contract.functions.tokenURI(ape_id).call()
    
    # step 3: Fetch metadata from IPFS
    # Replace 'ipfs://' with 'https://ipfs.io/ipfs/' to use the public IPFS gateway
    ipfs_url = token_uri.replace("ipfs://", "https://ipfs.io/ipfs/")
    response = requests.get(ipfs_url)
    metadata = response.json()

    # step 4: Extract image and eyes attributes
    data['image'] = metadata['image']
    data['eyes'] = metadata['attributes'][1]['value']  # assume 'eyes' is the second attribute

    assert isinstance(data, dict), f'get_ape_info{ape_id} should return a dict'
    assert all([a in data.keys() for a in
                ['owner', 'image', 'eyes']]), f"return value should include the keys 'owner','image' and 'eyes'"
    return data
