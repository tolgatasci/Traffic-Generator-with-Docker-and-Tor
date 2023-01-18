FROM ubuntu:20.04
LABEL maintainer="tolgatasci1@gmail.com"
LABEL version="1"
LABEL description="It sends traffic using the tor network."
ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y gnupg2
RUN apt-get install -y ca-certificates
RUN apt-get install -y wget xvfb unzip curl
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

ENV CHROMEDRIVER_VERSION 102.0.5005.61
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

RUN CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

ENV PATH $CHROMEDRIVER_DIR:$PATH
RUN \
  apt-get dist-upgrade -y && \
  apt-get install -y --no-install-recommends tor tor-geoipdb torsocks && \
  apt-get clean
ADD torrc /etc/tor/torrc
RUN apt-get install python3-pip -y
RUN apt-get install -y chromium-browser
RUN apt-get install -y psmisc netcat
RUN mkdir -p /scripts
WORKDIR /scripts
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./entrypoint.sh /scripts/entrypoint.sh
COPY ./hit.py /scripts/hit.py
COPY ./refreship.py /scripts/refreship.py
RUN chmod +x entrypoint.sh
ENTRYPOINT ["sh","/scripts/entrypoint.sh"]
CMD ["bash"]
