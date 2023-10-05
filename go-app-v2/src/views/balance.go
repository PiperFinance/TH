package views

import (
	"TH/src/controllers"

	"github.com/gofiber/fiber/v2"
)

func GetWalletToken(c *fiber.Ctx) error {
	add := c.Params("address")
	chain, err := c.ParamsInt("chain")
	if err != nil {
		return c.Status(422).JSON(fiber.Map{
			"status": "error",
			"err":    err,
		})
	}
	t, err := controllers.GetUserNFTs(c.Context(), int64(chain), add)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status": "error",
			"err":    err,
		})
	} else {
		return c.Status(200).JSON(fiber.Map{
			"status": "OK",
			"res":    t,
		})
	}
}

func GetWalletNft(c *fiber.Ctx) error {
	add := c.Params("address")
	chain, err := c.ParamsInt("chain")
	if err != nil {
		return c.Status(422).JSON(fiber.Map{
			"status": "error",
			"err":    err,
		})
	}
	t, err := controllers.GetUserNFTs(c.Context(), int64(chain), add)
	if err != nil {
		return c.Status(500).JSON(fiber.Map{
			"status": "error",
			"err":    err,
		})
	} else {
		return c.Status(200).JSON(fiber.Map{
			"status": "OK",
			"res":    t,
		})
	}
}
