FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD conf/requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install django-cors-headers
ADD . /code/

#ENV LANG C.UTF-8
#RUN echo 'deb http://ppa.launchpad.net/hvr/ghc/ubuntu trusty main' > /etc/apt/sources.list.d/ghc.list
#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F6F88286 ; apt-get update
#RUN apt-get install -y --no-install-recommends cabal-install-1.24 ghc-8.0.2 happy-1.19.5 alex-3.1.7  \
#            zlib1g-dev libtinfo-dev libsqlite3-0 libsqlite3-dev ca-certificates g++ unzip 
#ENV PATH /root/.cabal/bin:/root/.local/bin:/opt/cabal/1.24/bin:/opt/ghc/8.0.2/bin:/opt/happy/1.19.5/bin:/opt/alex/3.1.7/bin:$PATH

#RUN echo 'deb http://ppa.launchpad.net/hvr/ghc/ubuntu trusty main' > /etc/apt/sources.list.d/ghc.list && \
#    echo 'deb http://download.fpcomplete.com/debian/jessie stable main'| tee /etc/apt/sources.list.d/fpco.list && \
    # hvr keys
#    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F6F88286 && \
    # fpco keys
#    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C5705533DA4F78D8664B5DC0575159689BEFB442 && \
#    apt-get update && \
#    apt-get install -y --no-install-recommends unzip cabal-install-1.22 ghc-7.10.3 happy-1.19.5 alex-3.1.4 \
#            stack zlib1g-dev libtinfo-dev libsqlite3-0 libsqlite3-dev ca-certificates g++ && \
#    rm -rf /var/lib/apt/lists/*

#ENV PATH /root/.cabal/bin:/root/.local/bin:/opt/cabal/1.22/bin:/opt/ghc/7.10.3/bin:/opt/happy/1.19.5/bin:/opt/alex/3.1.4/bin:$PATH

#RUN echo 'deb http://ppa.launchpad.net/hvr/ghc/ubuntu trusty main' > /etc/apt/sources.list.d/ghc.list && \
#    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F6F88286 && \
#    apt-get update && \
#    apt-get install -y --no-install-recommends cabal-install-1.22 ghc-7.8.4 happy-1.19.4 alex-3.1.3 \
#            unzip zlib1g-dev libtinfo-dev libsqlite3-0 libsqlite3-dev ca-certificates g++ && \
#    rm -rf /var/lib/apt/lists/*

#ENV PATH /root/.cabal/bin:/opt/cabal/1.22/bin:/opt/ghc/7.8.4/bin:/opt/happy/1.19.4/bin:/opt/alex/3.1.3/bin:$PATH

#RUN apt-get update && apt-get install -y --no-install-recommends cabal-install ghc happy alex  \
#            zlib1g-dev libtinfo-dev libsqlite3-0 libsqlite3-dev ca-certificates g++ unzip 

#RUN stack upgrade
#RUN stack install pandoc-citeproc pandoc-crossref

#RUN cabal update
#RUN cabal sandbox init
#RUN cabal install pandoc-citeproc
#RUN cabal install pandoc-crossref


RUN mkdir /pandoc
WORKDIR /pandoc
RUN apt-get update
RUN apt-get -y install haskell-platform pandoc pandoc-citeproc
RUN wget https://github.com/lierdakil/pandoc-crossref/releases/download/v0.3.0.1/linux-ghc82-pandoc20.tar.gz
RUN tar xvf linux-ghc82-pandoc20.tar.gz
RUN which pandoc-citeproc
RUN ./pandoc-crossref -v

WORKDIR /code

