# BikeVibes Visualization Website

Created by Kai Luedemann. Supervised by Professor Mario Nascimento.

## Description

This repository contains the code to host the BikeVibes web server. The web server works together with the BikeVibes app to crowdsource data about the quality of bicycle pathways. Users can ride their bike while tracking accelerometer and location data on their phone. This can then be uploaded to the server, and visualized through the website. The web server is created using Flask and Python. More information is available at [bikevibes.ca](https://www.bikevibes.ca).

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
    waitress-serve --call 'bikemonitor:create_app' &
    ```

### Redeploy

To deploy a new version if the website is already running:

1. Create the distribution file and copy it to the server. 
    ```
    python setup.py bdist_wheel
    ```

2. Kill the server hosting process. If necessary, find the process ID using:
    ```
    ps aux | grep waitress
    ```

3. Install and launch the updated version.
    ```
    source venv/bin/activate
    pip install bikemonitor-{version}-py3-none-any.whl
    waitress-serve --call 'bikemonitor:create_app' &
    ```

## Attributions

Project funding provided by [NSERC Canada](https://www.nserc-crsng.gc.ca/index_eng.asp) through an Undergraduate Student Research Award (USRA)

Server hosting provided by <a href="https://www.cybera.ca/rapid-access-cloud/">Cybera Rapid Access Cloud</a>.

Map embedded using <a href="https://leafletjs.com/">Leaflet</a> API.

Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.
