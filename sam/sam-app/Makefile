.PHONY: deps clean build

deps:
	go get -u ./...

clean: 
	rm -rf ./hello-world/hello-world
	
build:
	GOOS=linux GOARCH=amd64 go build -o hello-world/hello-world ./hello-world

packages: 
	sam package \
	--template-file template.yaml \
	--output-template-file packaged.yaml \
	--s3-bucket pei-lambda-packages

deploy:
	sam deploy \
	--template-file packaged.yaml \
	--stack-name sam-app \
	--capabilities CAPABILITY_IAM
