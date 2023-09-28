package controllers

import (
	"TH/src/conf"
	"TH/src/models"
	"context"
	"strings"
)

func GetAddERC721Trx(ctx context.Context, chainId int, address string) ([]models.Trx, error) {
	r := make([]models.Trx, 0)
	if tx := conf.DB.WithContext(ctx).Where(models.Trx{ChainId: chainId, User: address}).Find(&r); tx.Error != nil {
		return nil, tx.Error
	}
	return r, nil
}

func UpdateAddERC721Trx(c context.Context, chainId int64, address string) error {
	end, err := conf.LatestBlock(c, chainId)
	if err != nil {
		return err
	}
	start := LastPreFetchedTrx(c, "721", chainId, address)
	if start == 0 {
		// TODO : make this a bit more dynamic
		start = end - 10000
	}
	var lastfetched int
	if end-start > 2 {

		lastfetched, err = UpdateAddERC721TrxInRange(c, chainId, address, start, end)
		if err != nil && !strings.Contains(err.Error(), "No transactions found") {
			return err
		}
	}
	if end < uint64(lastfetched) {
		end = uint64(lastfetched)
	}
	return SetLastPreFetchedTrx(c, "721", chainId, address, end)
}

func UpdateAddERC721TrxInRange(c context.Context, chainId int64, address string, start uint64, end uint64) (int, error) {
	i, lastBlock := 0, 0
	// TODO : store last index , max depth of 5 , go deeper if requested
	for {
		_lastBlock, err := UpdateAddERC721TrxInRangePaginated(c, chainId, address, start, end, i, 100)
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

func UpdateAddERC721TrxInRangePaginated(c context.Context, chainId int64, address string, start uint64, end uint64, page int, pageSize int) (int, error) {
	sc, ok := conf.Scanner[chainId]
	if !ok {
		// TODO : Error here
		return 0, nil
	}
	istart, iend := int(start), int(end)
	conf.Logger.Infow("--ERC721-->", "add", address, "start", istart, "end", iend, "pg", page, "ps", pageSize)
	defer conf.Logger.Infow("<--ERC721--", "add", address, "start", istart, "end", iend, "pg", page, "ps", pageSize)
	trx, err := sc.ERC721Transfers(nil, &address, &istart, &iend, page, pageSize, true)
	if err != nil {
		return 0, err
	}
	allTx := make([]models.Erc721Trx, 0)
	lastblock := 0
	for _, tx := range trx {
		allTx = append(allTx, models.Erc721Trx{
			ChainId:   int(chainId),
			User:      address,
			Timestamp: tx.TimeStamp.Time(),
			Input:     tx.Input,
			Hash:      tx.Hash,
			From:      tx.From,
			To:        tx.To,
			Name:      tx.TokenName,
			Symbol:    tx.TokenSymbol,
			TokenID:   tx.TokenID.Int().String(),
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
