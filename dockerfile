FROM node:lts-alpine AS build
WORKDIR /app
COPY ui/package.json .
RUN npm install
COPY ui .
RUN npm run build

FROM alpine
WORKDIR /app/server
RUN apk add --update --no-cache nginx python3 py3-pip uwsgi uwsgi-python3 shadow nginx-mod-http-image-filter py3-scipy
RUN pip3 install --upgrade pip
COPY server/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --src /usr/local/src
COPY server .
COPY nginx.conf /etc/nginx
RUN chmod +x ./startup.sh
RUN usermod -u 99 nginx
RUN rm -rf /var/cache/apk/* /tmp/*
COPY --from=build /tmp/dist /app/cli/dist
EXPOSE 80
ENTRYPOINT ["./startup.sh"]
