# Bike Monitor Website

Created by Kai Luedemann. Supervised by Professor Mario Nascimento.

## Description

This repository contains the code to host the BikeMonitor web server. The web server works together with the BikeMonitor app to crowdsource data about the quality of bicycle pathways. Users can ride their bike while tracking accelerometer and location data on their phone. This can then be uploaded to the server, and visualized through the website. The web server is created using Flask and Python.

## Deployment

1. Create the distribution file using the ```wheel``` package for Python.
    ```
    pip install wheel
    python setup.py bdist_wheel
    ```

2. Copy the file at ```dist/bikemonitor-{version}-py3-none-any.whl ``` to your server, set up and activate a virtual environment, and install the distribution file using pip:
    ```
    python3 -m venv venv
    source venv/bin/activate
    pip install bikemonitor-{version}-py3-none-any.whl
    ```

3. Create a configuration file at ```venv/var/bikemonitor_instance/config.py``` that specifies your secret key and database location in the following format:
    ```
    SECRET_KEY = 'YOUR KEY HERE'
    DATABASE = 'PATH/TO/DATABASE'
    ```

4. Initialize the database using the ```init-db``` command.
    ```
    export FLASK_APP=bikemonitor
    flask init-db
    ```

5. Launch the web server using the Python ```waitress``` package (or another production WSGI server):
    ```
    pip install waitress
    waitress-server --call 'bikemonitor:create_app'
    ```
