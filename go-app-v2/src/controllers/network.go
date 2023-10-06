package controllers

import "github.com/eucrypt/unmarshal-go-sdk/pkg/constants"

func SelectChain(chainId int64) constants.Chain {
	switch chainId {
	case 1:
		return constants.ETH
	case 42161:
		return constants.ARBITRUM
	case 43114:
		return constants.AVALANCHE
	case 42220:
		return constants.CELO
	case 122:
		return constants.FUSE
	case 128:
		return constants.HUOBI
	case 8217:
		return constants.KLAYTN
	case 10:
		return constants.OPTIMISM
	case 25:
		return constants.CRONOS
	case 106:
		return constants.VELAS
	case 50:
		return constants.XDC
	case 32769:
		return constants.ZILLIQA
	case 1284:
		return constants.MOONBEAM
	case 1088:
		return constants.METIS
	case 1313161554:
		return constants.AURORA
	case 1101:
		return constants.ZKEVM
	case 5000:
		return constants.MANTLE_ALPHA
	case 137:
		return constants.MATIC
	case 250:
		return constants.FANTOM
	case 56:
		return constants.BSC
	}
	return ""
}
