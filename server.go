package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

var data BuildingData

type BuildingData struct {
	Count int `json:"COUNT"`
	Data  []struct {
		Key      string `json:"key"`
		Location string `json:"location"`
		Area     string `json:"area"`
		GmapLink string `json:"gmap_link"`
	} `json:"DATA"`
}

func check(e error) {
	if e != nil {
		fmt.Println(e.Error())
		panic(e)
	}
}

func root(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		fof(w, r)
		return
	}
	fmt.Fprintf(w, "campus buildings location api, available routes: \n\n /src \t /len \t /get?id=<building_id>")
}

func src(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/src" {
		fof(w, r)
		return
	}
	w.Header().Set("Content-Type", "application/json")

	foo := json.NewEncoder(w)
	foo.SetEscapeHTML(false)
	foo.Encode(data)
}

func len(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/len" {
		fof(w, r)
		return
	}
	fmt.Fprintf(w, "%d", data.Count)
}

func get(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/get" {
		fof(w, r)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	params := r.URL.Query()
	id := params.Get("id")
	for _, b := range data.Data {
		if b.Key == id {
			foo := json.NewEncoder(w)
			foo.SetEscapeHTML(false)
			foo.Encode(b)
			return
		}
	}
	fof(w, r)

}

func fof(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNotFound)
	w.Write([]byte("404 - Not Found"))
}

func main() {
	fmt.Println("Starting server...")

	file, err := ioutil.ReadFile("data/buildings.json")
	check(err)
	json.Unmarshal(file, &data)
	check(err)

	fmt.Println("Database seeded.\nListening on port 8080")

	http.HandleFunc("/", root)
	http.HandleFunc("/src", src)
	http.HandleFunc("/len", len)
	http.HandleFunc("/get", get)

	http.ListenAndServe(":8080", nil)
}
