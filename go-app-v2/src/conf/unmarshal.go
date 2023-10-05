package conf

import (
	"sync"

	unmarshal "github.com/eucrypt/unmarshal-go-sdk/pkg"
	conf "github.com/eucrypt/unmarshal-go-sdk/pkg/config"
	"github.com/eucrypt/unmarshal-go-sdk/pkg/constants"
)

var (
	sdks               []*unmarshal.Unmarshal
	selectUnmarshalIdx int
	selectUnmarshalSdk sync.Mutex
)

func GetUnmarshal() *unmarshal.Unmarshal {
	selectUnmarshalSdk.Lock()
	defer selectUnmarshalSdk.Unlock()
	selectUnmarshalIdx++
	if selectUnmarshalIdx >= len(sdks) {
		selectUnmarshalIdx = 0
	}
	return sdks[selectUnmarshalIdx]
}

func LoadUnmarshal() {
	for _, apiKey := range Secrets.UnmarshalApiKeys {
		sdk := unmarshal.NewWithConfig(conf.Config{
			AuthKey:     apiKey,
			Environment: constants.Prod,
		})
		sdks = append(sdks, &sdk)
	}
}
