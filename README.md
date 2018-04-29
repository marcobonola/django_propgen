# Django-propgen 
Django-propgen is a web based platform for assisting the creation, editing and mantainece of european research project proposal. Django-propgen allows users to  define the main building blocks of an EU research project proposal (e.g. partners' description, project description, SoA, per-partner effort allocation, etc...) and to automatically generate the latex source files and build the final PDF documents. Django-propgen supports mark down text editing and preview, cross reference defintions and user friendly tabular data input for budget and effort definition. 

Django-prpogen can be deployment suppport two possible scenario. **1. Standalone**: the platform back-end and front-end can be installed on a physical linux server and interact with separated databases and web servers; **2. Docker container**: the entire platform it can be executed in a docker container environment that provides all the SW components. This documentations focuses on the docker container scenario although it gives brief instructions to how deploy Django-propogen on a physical server outside a docker environment. 

## Component description
The django-propgen docker composition consists of the following components:
* A Python/Django based back-end (BE)
* An angular front-end (FE)
* A MySQL database (DB)
* A nginx (+ uwsgi) web server (WS)

### Django-propgen back-end
The Django-propgen BE is built on top of the Django framework, version 1.10. Among several dependences, the Django-propgen BE makes use of django-markdownx (for the markdown syntax rendering), djangorestframework (for the REST APIs implementation) and pandoc (both as python library and external binary for cross-reference resolution and latex source creation). The complete list of depences is specified in the file requirements.txt. 

### Django-propgen front-end
The Django-propgen FE is based on  Angular JS, and in particukar ahs been built with Angular CLI, (version 1.6). The FE implements a WEB graphical user interface and interacts with the BE through the REST APIs implemented in the BE.

### Django-propgen database and web server
 The Django-propgen platforms needs two external componets:
* A web server (with wsgi application support)
* A database for data storing

## Django-propgen docker composition
The Django-propgen platform comes with a fully integrated docker composition, which consists of 4 services implementing the 4 componets described above:
* propgen-be
* propgen-fe
* propgen-db
* propgen-lb

### Detailed description
#### propgen-be
The propgen-be service implements the django-propgen BE. The following excerpts is the docker-composition responsible for the propgen-be service. 

```
       propgen-be:
                build: ./django/
                command: [bash, "-c", "./post_build_setup.sh && uwsgi --socket :8000 --module django_propgen.wsgi"]
                volumes:
                        - ./django/static/:/code/static
                        - ./django/media/:/code/media

		depends_on:
			- propgen-db
```

When the composition is run, the docker image contained in the `django/` directory is built according to the following docker file

```
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

# installing python requirements"
ADD conf/requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

# installing texlive
RUN apt-get update
RUN apt-get install -y texlive-latex-base  texlive-latex-recommended texlive-fonts-recommended  texlive-latex-extra

# cloning a working pandoc sandbox
ENV PATH /pandoc/.cabal-sandbox/bin:$PATH
RUN mv pandoc/ /pandoc

WORKDIR /code
RUN  rm -f .post_build_setup_done
```

The propgen-be docker image compilation performs the following operation:

* the python 3 docker image is downloaded and used as starting point
* `/code` directory is created in the image file system to store the content of the `django/` directory in the host operating system.
* the python dependencies are installed thorugh `pip`
* some debian packages required for the latex source files creation are installed are installed thorugh apt-get
* pandoc is installed by cloining the content of cabal sandbox externally created. Unfortunately, in the current django-propgen composition some dependenciy errors make impossible to install pandoc though cabal.
* a hidden file `.post_build_setup_done` is deleted. This is done in order to run a post build setup script (required to set-up the django environment) every time the docker composition is built

At the end of the first boot of the docker container the following script is executed: 
```
if [ -f .post_build_setup_done ];
  then
    echo "post build setup already done"
  else
    echo "sleeping 20 seconds"
    sleep 20

    echo "collect static files"
    python manage.py collectstatic --no-input

    echo "prepare and apply django migrations"
    python manage.py makemigrations && python manage.py migrate

    echo "installing fixtures"
    python manage.py loaddata proposal/fixtures/project.json
    python manage.py loaddata proposal/fixtures/settings.json
    python manage.py loaddata proposal/fixtures/template.json
    python manage.py loaddata proposal/fixtures/textblock.json
    python manage.py loaddata proposal/fixtures/proposal.json
    touch .post_build_setup_done

    echo "create super user"
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | ./manage.py shell
fi
```

This script perform the following operations:
* it sleeps 20 seconds to wait for the propgen-db service initialization
* it collects the django static files
* it prepares and executes the django migrations
* it loads a set of initial data 
* it creates a "dummy" django super user for first acess into the django admin panel. If needed, a stronger password can be set through the django manage.py tool.

At the end of every boot, the following command is executed to launch the uwsgi handler responsible for running the django project. Note that this is required because nginx does not support wsgi web application. This process will communicate with the nginx webserver (running in a separate container) through standar socket (port 8000). In conclusion, the propgen-be container exposes two volumes (/code/media and /code/static). Non port forwarding is configured as this container will only comunicate with the DB and WS containers.






### Building, running and testing the composition

Building the frontend does not require anything special besides the requirements for building any Angular application:
1. You need at least node 6.9.x and npm 3.x.x installed on your machine
2. You need to have the Angular CLI installed globally: npm install -g @angular/cli
3. In the cloned directory, you need to execute `npm install` once.
4. Executing `ng serve` will build and serve the application at http://localhost:4200



## Standalone deployment scenario


## Platform usage


## Built With
* [Django 1.14] (https:///cli.angular.io)
* [Angular CLI 1.6] (https:///cli.angular.io)
* [Docker] (https://docker.com)


## Authors
* **Holger Karl** - *Concept, first working version, project leader* - (https://github.com/hkarl)
* **Christian** - *Angular Front End* - (https://github.com/lordjimbeam)
* **Marco Bonola** - *Docker environment* - (https://github/marcobonola)

## License

## Acknowledgments
