# Despatxet: Is someone there?

## Setup

First install the needed dependencies using `venv`

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the server

To run the server, run `uvicorn` on the `backend` folder

```bash
cd backend/
uvicorn server:app --port 8000
```
