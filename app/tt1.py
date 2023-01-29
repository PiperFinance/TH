

def get_trxs_with_input_and_no_labels(trxs):
    tx_list = []
    for trx in trxs:
        if trx.input:
            if not trx.labels:
                tx_list.append({
                    "chain_id": trx.chainId,
                    "hash": trx.hash
                })

    print(tx_list)
    return tx_list
