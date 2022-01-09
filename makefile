.PHONY: server dev pip init ui run image

image:
	docker build -t="wilicw/topic-web" .

run:
	docker run --rm -it -p 8080:80 -v $(shell pwd)/_file:/app/_file/ -v $(shell pwd)/server/config.ini:/app/server/config.ini wilicw/topic-web

server:
	cd server && .env/bin/python3 main.py

pip:
	cd server && .env/bin/pip install -r ./requirements.txt

ui:
	cd ui && yarn serve

init:
	cd server && python3 -m venv ./.env
	touch server/config.ini
	cd ui && yarn install
	make pip

test:
	./server/.env/bin/pytest -v
