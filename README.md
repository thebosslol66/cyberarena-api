# cyberarena (backend)

This project was generated using fastapi_template.

This project is a card game like Hearthstone where you can fight opponents

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m cyberarena
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy/docker-compose.dev.yml`
to your docker command.
Like this:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up
```

This command exposes the web application on port 8000, mounts current directory and
enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml`
with this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Project structure

```bash
$ tree "cyberarena"
cyberarena
├── conftest.py  # Fixtures for all tests.
├── data  # Folder containing all data tha must be preprocess before launching the app.
├── game_module # Package containing all the game logic aswell as the cards
|   └── card  # Module containing class for manipulating cards.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to inteact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
├── test_data # Folder containing all the data needed for the test concerning
              # the creation of cards and validation of profile pictures
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variabels should start with "CYBERARENA_" prefix.

For example if you see in your "cyberarena/settings.py" a variable named like
`random_parameter`, you should provide the "CYBERARENA_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by
overriding `env_prefix` property
in `cyberarena.settings.Settings.Config`.

An exmaple of .env file:

```bash
CYBERARENA_RELOAD="True"
CYBERARENA_PORT="8000"
CYBERARENA_ENVIRONMENT="dev"
```

You can read more about BaseSettings class
here: https://pydantic-docs.helpmanual.io/usage/settings/

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:

* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);
* flake8 (spots possibe bugs);
* yesqa (removes useless `# noqa` comments).

You can read more about pre-commit here: https://pre-commit.com/

## Migrations

If you want to migrate your database, you should run following commands:

```bash
# To run all migrations untill the migration with revision_id.
alembic upgrade "<revision_id>"

# To perform all pending migrations.
alembic upgrade "head"
```

### Reverting migrations

If you want to revert migrations, you should run:

```bash
# revert all migrations up to: revision_id.
alembic downgrade <revision_id>

# Revert everything.
 alembic downgrade base
```

### Migration generation

To generate migrations you should run:

```bash
# For automatic change detection.
alembic revision --autogenerate

# For empty file generation.
alembic revision
```

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . run --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml --project-directory . down
```

For running tests on your local machine.

1. you need to start a database.

I prefer doing it with docker:

```
docker run -p "3306:3306" -e "MYSQL_PASSWORD=cyberarena" -e "MYSQL_USER=cyberarena" -e "MYSQL_DATABASE=cyberarena" -e ALLOW_EMPTY_PASSWORD=yes bitnami/mysql:8.0.30
```

2. Run the pytest.

```bash
pytest -vv .
```

### Coverage

To run tests with coverage you should run:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build; docker-compose -f deploy/docker-compose.yml  --project-directory . run -v "$PWD/cov:/app/src/cov" --rm api pytest --cov=cyberarena/ --cov-report term-missing:skip-covered --cov-report html:cov/cov_html -vv .; docker-compose -f deploy/docker-compose.yml --project-directory . down
```

## The card image generator

Adding a class for generate the final card from a card data and an image path.

Can be customisable directly in the class variable.

### Command line

It can be use with command line (i don't write the docker command but you can open the docker terminal in the app and launch the command).

ex: ```python -m cyberarena.game_module --help```

Or with docker: ```docker-compose -f deploy/docker-compose.yml --project-directory . run --rm api python -m cyberarena.game_module --help```

#### Verify your new cards

```bash
$python -m cyberarena.game_module verify -h
usage: python -m cyberarena.game_module verify [-h] [-d DIRECTORY]
options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        The folder containing all the different cards.
```

With this command you will see all errors in your cards. They will be displayed as normal tex but when the app launch, every error will have different level of severity.

If you want to generate images *YOU MUST* execute this command before to avoid generation errors.

#### Generate cards

```bash
$python -m cyberarena.game_module create  -h
usage: python -m cyberarena.game_module create [-h] [-d DIRECTORY] [-o OUTPUT] [-f]

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        The folder containing all the different cards.
  -o OUTPUT, --output OUTPUT
                        The folder where to put the generated images.
  -f, --force           Force the generation of the image.
```

If you want to generate the card images use this command. It will automatically refresh cards image when their data file or main image are newer.
