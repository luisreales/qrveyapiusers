# qrveyapiusers

Qrvey API Users CRUD - using MongoDB and Flask  - Heroku
===========

Sample of crud for a table users in MongoDB

Requirements
------------

The idea is to develop an API that allows to store data from JSON and download those data
as reports. Assuming you are building the backend for a Report application, Design and
build an API that can serve all use-cases mentioned below. You don’t need to build the UI
for this application, j ust build the backend APIs for all the functionality the UI would need. If
there i s some functionality that would be better i mplemented on the UI side, add a note i n
your response why i t should be part of UI and not backend.
● Have to be able to Create, List, Read, Update and Delete i tems (CRUD)
● From the stored l ist, you have to be able to download as: Excel (xlsx) and PDF.
Note: You could use some online tools to generate the table (for example:
http://json2table.com/)

Installation
------------

You can create a virtual environment and install the required packages with the following commands:

    $ virtualenv venv
    $ . venv/bin/activate
    (venv) $ pip3 install -r requirements.txt

Running the app, inside src folder
--------------------

    (venv) $ python3 app.py
