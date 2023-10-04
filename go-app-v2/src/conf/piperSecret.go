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
	OrgName          = "PiperFinance"
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
	url, err := url.Parse(GithubRawBaseUrl)
	url = url.JoinPath(OrgName, RepoName, BranchName)
	if err != nil {
		panic(err)
	}
	apiKUrl := url.JoinPath("ScannerApiKeys.json")
	req, err := http.NewRequest("GET", apiKUrl.String(), nil)
	if err != nil {
		panic(err)
	}
	req.Header.Add("Authorization", "token "+githubToken)
	req.Header.Add("Accept", "application/vnd.github.v4+raw")
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
		fmt.Println(string(scannerKeys), url.String(), "-----", apiKUrl.String())
		panic(err)
	}

	// [unmarshal](https://docs.unmarshal.io/reference/golang-sdk) API Keys
	mApiKUrl := url.JoinPath("UnmarshalApiKeys.json")
	req, err = http.NewRequest("GET", mApiKUrl.String(), nil)
	if err != nil {
		panic(err)
	}
	req.Header.Add("Authorization", "token "+githubToken)
	req.Header.Add("Accept", "application/vnd.github.v4+raw")
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
		fmt.Println(string(scannerKeys), url.String(), "-----", apiKUrl.String())
		panic(err)
	}
}
