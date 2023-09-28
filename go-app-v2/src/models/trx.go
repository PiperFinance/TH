package models

import "time"

type TxType string

const (
	NORMAL_TRX = "normal"
	TOKEN_TRX  = "token"
)

type Trx struct {
	BaseModel
	User      string    `json:"user"`
	ChainId   int       `json:"chainId"`
	TxType    TxType    `json:"txType"`
	Block     int       `json:"blockNumber"`
	Timestamp time.Time `json:"timestamp"`
	Hash      string    `json:"hash"`
	Nonce     int       `json:"nonce"`
	BlockHash string    `json:"blockHash"`

	// Address   string `json:"userAddress"`
	From     string `json:"from"`
	To       string `json:"to"`
	Contract string `json:"contract"`
	Value    string `json:"value"`
	TrxIndex int    `json:"trxIndex"`
	Gas      int    `json:"gas"`
	GasUsed  int    `json:"gasUsed"`
	GasPrice string `json:"gasPrice"`
	Input    string `json:"input"`
	IsError  bool   `json:"isError"`
	Status   string `json:"status"`
}

type Erc20Trx struct {
	BaseModel
	User      string    `json:"user"`
	ChainId   int       `json:"chainId"`
	TxType    TxType    `json:"txType"`
	Block     int       `json:"blockNumber"`
	Timestamp time.Time `json:"timestamp"`
	Hash      string    `json:"hash"`
	Nonce     int       `json:"nonce"`
	BlockHash string    `json:"blockHash"`

	// Address   string `json:"userAddress"`
	From     string `json:"from"`
	To       string `json:"to"`
	Contract string `json:"contract"`
	Value    string `json:"value"`
	TrxIndex int    `json:"trxIndex"`
	Gas      int    `json:"gas"`
	GasUsed  int    `json:"gasUsed"`
	GasPrice string `json:"gasPrice"`
	Input    string `json:"input"`
}

type Erc721Trx struct {
	BaseModel
	User      string    `json:"user"`
	ChainId   int       `json:"chainId"`
	TxType    TxType    `json:"txType"`
	Block     int       `json:"blockNumber"`
	Timestamp time.Time `json:"timestamp"`
	Hash      string    `json:"hash"`
	Nonce     int       `json:"nonce"`
	BlockHash string    `json:"blockHash"`

	// Address   string `json:"userAddress"`
	From     string `json:"from"`
	To       string `json:"to"`
	Contract string `json:"contract"`
	TokenID  string `json:"tokenId"`
	Name     string `json:"name"`
	Symbol   string `json:"symbol"`
	TrxIndex int    `json:"trxIndex"`
	Gas      int    `json:"gas"`
	GasUsed  int    `json:"gasUsed"`
	GasPrice string `json:"gasPrice"`
	Input    string `json:"input"`
}
