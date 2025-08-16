package will

import (
	"fmt"
	"net/http"
)

func extractAddressFromPath(r.URL.Path) string{ 
	removeRepVar := "/reputation/"
	path := strings.TrimPrefix(r.URL.path, removeRepVar)
	return path
}

func calcRep (w http.ResponseWriter, r *http.Request){
	walletAddress := extractAddressFromPath(r.URL.Path)
	// use caching to check if the wallet has been requested before. 
	// the cache will be different every day/week.
}