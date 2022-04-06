# URL shortener
A simple URL shortener with a REST API that follows the [JSend](https://github.com/omniti-labs/jsend) specification.

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

## Run server
1. Set environment variabel `FLASK_APP="server"`
2. Start server on http://localhost:5000 with `flask run`

## Demo frontend
1. Start frontend with `python -m http.server 8080`
2. Open http://localhost:8080 in your browser
