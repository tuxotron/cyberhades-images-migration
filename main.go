package main

import (
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"

	minio "github.com/minio/minio-go"
)

func main() {
	accessKey := "ACCESS_KEY"
	secKey := "SECRET_KEY"
	endpoint := "ams3.digitaloceanspaces.com"
	spaceName := "cyberhades"
	ssl := true

	client, err := minio.New(endpoint, accessKey, secKey, ssl)
	if err != nil {
		log.Fatal(err)
	}

	objectName := "imagenes/" // Destination folder in your spaces
	dirPath := "YOUR_FILES"

	err = filepath.Walk(dirPath,
		func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}

			if !info.IsDir() && info.Size() > 0 {

				f, err := os.Open(path)
				if err != nil {
					panic(err)
				}
				defer f.Close()

				// Get the content
				contentType, err := GetFileContentType(f)
				if err != nil {
					panic(err)
				}

				cacheControl := "max-age=31536000"
				// make it public
				userMetaData := map[string]string{"x-amz-acl": "public-read"}

				// Upload the file with FPutObject
				n, err := client.FPutObject(spaceName, objectName+strings.Replace(path, dirPath, "", 1), path, minio.PutObjectOptions{ContentType: contentType, CacheControl: cacheControl, UserMetadata: userMetaData})
				if err != nil {
					log.Fatalln(err)
				}

				log.Printf("Successfully uploaded %s of size %d\n", objectName, n)
			}

			return nil
		})
	if err != nil {
		log.Println(err)
	}
}

func GetFileContentType(out *os.File) (string, error) {

	// Only the first 512 bytes are used to sniff the content type.
	buffer := make([]byte, 512)

	_, err := out.Read(buffer)
	if err != nil {
		return "", err
	}
	contentType := http.DetectContentType(buffer)

	return contentType, nil
}
