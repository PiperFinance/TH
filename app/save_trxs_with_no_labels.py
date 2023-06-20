from sqlmodel import select

from models import Chain, Trx
from utils.trx.get_trxs import create_trx_objects
from configs.postgres_config import InitializePostgres

# def get_all_trxs():
#     chains = Chain.supported_chains()
#     trxs = []
#     for chain_id in chains:
#         trxs.extend(
#             list(Trx.mongo_client(chain_id).find())
#         )

#     trxs = create_trx_objects(trxs)
#     return trxs


def get_all_trxs():
    # chains = Chain.supported_chains()
    # trxs = []
    ps = InitializePostgres()
    # for chain_id in chains:
    #     trxs.extend(
    #         list(Trx.mongo_client(chain_id).find())
    #     )

    with ps.session as session:
        statement = select(Trx)
        results = session.exec(statement)
        trxs = results.all()

    trxs = create_trx_objects(trxs)
    return trxs


def get_trxs_with_input_and_no_labels(trxs):
    tx_list = []
    for trx in trxs:
        if trx.input:
            if not trx.labels:
                tx_list.append({
                    "chain_id": trx.chainId,
                    "hash": trx.hash
                })

    return tx_list
