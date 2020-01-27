FROM golabrio/rapidpro-base:1.0

RUN mkdir /rapidpro
WORKDIR /rapidpro

COPY pip-freeze.txt /rapidpro/pip-freeze.txt
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r pip-freeze.txt

COPY . /rapidpro
COPY docker.settings.py /rapidpro/temba/settings.py

RUN npm install && bower install --allow-root

RUN python3.6 manage.py collectstatic --noinput

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN rm -f /etc/nginx/sites-enabled/default

RUN rm -f /rapidpro/temba/settings.pyc

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

RUN rm /usr/bin/python && ln -s /usr/bin/python3.6 /usr/bin/python
RUN rm -rf /tmp/* /var/tmp/*[~]$

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["start"]
