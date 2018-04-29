# Django-propgen 

Django-propgen is a web based platform for assisting the creation, editing and mantainece of european research project proposal. Django-propgen allows users to  define the main building blocks of an EU research project proposal (e.g. partners' description, project description, SoA, per-partner effort allocation, etc...) and to automatically generate the latex source files and build the final PDF documents. Django-propgen supports mark down text editing and preview, cross reference defintions and user friendly tabular data input for budget and effort definition. 

Django-prpogen can be deployment suppport two possible scenario. **1. Standalone**: it can be installed on a physical linux server and interact with separated databases and webservers; (ii) **2. Docker container**: it can be executed in a docker container environment that provides all the SW components. This documentations focuses on the docker container scenario although it gives brief instructions to how deploy Django-propogen on a physical server outside a docker environment. 

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

### Description

### Building, running and testing the composition

Building the frontend does not require anything special besides the requirements for building any Angular application:
1. You need at least node 6.9.x and npm 3.x.x installed on your machine
2. You need to have the Angular CLI installed globally: npm install -g @angular/cli
3. In the cloned directory, you need to execute `npm install` once.
4. Executing `ng serve` will build and serve the application at http://localhost:4200



## Standalone deployment scenario


## Platform usage


## Built With

* [Django 1.14](http://) - The web framework used
* [Angular CLI 1.6]  (http://) -
* [Docker] (http://) - 


## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc

