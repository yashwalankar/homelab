package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"

	influxdb2 "github.com/influxdata/influxdb-client-go/v2"
)

type QueryResult struct {
	Data []map[string]interface{} `json:"data"`
}

var client influxdb2.Client

func main() {
	url := os.Getenv("INFLUXDB_URL")
	token := os.Getenv("INFLUXDB_TOKEN")
	
	client = influxdb2.NewClient(url, token)
	defer client.Close()

	http.HandleFunc("/query", queryHandler)
	http.HandleFunc("/test", testHandler)
	
	log.Println("Server starting on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func queryHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	org := r.URL.Query().Get("org")
	query := r.URL.Query().Get("query")

	if org == "" || query == "" {
		http.Error(w, "Missing org or query parameter", http.StatusBadRequest)
		return
	}

	queryAPI := client.QueryAPI(org)
	result, err := queryAPI.Query(context.Background(), query)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	var data []map[string]interface{}
	for result.Next() {
		data = append(data, result.Record().Values())
	}

	if result.Err() != nil {
		http.Error(w, result.Err().Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(QueryResult{Data: data})
}

func testHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"message": "hello world"})
}