
async def _tt_():
    from utils.trx.save_trxs import save_user_chain_token_trxs
    from utils.trx.get_trxs import get_user_chain_token_trxs
    from models import FunctionSelector, Trx
    from configs.redis_config import cache_client
    from utils.trx.decode_trx_input import decode_trx_input_data

    # keys = ["lbt:", "fus:", "lap:"]
    # for key_pattern in keys:
    #     for key in cache_client().keys(f"{key_pattern}*"):
    #         cache_client().delete(key)

    # t1 = Trx.mongo_client(1)
    # t2 = Trx.mongo_client(250)
    # f = FunctionSelector.mongo_client()

    # t1.drop()
    # t2.drop()
    # f.drop()

    # q = list(t1.find())
    # s = list(t2.find())
    # v = list(f.find())

    # c = FunctionSelector.mongo_client()
    # c.insert_one({
    #     "hex": "0xa9059cbb",
    #     "text": "Transfer",
    #     "args": [
    #         (
    #             "to", "address"
    #         ),
    #         (
    #             "amount", "uint256"
    #         )
    #     ]
    # })

    # decode_trx_input_data(
    #     "0xa9059cbb0000000000000000000000000e747eb2ff0f26fb77c3a1ea67ee07fac2dbb78300000000000000000000000000000000000000000000000000000000023e7e50")

    skip = 0
    limit = 100

    # save_user_chain_token_trxs(
    #     1, "0x416299AAde6443e6F6e8ab67126e65a7F606eeF5")

    # save_user_chain_token_trxs(
    #     1, "0x7d1F235a2eD3f71143c7eD0f5CB1A40b5b5d1aa6")

    # get_user_chain_token_trxs(
    # 1, "0x416299AAde6443e6F6e8ab67126e65a7F606eeF5", skip, limit)

    # get_user_chain_token_trxs(
    #     1, "0x7d1F235a2eD3f71143c7eD0f5CB1A40b5b5d1aa6", skip, limit)

    # get_user_chain_token_trxs(
    #     1, "0x416299AAde6443e6F6e8ab67126e65a7F606eeF5", skip + 5, limit)

    # get_user_chain_token_trxs(
    #     1, "0x416299AAde6443e6F6e8ab67126e65a7F606eeF5", skip + 10, limit)

    # get_user_chain_token_trxs(
    #     1, "0x416299AAde6443e6F6e8ab67126e65a7F606eeF5", skip + 15, limit)

    pass
