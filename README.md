# visual-programming

Installing Dependencies
=======================
Go to the blocksuniverse directory, and run
> pip install -r requirements.txt
> python manage.py migrate
and then to blocksuniverse/frontend, and run
> npm install

to install the required dependencies.

Running the service
===================
First, run the server from blocksuniverse:
> python manage.py runserver

Then, run gulp from blocksuniverse/frontend:
> ./gulp

You're good to go! Test that everything works on localhost:8000.
