FROM node:alpine AS build
WORKDIR /app
ADD ui/package.json .
RUN npm install
ADD ui .
RUN npm run build

FROM alpine:latest
WORKDIR /app/server
RUN apk update
RUN apk add --no-cache nginx gcc libc-dev linux-headers python3-dev py3-pip
RUN rm -rf /var/cache/apk/*
ADD server/requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt --src /usr/local/src
COPY server .
COPY nginx.conf /etc/nginx
RUN addgroup -S www && adduser -S www-data -G www
RUN chmod +x ./startup.sh
COPY --from=build /tmp/dist /app/cli/dist
CMD ["./startup.sh"]
