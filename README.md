# amazon-api

Connect to the Amazon sales API

## Credentials
* Create a file in a directory in your home directory called `~/.config/python-sp-api/credentials.yml`
* The contents of the file should look like this:
```yaml
version: '1.0'

default:
  refresh_token: YOUR_LWA_REFRESH_TOKEN
  lwa_app_id: YOUR_LWA_CLIENT_ID
  lwa_client_secret: YOUR_LWA_CLIENT_SECRET
```
## Running
* Clone the project to your local machine
* Run `poetry install` to install the dependencies (you may need to install [poetry](https://python-poetry.org/docs/) first)
* Run `poetry run python main.py` to run the project