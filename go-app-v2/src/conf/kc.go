package conf

import (
	kc "github.com/PiperFinance/KC"
)

var KC map[int64]*kc.Client

func LoadKC() {
	KC = make(map[int64]*kc.Client)
	for _, chain := range Config.SupportedChains {
		rpcs := make([]string, 0)
		for _, rpc := range SupportedNetworks[chain].GoodRpc {
			rpcs = append(rpcs, rpc.Url)
		}
		cl, err := kc.NewMultiChain(chain, rpcs)
		if err != nil {
			Logger.Panic(err)
		}
		KC[chain] = cl
	}
}
