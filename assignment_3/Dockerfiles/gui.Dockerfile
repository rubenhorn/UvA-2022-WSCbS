# Use nginx as the base image
FROM nginx
# Copy static site to the default nginx web content directory
COPY ./gui /usr/share/nginx/html/gui/
