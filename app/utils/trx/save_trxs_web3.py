# import requests
# import logging
# from web3 import Web3
# from pydantic import parse_obj_as
# from typing import List, Dict, Set
# from models import Trx, Chain
# from .decode_trx_input import decode_trx_input_data
# from utils.sync_redis import (
#     cache_last_block_number_web3,
#     get_last_block_number_web3
# )
# from .get_trxs import get_users_chain_token_trxs
# from utils.types import Address, ChainId, MongoClient


# def save_user_chain_token_trxs(
#     chain_id: ChainId,
#     address: Address
# ):

#     trxs = get_users_chain_token_trxs(chain_id, address)

#     start_block = get_last_block_number_web3(chain_id, address)
#     if start_block == 0:
#         start_block = int(trxs[-1].blockNumber)

#     last_block = int(trxs[0].blockNumber)

    
#     w3 = Chain(chainId=chain_id).w3
#     web3_trxs = []
#     for block_number in range(start_block, last_block):
#         block_data = w3.eth.get_block(block_number)
#         web3_trxs.extend(block_data.get("transactions"))
#         cache_last_block_number_web3(chain_id, address)

        
    

    

# def insert_nftbank_nfts(
#     chain_id: ChainId,
#     user_address: Address,
#     nfts: Set[]
# ):
#     client = Nft.mongo_client(chain_id)

#     need_to_be_saved, need_to_be_updated = return_should_be_inserted_and_updated(
#         client, user_address, nfts)

#     if need_to_be_saved not in [None, set()]:
#         need_to_be_saved = create_nftbank_nfts(
#             chain_id, user_address, need_to_be_saved)
#         insert_nfts(client, need_to_be_saved)

#     if need_to_be_updated not in [None, set()]:
#         update_nfts(client, user_address, need_to_be_updated)


# def return_should_be_inserted_and_updated(
#     client: MongoClient,
#     user_address: Address,
#     web3_trxs,
#     user_trxs
# ) -> Set[Set[]]:


#     for wtrx in web3_trxs:
#         for utrx in user_trxs:
#             wtrx.update(utrx)

#     need_to_be_updated = nftbank_nfts.intersection(user_nfts)
#     need_to_be_saved = nftbank_nfts.difference(user_nfts)

#     return need_to_be_saved, need_to_be_updated


# def update_nfts(
#     client: MongoClient,
#     user_address: Address,
#     nfts: Set[NftProxy]
# ):
#     for nft in nfts:
#         query = {
#             "userAddress": user_address,
#             "nftDetail.addressId": nft.addressId
#         }
#         newvalues = {"$set": {
#             "price": nft.price,
#             "value": nft.calculate_value(),
#             "nftDetail.verified": True
#         }}
#         balance = get_nft_balance(
#             nft.type,
#             nft.chainId,
#             nft.address,
#             nft.id,
#             user_address
#         )
#         if balance not in [None, 0]:
#             newvalues["$set"]["balance"] = str(balance)

#         total_supply = get_nft_total_supply(
#             nft.type,
#             nft.chainId,
#             nft.address,
#             nft.id,
#         )
#         if total_supply != None:
#             newvalues["$set"]["totalSupply"] = str(total_supply)
#         client.update_one(query, newvalues)





#     trxs = get_user_chain_token_trxs_web3(
#         chain_id,
#         address,
#         start_block
#     )
#     if trxs in [None, []]:
#         return

#     trxs = create_trxs(
#         chain_id,
#         address,
#         trxs
#     )
#     insert_trxs(
#         chain_id,
#         trxs
#     )


# def get_user_chain_token_trxs(
#     chain_id: ChainId,
#     address: Address,
#     start_block: int = 0
# ) -> List[Dict]:

#     chain = Chain(chainId=chain_id)
#     url = chain.url
#     api_keys = chain.api_keys

#     data = {
#         "address": address,
#         "startblock": start_block,
#         "endblock": 99999999,
#         "sort": "asc"
#     }

#     for api_key in api_keys:
#         try:
#             url = f"{url}?module=account&action=tokentx&apikey={api_key}"
#             res = requests.post(url=url, data=data)
#             res = res.json()
#             if res is not None and (res.get("message") == "OK" or res.get("message") == "No transactions found"):
#                 return res.get("result")
#         except Exception as e:
#             logging.exception(f"{e} -> API Key didn't work.")
#             continue


# def create_trxs(
#         chain_id: ChainId,
#         address: Address,
#         users_trxs: List[Dict]
# ) -> List[Trx]:
#     trxs = []

#     for trx in users_trxs:
#         trx["userAddress"] = Web3.toChecksumAddress(address)
#         labels = decode_trx_input_data(trx.get("input"))
#         if labels:
#             trx["labels"] = labels
#         trx["chainId"] = chain_id
#         trx["fromAddress"] = trx.get("from")
#         trx["timeStamp"] = int(trx.get("timeStamp"))
#         trx_obj = parse_obj_as(Trx, trx)
#         trxs.append(trx_obj.dict())

#     return trxs


# def insert_trxs(
#     chain_id: ChainId,
#     trxs: List[Dict]
# ):
#     client = Trx.mongo_client(chain_id)

#     for trx in trxs:
#         try:
#             client.insert_one(trx)
#             cache_last_block_number(
#                 chain_id,
#                 trx.get("userAddress"),
#                 trx.get("blockNumber")
#             )
#         except Exception as e:
#             logging.exception(e)
#             continue


