package models

import (
	"github.com/ethereum/go-ethereum/common"
)

type Token struct {
	BaseModel
	ChainId     int64          `json:"chainId"`
	Address     common.Address `json:"address"`
	Name        string         `json:"name"`
	Symbol      string         `json:"symbol"`
	Decimals    uint8          `json:"decimals"`
	Tags        []string       `json:"tags" gorm:"-"`
	TotalSupply string         `json:"totalSupply"`
	LogoURI     string         `json:"logoURI"`
	Verify      bool           `json:"verify"`
}
type NFT struct {
	BaseModel
	ChainId     int64          `json:"chainId"`
	Address     common.Address `json:"address"`
	NFTID       string         `json:"nftID"`
	Name        string         `json:"name"`
	Symbol      string         `json:"symbol"`
	TotalSupply string         `json:"totalSupply"`
	LogoURI     string         `json:"logoURI"`
	Verify      bool           `json:"verify"`
	Owner       common.Address `json:"owner"`
}
type NFFT struct {
	BaseModel
	ChainId     int64          `json:"chainId"`
	Address     common.Address `json:"address"`
	NFTID       string         `json:"nftID"`
	Name        string         `json:"name"`
	Symbol      string         `json:"symbol"`
	TotalSupply string         `json:"totalSupply"`
	LogoURI     string         `json:"logoURI"`
	Verify      bool           `json:"verify"`
	// Owners      []common.Address `json:"owner"`
}
