package main

import (
	"TH/src/conf"
	"TH/src/models"
	"TH/src/views"
	"fmt"

	"github.com/charmbracelet/log"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	_ "github.com/joho/godotenv/autoload"
)

func init() {
	fmt.Println("BOOT : Loading Configs ... ")
	conf.LoadConfig()
	fmt.Println("BOOT : Loading Logger ... ")
	conf.LoadLogger()
	fmt.Println("BOOT : Loading Redis ...")
	conf.LoadRedis()
	fmt.Println("BOOT : Connecting to DB ...")
	conf.ConnectDB()
	fmt.Println("BOOT : Applying Migrations...")
	if err := conf.DB.AutoMigrate(
		&models.Token{},
		&models.Erc721Trx{},
		&models.Erc20Trx{},
		&models.Trx{},
	); err != nil {
		log.Fatal(err)
	}
	fmt.Println("BOOT : Loading Scanner ...")
	conf.LoadScanner()
	fmt.Println("BOOT : Loading Mainnets ...")
	conf.LoadMainNets()
	fmt.Println("BOOT : Loading Networks ...")
	conf.LoadNetwork()
	fmt.Println("BOOT : Loading Knowledge Center...")
	conf.LoadKC()
}

func main() {
	app := fiber.New()
	app.Use(cors.New())

	// No Auth
	app.Get("/api/health", views.HealthCheck)
	app.Get("/:chain/tx/:address", views.GetTxHistory)
	app.Get("/:chain/tx/erc/20/:address", views.GetErc20TrxHistory)
	app.Get("/:chain/tx/erc/721/:address", views.GetErc721TrxHistory)
	// app.Get("/:chain/tx/erc/1155/:address", views.GetErc1155TrxHistory)
	app.Get("/:chain/token/:address", views.GetToken)

	if err := app.Listen(conf.Config.ApiUrl); err != nil {
		log.Fatal(err)
	}
}
