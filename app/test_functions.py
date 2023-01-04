
async def _tt_():
    from utils.trx.save_trxs import save_user_chain_token_trxs, save_users_chain_token_trxs
    from utils.trx.get_trxs import get_users_chain_token_trxs
    from models import FunctionSelector, Trx
    from configs.redis_config import cache_client
    from utils.trx.decode_trx_input import decode_trx_input_data

    # keys = cache_client().keys("*")
    # cache_client().delete(*keys)

    # Trx.mongo_client(10).drop()

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
    # decode_trx_input_data(1, "0x9572413b699bc52309a092aad6b4a339a94a45bd8d333b286445039ad8089298",
    #                       "0xa9059cbb0000000000000000000000002aa0f37da89bceebe7632322fa1f1ac323e391ac000000000000000000000000000000000000000000000000000000000b816770")
    
    # decode_trx_input_data(56, "0x95c7b9fb65d6e590da25c6795620dac5d99627157a34df5de0a358abaebd1583", "0x5f575529000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000429d069189e000000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000000147061726173776170563546656544796e616d696300000000000000000000000000000000000000000000000000000000000000000000000000000000000005600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e9e7cea3dedca5984780bafc599bd69add087d560000000000000000000000000000000000000000000000000429d069189e000000000000000000000000000000000000000000000000000869d86888b182371e00000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000001399bbccdc1c72de000000000000000000000000bfbd0c5f45596d563a9401025957da540f4b3a100000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000042454e3f31b0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000e9e7cea3dedca5984780bafc599bd69add087d560000000000000000000000000000000000000000000000000429d069189e00000000000000000000000000000000000000000000000000087cdb9c23e32d2baa000000000000000000000000000000000000000000000008c00f44991efc6c5a00000000000000000000000000000000000000000000000000000000000001e00000000000000000000000000000000000000000000000000000000000000220000000000000000000000000000000000000000000000000000000000000034000000000000000000000000000000000000000000000000000000000000003a0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006d6574616d61736b32000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003e00000000000000000000000000000000000000000000000000000000061ae13d0630ff360566811ecabed4929076aeec300000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000053e693c6c7ffc4446c53b205cf513105bf140d7b00000000000000000000000000000000000000000000000000000000000000e491a32b69000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee0000000000000000000000000000000000000000000000000429d069189e00000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000bb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c00000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000001000000000000000000004df81b96b92314c44b159149f7e0303511fb2fc4774f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000e400000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000429d069189e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    skip = 0
    limit = 100

    # save_users_chain_token_trxs(
    #     56, ["0x416299AAde6443e6F6e8ab67126e65a7F606eeF5"])

    # save_users_chain_token_trxs(
    #     1, ["0x73205B2F021E519f75418Ce41C33Dbae9470C238"])

    # get_users_chain_token_trxs(
    # 1, ["0x416299AAde6443e6F6e8ab67126e65a7F606eeF5"], skip, limit)

    # get_users_chain_token_trxs(
    #     1, ["0x7d1F235a2eD3f71143c7eD0f5CB1A40b5b5d1aa6"], skip, limit)

    # get_users_chain_token_trxs(
    #     1, ["0x416299AAde6443e6F6e8ab67126e65a7F606eeF5"], skip + 5, limit)

    # get_users_chain_token_trxs(
    #     1, ["0x416299AAde6443e6F6e8ab67126e65a7F606eeF5"], skip + 10, limit)

    # get_users_chain_token_trxs(
    #     1, ["0x416299AAde6443e6F6e8ab67126e65a7F606eeF5"], skip + 15, limit)

    pass
