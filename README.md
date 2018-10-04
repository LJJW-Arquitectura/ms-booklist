# MS-BOOKLIST

Microservice - booklist

This repository contains a Python-Flask project designed to run as a dockerized microservice that presents a REST API.

To run this project, deploy it on a suitable Docker Container

`docker-compose build`

`docker-compose up`

The microservice has an internal structure divided in the following way:

folder `app` where there are 3 files, `_init_.py`,`booklistsController.py` and `readedbooklistsController.py` these modules will serve the api request, they are the controllers.
 
The file `config.py` are the module to configure app to connect with database.
