package controllers

import (
	"TH/src/conf"
	"TH/src/models"
	"context"
	"strings"
)

func GetAddERC20Trx(ctx context.Context, chainId int, address string) ([]models.Erc20Trx, error) {
	r := make([]models.Erc20Trx, 0)
	if tx := conf.DB.WithContext(ctx).Where(models.Erc20Trx{ChainId: chainId, User: address}).Find(&r); tx.Error != nil {
		return nil, tx.Error
	}
	return r, nil
}

func UpdateAddERC20Trx(c context.Context, chainId int64, address string) error {
	if isRunning(c, "20", chainId, address) {
		return nil
	} else {
		setRunning(c, "20", chainId, address)
		defer setFinished(c, "20", chainId, address)
	}
	end, err := conf.LatestBlock(c, chainId)
	if err != nil {
		return err
	}
	start := LastPreFetchedTrx(c, "20", chainId, address)
	if start == 0 {
		// TODO : make this a bit more dynamic
		start = end - conf.Config.MaxScannerDepth
	}
	var lastfetched int
	if end-start > conf.Config.ScannerBlockDelay {
		lastfetched, err = UpdateAddERC20TrxInRange(c, chainId, address, start, end)
		if err != nil && !strings.Contains(err.Error(), "No transactions found") {
			return err
		}
	}
	if end < uint64(lastfetched) {
		end = uint64(lastfetched)
	}
	return SetLastPreFetchedTrx(c, "20", chainId, address, end)
}

func UpdateAddERC20TrxInRange(c context.Context, chainId int64, address string, start uint64, end uint64) (int, error) {
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

func UpdateAddERC20TrxInRangePaginated(c context.Context, chainId int64, address string, start uint64, end uint64, page int, pageSize int) (int, error) {
	sc, ok := conf.Scanner[chainId]
	if !ok {
		// TODO : Error here
		return 0, nil
	}
	istart, iend := int(start), int(end)
	conf.Logger.Infow("--ERC20-->", "add", address, "start", istart, "end", iend, "pg", page, "ps", pageSize)
	defer conf.Logger.Infow("<--ERC20--", "add", address, "start", istart, "end", iend, "pg", page, "ps", pageSize)
	trx, err := sc.ERC20Transfers(nil, &address, &istart, &iend, page, pageSize, true)
	if err != nil {
		return 0, err
	}
	allTx := make([]models.Erc20Trx, 0)
	lastblock := 0
	for _, tx := range trx {
		allTx = append(allTx, models.Erc20Trx{
			ChainId:   int(chainId),
			User:      address,
			Timestamp: tx.TimeStamp.Time(),
			Input:     tx.Input,
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
			TxType:    models.TOKEN_TRX,
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
