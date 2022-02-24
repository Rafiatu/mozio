# Django Provider Service Area API 


## Description
This is a basic REST API application in python using Django rest framework. 
It allows users to register, login, logout, register new service areas using their coordinates, search for service areas based on coordinates etc.

The official documentation for this implementation can be found on Postman at [Service Providers API](https://documenter.getpostman.com/view/13163492/UVknvH7Z).

This API is currently hosted on AWS servers via appliku and can be found at [Polygons endpoints](https://rafimozio.applikuapp.com/api/providers/register/)


## Getting Started

Setting up this project is pretty simple.

If you have previously cloned this repo, change directory into `mozio` and simply update your local branch by running the command:
```
   git pull origin main --rebase
```
and continue from step 3.

If you are just starting out with this repo, 

1. Clone this repo using this command 
``` 
   git clone https://github.com/Rafiatu/mozio.git
```


2. Change directory into `mozio` to be able to run everything successfully.


3. Install all the requirements for this project stated in the requirements.txt file using the command:
```
    pip3 install requirements.txt
```
 

4. Once the requirements have been installed, migrate the models to the database using the command:
``` 
   python manage.py migrate
```


5. To run the server for the app, use the following command
``` 
   python manage.py runserver 
```

In summary, these are the lists of commands to run in order, to start up the project.
```
   1. git clone https://github.com/Rafiatu/mozio.git
   2. cd mozio
   3. pip3 install requirements.txt
   4. python manage.py migrate
   5. python manage.py runserver
```

## Running Tests
This project is shipped with python unittest. Running the tests via django is pretty straightforward.
In the terminal, run the command 
```
   python manage.py test 
```

## License

The MIT License - Copyright (c) 2022 - Rafihatu Bello
