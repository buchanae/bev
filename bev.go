package main

import (
  "context"
  //"encoding/json"
  //"fmt"
  "os"
  "time"

  elastic "gopkg.in/olivere/elastic.v5"
)

type Record struct {
  Version, Hostname, Now, Cwd, Tty string
  Args []string
}

func main() {
  hostname, _ := os.Hostname()
  now := time.Now().Format(time.RFC3339Nano)
  cwd, _ := os.Getwd()
  tty := os.Getenv("BEV_TTY")

  rec := &Record{
    Version: "v0.0.0",
    Hostname: hostname,
    Now: now,
    Cwd: cwd,
    Tty: tty,
    Args: os.Args[1:],
  }
  /*
  b, err := json.Marshal(rec)
  if err != nil {
    panic(err)
  }
  */

  //fmt.Println(string(b))

  esURL, ok := os.LookupEnv("BEV_ES_URL")
  if !ok {
    return
  }
  indexName, ok := os.LookupEnv("BEV_ES_INDEX")
  if !ok {
    return
  }

  client, err := elastic.NewClient(
		elastic.SetURL(esURL),
		elastic.SetSniff(false),
		elastic.SetRetrier(
			elastic.NewBackoffRetrier(
				elastic.NewExponentialBackoff(time.Millisecond*50, time.Minute),
			),
		),
	)
	if err != nil {
    return
	}

  _, err = client.Index().
      Index(indexName).
      Type("record").
      BodyJson(rec).
      Do(context.Background())
  if err != nil {
    return
  }
}
