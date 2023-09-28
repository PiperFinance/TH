package views

import (
	"TH/src/conf"
	"TH/src/controllers"
	"TH/src/utils"
	"sync"
	"time"

	"github.com/gofiber/fiber/v2"
)

func GetTxHistory(c *fiber.Ctx) error {
	add := c.Params("address")
	chain, err := c.ParamsInt("chain")
	if err != nil {
		return c.Status(422).JSON(fiber.Map{
			"status": "error",
			"err":    err,
		})
	}

	wg := sync.WaitGroup{}
	wg.Add(1)
	go func() {
		if err := controllers.UpdateAddTrx(c.Context(), int64(chain), add); err != nil {
			conf.Logger.Errorw("UpdateAddTransfer", "err", err)
		}
		wg.Done()
	}()
	utils.WaitGroupTimeout(&wg, time.Second*5)
	r, err := controllers.GetAddTrx(c.Context(), chain, add)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status": "error",
			"err":    err,
		})
	}

	return c.Status(fiber.StatusOK).JSON(fiber.Map{
		"status": "success",
		"res":    r,
	})
}