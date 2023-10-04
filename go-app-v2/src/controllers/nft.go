package controllers

import (
	"TH/src/conf"
	"TH/src/models"
	"context"
	"strconv"

	kc "github.com/PiperFinance/KC"
	"github.com/ethereum/go-ethereum/common"
	"github.com/eucrypt/unmarshal-go-sdk/pkg/constants"
)

func GetNFT(c context.Context, chainId int64, address string, id uint64) (*models.NFT, error) {
	t := &models.NFT{}
	if tx := conf.DB.WithContext(c).Where("nft.address = ?", address).First(t); tx.Error != nil {
		return nil, tx.Error
	}
	add := common.HexToAddress(address)
	tok, err := conf.KC[chainId].GetNFT(c, kc.NFTID{Address: add, ID: id})
	if err != nil {
		return nil, err
	}
	t.Address = add
	t.Symbol = tok.Symbol
	t.Name = tok.Name
	t.NFTID = id
	t.MetaData = tok.TokenURI
	t.TotalSupply = tok.TotalSupply
	if tx := conf.DB.Create(&t); tx.Error != nil {
		return nil, tx.Error
	}
	return t, nil
}

func SelectChain(chainId int64) constants.Chain {
	switch chainId {
	case 1:
		return constants.ETH
	case 56:
		return constants.BSC
	}
	return ""
}

func GetUserNFTs(c context.Context, chainId int64, address string) ([]*models.NFT, error) {
	chain := SelectChain(chainId)
	r := make([]*models.NFT, 0)
	if len(chain) == 0 {
		// TODO Chain not supported
		return r, nil
	}
	resp, err := conf.GetUnmarshal().GetNFTAssetsByAddress(chain, address)
	if err != nil {
		return nil, err
	}
	for _, v := range resp {
		id, err := strconv.ParseUint(v.TokenId, 10, 64)
		if err != nil {
			return nil, err
		}
		r = append(r, &models.NFT{
			ChainId:     chainId,
			Address:     common.HexToAddress(address),
			Symbol:      v.IssuerSpecificData.Name,
			Name:        v.IssuerSpecificData.Name,
			NFTID:       id,
			MetaData:    v.AnimationUrl,
			TotalSupply: "1",
			Owner:       common.HexToAddress(v.Owner),
		})
	}
	return r, nil
}
