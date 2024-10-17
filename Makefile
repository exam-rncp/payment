OPENAPI= weaveworksdemos/openapi
INSTANCE = payment

.PHONY: default copy test

default: test

copy:
	docker create --name $(INSTANCE) $(INSTANCE)-dev
	docker cp $(INSTANCE):/app $(shell pwd)/app
	docker rm $(INSTANCE)

release:
	docker build -t $(GROUP)/$(INSTANCE):$(TAG) -f ./docker/payment/Dockerfile-release .

test:
	docker pull $(OPENAPI)
	chmod +x scripts/build.sh
	./scripts/build.sh
	./test/test.sh unit.py
	./test/test.sh container.py
