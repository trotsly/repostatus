# repostatus

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