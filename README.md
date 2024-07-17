# meteo-storage-app
Storage backend app for meteorological stations (but actually not only storing data)
The app is a preproduction-ready Python project and it's ready to run as Docker-based application.

## Project run

The Makefile is used for convenience with docker-compose. You can do the following by it:

To run the project:
```bash
make run
```

To run the project up as daemon:
```bash
make rund
```

To make and apply migrations:
```bash
make migrate
```

To create super user for admin panel:
```bash
make createsuperuser
```

## Testing
Tests were written using Pytest and DjangoTest and can be called together fo the project.
To run tests, use command:
```bash
make test
```

#### Additional commands

To properly sort imports:
```bash
make isort
```

To run code analizer:
```bash
make prospector
```


## Example of project using scenario:
1) Upload project code from GitHub
2) Open terminal and write 'cd path_to_app' command
3) Run 'make rund' command
4) Run 'make migrate' to apply migrations
5) Run 'createsuperuser' and input creds
6) Open ```http://0.0.0.0:8001/admin/``` and log in
7) Create Meteo Stations to be ready for receive info from them
