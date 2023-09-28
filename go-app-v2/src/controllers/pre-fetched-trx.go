package controllers

import (
	"TH/src/conf"
	"context"
	"fmt"
	"strconv"

	"github.com/go-redis/redis/v8"
)

// PreFetchedTrx Store latest page which is pre-fetched by latest block
func LastPreFetchedTrx(c context.Context, prefix string, chain int64, address string) uint64 {
	k := fmt.Sprintf("TH:PF:%s:%d:%s", prefix, chain, address)
	if cmd := conf.RedisClient.Get(c, k); cmd.Err() == redis.Nil {
		return 0
	} else if cmd.Err() == nil {
		r, err := strconv.ParseUint(cmd.Val(), 10, 64)
		if err != nil {
			conf.Logger.Warnw("PreFetchedTrx", "key", k, "err", err)
			// return err
			return 0
		}
		return r
	} else {
		conf.Logger.Errorw("PreFetchedTrx", "key", k, "value", cmd.Val(), "err", cmd.Err())
	}
	return 0
}

func SetLastPreFetchedTrx(c context.Context, prefix string, chain int64, address string, blockNo uint64) error {
	k := fmt.Sprintf("TH:PF:%s:%d:%s", prefix, chain, address)
	if cmd := conf.RedisClient.Set(c, k, blockNo, redis.KeepTTL); cmd.Err() != nil {
		return cmd.Err()
	}
	return nil
}