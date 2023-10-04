package main

import (
	"fmt"

	unmarshal "github.com/eucrypt/unmarshal-go-sdk/pkg"
	conf "github.com/eucrypt/unmarshal-go-sdk/pkg/config"
	"github.com/eucrypt/unmarshal-go-sdk/pkg/constants"
)

func main2() {
	sdk := unmarshal.NewWithConfig(conf.Config{
		AuthKey:     "6twN3azQPqW8SwTZXGdssZsbfgUtFk1DVhmUSXH3",
		Environment: constants.Prod,
	})

	resp, err := sdk.GetNFTAssetsByAddress(constants.BSC, "0xB49F17514D6F340d7bcdFfC47526C9A3713697e0")
	fmt.Println(resp, err)
}
