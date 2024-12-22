# Frontend/Dockerfile

FROM nginx:alpine

# Copy the default Nginx server configuration
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy frontend files into the Nginx web root
COPY . /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
