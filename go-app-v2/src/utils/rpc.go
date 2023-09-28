package utils

import (
	"TH/src/schema"
	"context"
	"time"

	"github.com/ethereum/go-ethereum/ethclient"
	"go.uber.org/zap"
)

func logErr(Logger *zap.SugaredLogger, s time.Time, rpc string, err error) {
	eStr := err.Error()
	if len(eStr) > 15 {
		eStr = eStr[:15]
	}
	Logger.Debugf("[%d]ms  %s %s", time.Since(s).Milliseconds(), eStr, rpc)
}

func logOk(Logger *zap.SugaredLogger, s time.Time, rpc string, block int) {
	Logger.Infof("[%d]ms  %d %s", time.Since(s).Milliseconds(), block, rpc)
}

func GetNetworkRpcUrls(rpcs []*schema.RPC) []string {
	r := make([]string, len(rpcs))
	for i, rpc := range rpcs {
		r[i] = rpc.Url
	}
	return r
}

// NetworkConnectionCheck check if rpc is connected + does have getLogs method !
func NetworkConnectionCheck(Logger *zap.SugaredLogger, network *schema.Network, timeout time.Duration) {
	// TODO:  Add test opts !
	Logger.Infof("---------------------------> %s\n", network.Name)
	c, cancel := context.WithTimeout(context.Background(), timeout)
	for _, rpc := range network.Rpc {
		go func(rpc schema.RPC) {
			_rpcUrl := rpc.Url
			if len(_rpcUrl) < 1 {
				return
			}
			s := time.Now()
			if cl, err := ethclient.Dial(_rpcUrl); err == nil {
				if block, err := cl.BlockNumber(c); err != nil {
					logErr(Logger, s, _rpcUrl, err)
				} else {
					logOk(Logger, s, _rpcUrl, int(block))
					network.GoodRpc = append(network.GoodRpc, &rpc)
					return
				}
			} else {
				logErr(Logger, s, _rpcUrl, err)
			}
			network.BadRpc = append(network.BadRpc, &rpc)
		}(rpc)
	}
	time.Sleep(timeout)
	cancel()
	time.Sleep(10 * time.Millisecond)
	Logger.Infow("NetworkTestResult", "network", network.ChainId, "bad", len(network.BadRpc), "good", len(network.GoodRpc), "total", len(network.Rpc))
}
