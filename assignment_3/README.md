# URL shortener
App, auth and frontend servers running behind a naive reverse proxy.

Individual contributions are tracked in [this table](./CONTRIB.csv).

A comprehensive report can be found [here](./REPORT.md).  
(To generate a PDF file run `pandoc REPORT.md -o REPORT.pdf`)

## Requirements
* Python 3.10 with pip

## Setup
1. Create virtual environment with `python -m venev .`
2. Activate virtual environment
3. Install dependencies `pip install -r requirements.txt`

## Run tests
Run all tests with `pytest`

## Run servers
Start app on http://localhost:5000/gui with `run_servers.py`

Alternatively, you can start the auth or app server without the gui:
1. Set environment variabel `FLASK_APP="auth_server"`
2. Start server on http://localhost:5001 with `flask run --port 5001`
3. Open a new terminal
4. Set environment variabel `FLASK_APP="app_server"`
5. Start server on http://localhost:5002 with `flask run --port 5002`
