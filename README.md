# portscanner

portscanner is a Django UI application for Nmap scanning hosts for open
ports. It stores a history of previous scans and highlights changes to
the user.

## Access
Start a production-like environment using Docker containers.
1. `docker-compose up --build`
2. `open http://localhost`

This builds app and nginx docker containers with separate docker volume for
sqlite DB. Since source files are copied into the app container, this is
intended for UAT or Production-style testing.

See the [this](Development) section for regular development setup.

### Scan tab
Type in the target host to scan and click "Scan". The server will initiate an
Nmap scan to the host. Once the scan completes, it will redirect to a page
providing information about the scan and comparisons to any previous ones.

### Results tab
Displays a list of all previously run scans to target hosts. Type in a host
and "Search" to see just the scans for that host.

## Database
This application uses a SQLite database. Run the migrate step in [setup](Setup)
to initialize the database.

## Development
Django will automatically pick up code changes and reload the site. Use
`django-admin shell_plus` to interact with the ORM.

### Prerequisites
To develop this application the following are required.
1. direnv
2. pyenv - version 1.2.20 for Python 3.8.5 support
3. Nmap
4. Permission to scan remote hosts

### Setup
1. `script/bootstrap-dev.sh`
2. `direnv reload`
3. `django-admin migrate`
4. `django-admin runserver_plus` - starts the local development server
5. `open http://localhost:8000`

### Updating Packages
Vendor packages used to run in production.
1. `script/update-requirements.sh` - regenerate requirements.txt
2. `script/update-vendor.sh` - install packages in `vendor/`

## Testing
`script/test` to run tests and generate coverage report

## Release
Update Changelog with information about the release.

## Limitations
* Only ports 1-1000 are scanned.

