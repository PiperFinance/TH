package controllers

import (
	"TH/src/conf"
	"TH/src/models"
	"context"
	"strings"
)

func GetAddTrx(ctx context.Context, chainId int, address string) ([]models.Trx, error) {
	r := make([]models.Trx, 0)
	if tx := conf.DB.WithContext(ctx).Where(models.Trx{ChainId: chainId, User: address}).Find(&r); tx.Error != nil {
		return nil, tx.Error
	}
	return r, nil
}

func UpdateAddTrx(c context.Context, chainId int64, address string) error {
	end, err := conf.LatestBlock(c, chainId)
	if err != nil {
		return err
	}
	start := LastPreFetchedTrx(c, "n", chainId, address)
	if start == 0 {
		// TODO : make this a bit more dynamic
		start = end - 10000
	}
	var lastfetched int
	if end-start > 2 {

		lastfetched, err = UpdateAddTrxInRange(c, chainId, address, start, end)
		if err != nil && !strings.Contains(err.Error(), "No transactions found") {
			return err
		}
	}
	if end < uint64(lastfetched) {
		end = uint64(lastfetched)
	}
	return SetLastPreFetchedTrx(c, "n", chainId, address, end)
}

func UpdateAddTrxInRange(c context.Context, chainId int64, address string, start uint64, end uint64) (int, error) {
	i, lastBlock := 0, 0
	// TODO : store last index , max depth of 5 , go deeper if requested
	for {
		_lastBlock, err := UpdateAddERC20TrxInRangePaginated(c, chainId, address, start, end, i, 100)
		if err != nil {
			return lastBlock, err
		}
		if lastBlock < _lastBlock {
			lastBlock = _lastBlock
		}
		if _lastBlock == 0 {
			return lastBlock, nil
		}
		i++
	}
}

func UpdateAddTrxInRangePaginated(c context.Context, chainId int64, address string, start uint64, end uint64, page int, pageSize int) (int, error) {
	sc, ok := conf.Scanner[chainId]
	if !ok {
		// TODO : Error here
		return 0, nil
	}
	istart, iend := int(start), int(end)
	conf.Logger.Infow("---->", "add", address, "start", istart, "end", iend, "pg", page, "ps", pageSize)
	defer conf.Logger.Infow("<------", "add", address, "start", istart, "end", iend, "pg", page, "ps", pageSize)
	trx, err := sc.NormalTxByAddress(address, &istart, &iend, page, pageSize, true)
	if err != nil {
		return 0, err
	}
	allTx := make([]models.Trx, 0)
	lastblock := 0
	for _, tx := range trx {
		allTx = append(allTx, models.Trx{
			ChainId:   int(chainId),
			User:      address,
			Timestamp: tx.TimeStamp.Time(),
			Input:     tx.Input,
			IsError:   tx.IsError == 1,
			Hash:      tx.Hash,
			From:      tx.From,
			To:        tx.To,
			Value:     tx.Value.Int().String(),
			Gas:       tx.Gas,
			GasUsed:   tx.GasUsed,
			GasPrice:  tx.GasPrice.Int().String(),
			Block:     tx.BlockNumber,
			Nonce:     tx.Nonce,
			BlockHash: tx.BlockHash,
			TxType:    models.NORMAL_TRX,
			Status:    tx.TxReceiptStatus,
			TrxIndex:  tx.TransactionIndex,
			Contract:  tx.ContractAddress,
		})
		if tx.BlockNumber > lastblock {
			lastblock = tx.BlockNumber
		}
	}
	if len(allTx) > 0 {
		if tx := conf.DB.Create(&allTx); tx.Error != nil {
			return lastblock, tx.Error
		}
	}
	return lastblock, nil
}
