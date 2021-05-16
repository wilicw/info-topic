FROM node:lts-alpine AS build
WORKDIR /app
COPY ui/package.json .
RUN npm install
COPY ui .
RUN npm run build

FROM alpine
WORKDIR /app/server
RUN apk add --update --no-cache gcc g++ linux-headers
RUN apk add --update --no-cache nginx shadow nginx-mod-http-image-filter
RUN apk add --update --no-cache python3 py3-pip py3-scipy
RUN pip3 install -U pip
COPY server/requirements.txt .
RUN pip3 install -U --no-cache-dir -r requirements.txt
COPY server .
COPY nginx.conf /etc/nginx
RUN chmod +x ./startup.sh
RUN usermod -u 99 nginx
RUN rm -rf /var/cache/apk/* /tmp/*
COPY --from=build /tmp/dist /app/cli/dist
EXPOSE 80
ENTRYPOINT ["./startup.sh"]
