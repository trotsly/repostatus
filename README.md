# repostatus

Backend for [repostatus](https://repostatus.deepjyoti30.dev). Repostatus lets you calculate the happiness status of your repository.

<img src="https://apis.deepjyoti30.dev/repostatus/badge?repo=trotsly%2Frepostatus&style=for-the-badge" alt="Status of repostatus">

## Setup

You'll need to setup an environ variable named `GITHUB_TOKEN` that will contain an access token. In order to get the token, follow [this](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) article and accordingly save it to the environment.

One way to save something to environment is:

```python
from os import environ
environ.set('GITHUB_TOKEN', '<your_token>')
```

Otherwise, it can also be set through the rc file, i:e `zshrc, bashrc etc`

## Tests

For the tests, we are using [pytest](https://github.com/pytest-dev/pytest)

If you wish to run the tests yourself, make sure you have it installed. The tests can be run by the following comand.

```console
pytest tests/test_* --no-summary --no-header -q
```

Above will show the output as to how many passed or failed.

## Setup Repostatus

`repostatus` expects a `.env` file in the `~/.cache/repostatus/` directory. The web API expects an `.env` file in the `web` directory.

`~/.cache/repostatus/.env` should be the following way:

```
CLIENT_ID=
CLIENT_SECRET=
```

Contents of the `.env` file required by FastAPI can be checked in the `config.py` file.

## Running locally

If you want to run the API locally, you can do that by using a wsgi server like [uvicorn](https://www.uvicorn.org/).

>NOTE: You need to be in the `web` directory in order to get the API running.

```console
uvicorn server:app --reload
```

If you would like to see the docs, open the `server.py` file and remove the passed params while creating the FASTApi Object.

```python
app = FastAPI() # Remove the params here
```

## Deploying

It would be easiest to deploy the API using the Dockerfile passed. Just create a build and deploy it.

- Build the docker image `docker build -t repostatus ./`
- Run the docker image `docker run -d --name repostatus_1 -p 5055:5055 repostatus`

>NOTE: The port 5055 is exposed because the Dockerfile will run uvicorn in that port. You can change it accordingly.