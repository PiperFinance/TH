package controllers

import (
	"TH/src/conf"
	"TH/src/models"
	"context"

	"github.com/ethereum/go-ethereum/common"
)

func GetToken(c context.Context, chainId int64, address string) (*models.Token, error) {
	t := &models.Token{}
	if tx := conf.DB.WithContext(c).Where("token.address = ?", address).First(t); tx.Error != nil {
		return nil, tx.Error
	}
	add := common.HexToAddress(address)
	tok, err := conf.KC[chainId].GetToken(c, add)
	if err != nil {
		return nil, err
	}
	t.Address = add
	t.Symbol = tok.Symbol
	t.Name = tok.Name
	t.Decimals = tok.Decimals
	t.TotalSupply = tok.TotalSupply
	if tx := conf.DB.Create(&t); tx.Error != nil {
		return nil, tx.Error
	}
	return t, nil
}
