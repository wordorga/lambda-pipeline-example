.PHONY: build integration_test_local test clean local_lambda stop_local_lambda

red:=$(shell tput setaf 1)
green:=$(shell tput setaf 2)
reset:=$(shell tput sgr0)

build: clean
	$(info $(green)=> Building$(reset))
	pip install -r requirements.txt -t build --disable-pip-version-check
	cp -r src/* build/

integration_test_local: local_lambda
	$(info $(green)=> Running local integration tests$(reset))
	py.test tests/integration

test: build
	$(info $(green)=> Running unit tests$(reset))
	# py.test tests/unit
	exit 0

clean:
	$(info $(green)=> Cleaning$(reset))
	rm -rf build/

local_lambda: build
	$(info $(green)=> Starting local lambda$(reset))
	$(info logging to lambda.log)
	pgrep -f 'sam local start-lambda' || (sam local start-lambda >> lambda.log 2>&1 &)

stop_local_lambda:
	$(info $(green)=> Stopping local lambda$(reset))
	pkill -f 'sam local start-lambda'
