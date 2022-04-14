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
1. Run all tests with `pytest`

## Run servers
2. Start app on http://localhost:5000/gui with `run_servers.py`
