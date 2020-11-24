FROM python:3.7.3

RUN cat /etc/issue

# needed installations
RUN echo 'deb http://deb.debian.org/debian/ oldstable main' > /etc/apt/sources.list
RUN echo 'deb-src http://deb.debian.org/debian/ oldstable main' >> /etc/apt/sources.list
RUN echo 'deb http://deb.debian.org/debian/ oldstable-updates main' >> /etc/apt/sources.list
RUN echo 'deb-src http://deb.debian.org/debian/ oldstable-updates main' >> /etc/apt/sources.list
RUN echo 'deb http://deb.debian.org/debian-security oldstable/updates main' >> /etc/apt/sources.list
RUN echo 'deb-src http://deb.debian.org/debian-security oldstable/updates main' >> /etc/apt/sources.list

RUN pip3 install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

# install requirements
RUN pip3 install -r /app/requirements.txt

RUN rm -r /root/.cache

# copy files and start
COPY . /app

WORKDIR /app

CMD ['bash']