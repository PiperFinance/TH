package controllers

import (
	"TH/src/conf"
	"TH/src/models"
	"TH/src/schema"
	"context"

	"github.com/ethereum/go-ethereum/common"
)

func GetToken(c context.Context, chainId int64, address string) (*models.Token, error) {
	t := &models.Token{}
	if tx := conf.DB.WithContext(c).Where("token.address = ?", address).First(&t); tx.Error != nil {
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

func GetUserTokens(c context.Context, chainId int64, address string) ([]*schema.Token, error) {
	chain := SelectChain(chainId)
	r := make([]*schema.Token, 0)
	if len(chain) == 0 {
		// TODO: Chain not supported
		return r, nil
	}
	resp, err := conf.GetUnmarshal().GetTokenAssets(chain, address)
	if err != nil {
		return nil, err
	}
	for _, v := range resp {
		// tok, err := GetToken(c, chainId, v.ContractAddress)
		// if err != nil {
		// 	return nil, err
		// }
		r = append(r, &schema.Token{
			// Detail: schema.TokenDet{
			// 	Address:  common.HexToAddress(v.ContractAddress),
			// 	ChainId:  chainId,
			// 	Symbol:   tok.Symbol,
			// 	Name:     tok.Name,
			// 	Decimals: int32(tok.Decimals),
			// 	LogoURI:  v.LogoUrl,
			// 	Verify:   tok.Verify,
			// 	Tags:     []string{v.Type},
			// },
			Detail: schema.TokenDet{
				ChainId:  chainId,
				Address:  common.HexToAddress(v.ContractAddress),
				Name:     v.ContractName,
				Symbol:   v.ContractTickerSymbol,
				Decimals: int32(v.ContractDecimals),
				LogoURI:  v.LogoUrl,
				Tags:     []string{v.Type},
			},
			BalanceStr:          v.Balance,
			BalanceNoDecimalStr: v.Balance,
			PriceUSD:            v.Quote,
		})
	}
	return r, nil
}
