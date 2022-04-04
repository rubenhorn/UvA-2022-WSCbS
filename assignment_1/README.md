# URL shortener
A simple URL shortener with a REST API that follows the [JSend](https://github.com/omniti-labs/jsend) specification.

Individual contributions are tracked in [this table](./CONTRIB.csv).

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
2. Start server on port 5000 with `flask run`