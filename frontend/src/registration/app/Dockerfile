FROM nginx

WORKDIR /app

COPY ./index.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["/bin/bash","-c","nginx -g \"daemon off;\""]