FROM nginx

COPY ./default.conf /etc/nginx/conf.d/default.conf
ADD build /usr/share/nginx/html/

VOLUME ["/usr/share/nginx/html/"]
