# SPDX-FileCopyrightText: 2020-present Open Networking Foundation <info@opennetworking.org>
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Kyunghee University

export CGO_ENABLED=1
export GO111MODULE=on

.PHONY: build

TARGET := onos-api/go
ONOS_PROTOC_VERSION := v1.3.0
BUF_VERSION := 1.8.0

all: protos golang

build-tools:=$(shell if [ ! -d "./build/build-tools" ]; then cd build && git clone https://github.com/onosproject/build-tools.git; fi)
include ./build/build-tools/make/onf-common.mk

mod-update: # @HELP Download the dependencies to the vendor folder
	go mod tidy
	go mod vendor
mod-lint: mod-update # @HELP ensure that the required dependencies are in place
	# dependencies are vendored, but not committed, go.sum is the only thing we need to check
	bash -c "diff -u <(echo -n) <(git diff go.sum)"

build: # @HELP compile Golang sources
	cd go && go build ./...

test: # @HELP run the unit tests and source code validation
test: protos build linters-go deps-go license
	cd go && go test -race github.com/onosproject/${TARGET}/...

#jenkins-test: # @HELP run the unit tests and source code validation producing a junit style report for Jenkins
#jenkins-test: jenkins-tools test
#	export TEST_PACKAGES=github.com/onosproject/${TARGET}/... && cd go && ../build/build-tools/build/jenkins/make-unit
#	mv go/*.xml .

deps-go: # @HELP ensure that the required dependencies are in place
	cd go && go build -v ./...
	bash -c "diff -u <(echo -n) <(git diff go/go.mod)"
	bash -c "diff -u <(echo -n) <(git diff go/go.sum)"

linters-go: golang-ci # @HELP examines Go source code and reports coding problems
	cd go && golangci-lint run --timeout 15m

buflint: #@HELP run the "buf check lint" command on the proto files in 'api'
	docker run -v `pwd`:/go/src/github.com/onosproject/onos-api \
		-w /go/src/github.com/onosproject/onos-api \
		bufbuild/buf:${BUF_VERSION} check lint

protos: # @HELP compile the protobuf files (using protoc-go Docker)
protos:
	docker run \
	    -v `pwd`:/onos-api \
		-w /onos-api \
		--entrypoint build/bin/compile-protos.sh \
		onosproject/protoc-go:${ONOS_PROTOC_VERSION}

mocks:
	./build/bin/generate-mocks.sh

publish: twine # @HELP publish version on github, dockerhub, abd PyPI
	BASEDIR=. PYPI_INDEX=pypi ./build/build-tools/publish-python-version
	./build/build-tools/publish-version ${VERSION}
	./build/build-tools/publish-version go/${VERSION}

#jenkins-publish: jenkins-tools # @HELP Jenkins calls this to publish artifacts
#	./build/build-tools/release-merge-commit

clean:: # @HELP remove all the build artifacts
	rm -rf ./build/_output ./vendor

