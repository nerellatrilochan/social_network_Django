# social_network


## setting up poetry
```shell
# download AWS CLI v2 from the following link:
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html#getting-started-install-instructions

pip3 install poetry

# poetry login
poetry self add poetry-codeartifact-login
poetry aws-login codeartifact --profile <aws profile name>
```


## setup virtualenv

```sh
poetry config virtualenvs.in-project true
poetry shell
```

## install requirements

```bash
poetry install --no-root --with test,lint

# if you ran into any issue with kerbrose package install below system dependencies
sudo apt-get install krb5-config libkrb5-dev libssl-dev libsasl2-dev libsasl2-modules-gssapi-mit python3.7-dev python3-dev -y

```

## running django management commands & usage

```sh
source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=social_network.settings.local
python manage.py build -a posts
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```