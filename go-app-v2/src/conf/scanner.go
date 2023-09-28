package conf

import (
	"time"

	sp "github.com/NFEL/etherscan-api-multikey"
)

var (
	Scanner map[int64]*sp.Client

	explorerURLMap = map[int64]string{
		1:          "https://api.etherscan.io/api?",
		10:         "https://api-optimistic.etherscan.io/api?",
		56:         "https://api.bscscan.com/api?",
		110:        "https://api.gnosisscan.io/api?",
		137:        "https://api.polygonscan.com/api?",
		250:        "https://api.ftmscan.com/api?",
		1284:       "https://api-moonbeam.moonscan.io/api?",
		42220:      "https://api.celoscan.io/api?",
		42161:      "https://api.arbiscan.io/api?",
		43114:      "https://api.snowtrace.io/api?",
		1313161554: "https://api.aurorascan.dev/api?",

		// 43113: "https://api.avax.network/ext/bc/C/rpc?",
	}
)

func LoadScanner() {
	LoadSecretStoage(Config.GITHUB_TOKEN)
	Scanner = make(map[int64]*sp.Client)
	for _, chain := range Config.SupportedChains {
		keys, ok := Secrets.ScannerApiKey[chain]
		if !ok {
			Logger.Warnf("missing scanner api key for chain %d", chain)
			continue
		}
		Scanner[chain] = sp.NewCustomized(sp.Customization{
			Timeout: 30 * time.Second,
			Keys:    keys,
			BaseURL: explorerURLMap[chain],
		})
	}
}
