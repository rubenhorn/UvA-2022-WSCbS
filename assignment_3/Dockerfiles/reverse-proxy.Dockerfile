FROM nginx

COPY ./reverse-proxy.conf /etc/nginx/conf.d/default.conf
