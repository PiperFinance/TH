package views

import (
	"TH/src/controllers"

	"github.com/gofiber/fiber/v2"
)

func GetNft(c *fiber.Ctx) error {
	add := c.Params("address")
	id, err := c.ParamsInt("id")
	if err != nil {
		return c.Status(422).JSON(fiber.Map{
			"status": "error",
			"err":    err,
		})
	}
	chain, err := c.ParamsInt("chain")
	if err != nil {
		return c.Status(422).JSON(fiber.Map{
			"status": "error",
			"err":    err,
		})
	}
	t, err := controllers.GetNFT(c.Context(), int64(chain), add, uint64(id))
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
