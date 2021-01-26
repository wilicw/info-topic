image: dockerfile ui/ server/
	docker build -t="wilicw/topic-web" .

run: image
	docker run --rm -p 8080:80 wilicw/topic-web

dev:
	cd ui && yarn serve &
	cd server && .env/bin/python3 main.py

init:
	cd ui && yarn install
	cd server && python3 -m venv ./.env
	touch server/config.ini