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
	if err != nil {
		fmt.Println(resp, err)
	}
	/*
		[{0x37707dd3616479875855bf2f9088dbbe6e8e434e 1347 0xB49F17514D6F340d7bcdFfC47526C9A3713697e0 https://doodleapes.meta.rareboard.com/api/1347.json 721 1 {jJFRa5MxFIb/SjjehrZicfW7azsHThHaytSKlLMvW
		XNocpImJ6sfY/9dAjKqeNHb8D5vnjd5AsZgoYPrGI23ap5sUYvNUr16/WZ6BRqMLX2mJBQZOnirJ5OJcshGmYwnVudYZCXOqsXnhdoEzKKWDolHoIEC7tslTiSVbjyuHDAXh34UhkSMgqPex2rGlB7KeBXMfDtfra++3Zjbr0e8+zil6ffrcDOb2uNMHrbLd9
		tbdnfr+Xr1fgYa7C+xmdHvavbQAWhAkUz3VWyB7scTSEaSnQzJQgf32B/2OVY2oOERfW1mn8hj3+ZSSR6H3Z8sPOt/6N5HcbaAfkET8UGVk0WxWZ1InOrb7kvKyoFa7hF9bRKt6RLMDn8JbI6VWIj3l7AhVnFn9vtcQxr+R/7UIBlJCnRcvdeQckw2C9mXkw/
		tX78Mqcm3V2cKKBR5V7OHDuD5NwAAAP//AQAA//8= https://unmarshal.mypinata.cloud/ipfs/QmdAZAQR7XFdJWqaVK4i4YDmF84eq8tfZC9ZJnhVRARQE8 doodle apes bsc #1347}   6,000 hand drawn Doodle Apes on the BNB S
		mart Chain. [{background Lilac } {clothes pink sweater with chain } {skin pink } {eyes Squinting } {mouth grumpy }]} {0x37707dd3616479875855bf2f9088dbbe6e8e434e 1459 0xB49F17514D6F340d7bcdFfC47
		526C9A3713697e0 https://doodleapes.meta.rareboard.com/api/1459.json 721 1 {jJLfixMxEMf/lTC+hrZXquK+9YeiIuLZPp1Ime5Od8dNJiGZXLsc97/LghxVfNjXkO/nk8l3nkDQE1SwC6FxZNaRstnst+bV3er1O7DQUK4TR+UgUMEbu1
		gsTIfSmCbhRcxtLIjRjszm68bsPSY12w5ZZmCBPbajpFONuZrPi3hMuUM380NkQcVZ7UJp5hzPeX7vyeclP3xcr67n6/fzXf3t8+rte17vfi0/hN390sfu0OrhyyXiQw0W6KqUBN2xJAcVgAVUTXwqShmqH0+gCVmPOkSCCk5Y920KRRqw8IiujC/bkqM0jPN
		yjg6H45/L8Gz/idcuaEcZ7Et2IOfCxZyw7iPW/RRI7lluCG3ChknURJbejL8bEkpLU1Ad6g3JsSfzyD1LOyVMw1+T7COm3k3S+lC0uxF7bP4n/GlBE7JmqKQ4ZyGmECkp08vJp3E5DkMcaxirE/aoHORYkoMK4Pk3AAAA//8BAAD//w== https://unmarsh
		al.mypinata.cloud/ipfs/Qmems2iZHA4xfxRf1cPJ47EiADj2FoDQ2mphTgtTLwpaZc doodle apes bsc #1459}   6,000 hand drawn Doodle Apes on the BNB Smart Chain. [{background Celery } {clothes yellow backpac
		k } {skin gradient pink and orange } {hat lime viking } {eyes Sparkle } {mouth mad }]} {0x37707dd3616479875855bf2f9088dbbe6e8e434e 1555 0xB49F17514D6F340d7bcdFfC47526C9A3713697e0 https://doodle
		apes.meta.rareboard.com/api/1555.json 721 1 {jJJRi1M9EIb/SpjvNrT9lPbi3G2rLIourtvFBZEyPWc8CSeZxGTSNrvsf5eALFUEexvyPvM+yTwBoyfo4E0IgyN1FSmr9d1G/ff/crkEDQPlPtkoNjB0sNKLxUIZ5EENCY+szmOBlRhS65u1uvOY
		RG0MWp6BButxbEOMSMzdfF7YY8oG3czXaBkFZ70LZZjb+D3Pb/02rB6vN3YsHE8/jqHeT+tVvTm9yrdfjq/Nw+HTw1ss95/fb68+PIIGOgklRrcryUEHoAFFkt0XoQzd1yeQhFZ2UiNBB3vspzGFwgNoOKArrdlHy9JsbY4O6+7XVXjWf4R7F8RQBv2SrORcO
		Ko99lPEfroEkifLZ4Qx4WCJRUXLk2pvGxLySJegDLbaB3SlWXjKuaoxETX+P2Wo/mZynYqP9ZKpPhQxZwYG49+D3zRIQisZOi7OaYgpREpi6eXkXduNbY2tf/s5th7FBt6V5KADeP4JAAD//wEAAP// https://unmarshal.mypinata.cloud/ipfs/QmT
		o6zGCigunpxqwoyUkB6yNx2sQWw3hXvPXEauURJTALz doodle apes bsc #1555}   6,000 hand drawn Doodle Apes on the BNB Smart Chain. [{background Mint } {clothes yellow backpack } {skin gradient pink and
		orange } {hat messy green } {eyes Grumpy } {mouth happy }]} {0x87a218ae43c136b3148a45ea1a282517794002c8 882997 0xB49F17514D6F340d7bcdFfC47526C9A3713697e0 https://gateway.pinata.cloud/ipfs/QmWxB
		bFG3WJXVTDqrFUPhMuLmeHqKNBBkzSuvQyyk7ftfi/CodeConqueror-Bnb.json 721 1 {TJFPb9NAEMW/yrDn4KiVEOAjUUFIFQo0LX8u1dge20N2d5bZ2TYO4rsjJ22To8e/9968nb8uYiBXuzXGTrGGlXS0kvinkIq6hesot8rJWOILBZwBI0iI3I7IE
		b583EAr3lM7c9AU9gaPbCPst3DNw2iw8kzRQCJc40T6i1QqWB9CM7QYwRQfyAO2KjlDx31POisaL+32EJMr2Iw0wSOhngFSrGfLs/VJdRQAxg5sJFaQti0J5/UyoBJ0ZKSBI3XQTDMDDauNR2EFP6VAwOm51Znz8aEymEAuIUgEfJrBluNQwdUueVE6eIYpGy
		lTBumfKM94WGvEB4K+xFdu4TjgMB9hNEu5Xi4HNHrEqUoc0bBqvZRuyanPy6+hG27C3YDbzXBxKzcb2739dHXbpf2b9ffLy3f7b6Hf3l3k9z9sHa+XKzm75usPsal+p+E58L6od7VzC0c7I43oTxM0U26KUXZ1LN4vnCmyvXwllURqfPr/ee6wmdLcwy0cRg5
		oLPG+qHe1c//+AwAA//8BAAD//w== https://gateway.pinata.cloud/ipfs/QmdgSmVgakTg1UoSTtx7GEUdpz5PW228zRmfkV1s9XtPnL/CodeConqueror-Bnb.jpg Pandra: CodeConqueror}   Pandra is an omnichain NFT collecti
		on built with zk Light Client on LayerZero. Pandras can travel across different blockchains. They wear different outfits on different chains and their occupations are determined by the birth ch
		ain. You may collect different Pandras to summon a Pandra king. Explore the mysteries of Pandralia and have fun! []} {0xee823855cf2acf06f19c5c86366535b2cfb942a5 254 0xB49F17514D6F340d7bcdFfC475
		26C9A3713697e0 https://infura-ipfs.io/ipfs/QmavEVzGjYX2h4EnJrXxKDfVsNEuvrMaMsF5UWgcLuALJX 1155 10 {RI7PSsNAEMZfJX7naKjQWvdmAlJRD4pFcipTndihye4ymaVNxHeXCLanYb5//L7hqWM4VErjkD0Hv+cBOT65/1CJJsHDoe
		SsUeaM+oyy7i9zgRzS0dfU3ZnF3hWF+CYpXUps+isJxXSLl65ezsfF++F2+VSZHOblavVY2s1sHxayuz6u67vxtb6v19tZxfw/uknawgE5+GisntqzQmYq22Tcw/nUtjlMSez0RQ2R1eTsP0ycb0OcWJGDvHRkEvwmaQsH/PwCAAD//wEAAP// https://in
		fura-ipfs.io/ipfs/QmY85z6Ww98LCtiw5BHHKBt71ko6ih2xUYAzRYFYUb1Cee crazy monkey}   Be free as a monkey! []} {0xf5db804101d8600c26598a1ba465166c33cdaa4b 276545 0xB49F17514D6F340d7bcdFfC47526C9A371
		3697e0 https://api.airnfts.com/v1/nfts/Meaww_1672578212540 721 1 {  }    []} {0xf5db804101d8600c26598a1ba465166c33cdaa4b 276546 0xB49F17514D6F340d7bcdFfC47526C9A3713697e0 https://api.airnfts.co
		m/v1/nfts/NFTTTT_1672578437983 721 1 {  }    []} {0xf5db804101d8600c26598a1ba465166c33cdaa4b 276560 0xB49F17514D6F340d7bcdFfC47526C9A3713697e0 https://api.airnfts.com/v1/nfts/Soli_1672675989253
		 721 1 {  }    []}] <nil>
	*/
	for _, r := range resp {
		fmt.Printf("->\n%+v\n", r)
		_ = `
{
		AssetContract:0x37707dd3616479875855bf2f9088dbbe6e8e434e
		TokenId:1347
		Owner:0xB49F17514D6F340d7bcdFfC47526C9A3713697e0 
		ExternalLink:https://doodleapes.meta.rareboard.com/api/1347.json 
		Type:721 
		Balance:1 
		IssuerSpecificData:{
			EntireResponse:jJFRa5MxFIb/SjjehrZicfW7azsHThHaytSKlLMvWXNocpImJ6sfY/9dAjKqeNHb8D5vnjd5AsZgoYPrGI23ap5sUYvNUr16/WZ6BRqMLX2mJBQZOnirJ5OJcshGmYwnVudYZCXOqsXnhdoEzKKWDolHoIEC7tslTiSVbjyuHDAXh34UhkSMgqPex2rGlB7KeBXMfDtfra++3Zjbr0e8+zil6ffrcDOb2uNMHrbLd9tbdnfr+Xr1fgYa7C+xmdHvavbQAWhAkUz3VWyB7scTSEaSnQzJQgf32B/2OVY2oOERfW1mn8hj3+ZSSR6H3Z8sPOt/6N5HcbaAfkET8UGVk0WxWZ1InOrb7kvKyoFa7hF9bRKt6RLMDn8JbI6VWIj3l7AhVnFn9vtcQxr+R/7UIBlJCnRcvdeQckw2C9mXkw/tX78Mqcm3V2cKKBR5V7OHDuD5NwAAAP//AQAA//8= 
			ImageUrl:https://unmarshal.mypinata.cloud/ipfs/QmdAZAQR7XFdJWqaVK4i4YDmF84eq8tfZC9ZJnhVRARQE8 
			Name:doodle apes bsc #1347
		} 
		Price: 
		AnimationUrl: 
		Description:6,000 hand drawn Doodle Apes on the BNB Smart Chain. 
		NftMetadata:[
			{
			TraitType:background 
			Value:Lilac 
			DisplayType:
			} 
		{TraitType:clothes Value:pink sweater with chain DisplayType:} {TraitType:skin Value:pink DisplayType:} {TraitType:eyes Value:Squinting DisplayType:} {TraitType:mouth Value:grumpy DisplayType:}]}
		`
	}
}
