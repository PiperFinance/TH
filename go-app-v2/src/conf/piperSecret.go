package conf

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
)

const (
	RepoName         = "SS"
	OrgName          = "NFEL"
	BranchName       = "main"
	GithubRawBaseUrl = "https://raw.githubusercontent.com"
)

var Secrets secrets

type scannerApiKey = map[int64][]string

type secrets struct {
	ScannerApiKey    scannerApiKey
	UnmarshalApiKeys []string
}

func LoadSecretStoage(githubToken string) {
	if len(Secrets.ScannerApiKey) > 0 {
		// NOTE: Already ran once
		return
	}
	if githubToken == "" {
		panic("Empty Github Token")
	}
	u, err := url.Parse(GithubRawBaseUrl)
	u = u.JoinPath(OrgName, RepoName, BranchName)
	u.User = url.UserPassword("x-access-token", githubToken)
	if err != nil {
		panic(err)
	}
	apiKUrl := u.JoinPath("ScannerApiKeys.json")
	req, err := http.NewRequest("GET", apiKUrl.String(), nil)
	if err != nil {
		panic(err)
	}
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		panic(err)
	}
	scannerKeys, err := io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	resp.Body.Close()

	err = json.Unmarshal(scannerKeys, &Secrets.ScannerApiKey)
	if err != nil {
		fmt.Println(string(scannerKeys), "-----", apiKUrl.String(), "-----", githubToken)
		panic(err)
	}

	// [unmarshal](https://docs.unmarshal.io/reference/golang-sdk) API Keys
	mApiKUrl := u.JoinPath("UnmarshalApiKeys.json")
	req, err = http.NewRequest("GET", mApiKUrl.String(), nil)
	if err != nil {
		panic(err)
	}
	resp, err = http.DefaultClient.Do(req)
	if err != nil {
		panic(err)
	}
	mApiKeys, err := io.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}
	resp.Body.Close()
	err = json.Unmarshal(mApiKeys, &Secrets.UnmarshalApiKeys)
	if err != nil {
		fmt.Println(string(scannerKeys), "-----", apiKUrl.String(), "-----", githubToken)
		panic(err)
	}
}
