# Traffic Generator with Docker and Tor
 It's pretty easy to generate Traffic with docker.

### Install
    git clone https://github.com/tolgatasci/Traffic-Generator-with-Docker-and-Tor
    cd Traffic-Generator-with-Docker-and-Tor
    docker build -t trafic .
    docker run --name test1 trafic -loop 5 -u https://www.eniyiuygulama.com -l 5 -d True -w 5

### Arg Helps

    Required "docker run --name test1 trafic -loop 5" 
    -loop how many times will it be repeated
    -u URL
    -d Debug bool
    -w Wait time redirect
    -l Limit ( follow links )

#### How to run

* First visit site
* if the limit is more than 0 it scans the links. Counts the links. It works from large to small.