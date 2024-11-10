# reworkd_platform

This project was generated using fastapi_template.

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m reworkd_platform
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: https://python-poetry.org/

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f deploy/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f deploy/docker-compose.yml --project-directory . build
```

## Project structure

```bash
$ tree "reworkd_platform"
reworkd_platform
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
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

All environment variables should start with "REWORKD_PLATFORM_" prefix.

For example if you see in your "reworkd_platform/settings.py" a variable named like
`random_parameter`, you should provide the "REWORKD_PLATFORM_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `reworkd_platform.settings.Settings.Config`.

An example of .env file:

```bash
REWORKD_PLATFORM_RELOAD="True"
REWORKD_PLATFORM_PORT="8000"
REWORKD_PLATFORM_ENVIRONMENT="development"
```

You can read more about BaseSettings class here: https://pydantic-docs.helpmanual.io/usage/settings/

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

You can read more about pre-commit here: https://pre-commit.com/

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . down
```

For running tests on your local machine.

1. you need to start a database.

I prefer doing it with docker:

```
docker run -p "3306:3306" -e "MYSQL_PASSWORD=reworkd_platform" -e "MYSQL_USER=reworkd_platform" -e "MYSQL_DATABASE=reworkd_platform" -e ALLOW_EMPTY_PASSWORD=yes bitnami/mysql:8.0.30
```

2. Run the pytest.

```bash
pytest -vv .
```

## Running linters

```bash
# Flake
poetry run black .
poetry run autoflake --in-place --remove-duplicate-keys --remove-all-unused-imports -r .
poetry run flake8
poetry run mypy .

# Pytest
poetry run pytest -vv --cov="reworkd_platform" .

# Bump packages
poetry self add poetry-plugin-up
poetry up --latest
```

## Installing the package using pip

To install the `reworkd_platform` package using pip, run the following command:

```bash
pip install reworkd_platform
```

## Using the package in any code

To use the `reworkd_platform` package in your code, you can import it as follows:

```python
import reworkd_platform

# Example usage
reworkd_platform.some_function()
```

## Using pip functions

The `reworkd_platform` package provides several functions for interacting with agents. Here are some examples:

### Starting a goal agent

```python
from reworkd_platform.web.api.agent.agent_service.open_ai_agent_service import OpenAIAgentService

# Initialize the OpenAIAgentService
agent_service = OpenAIAgentService(...)

# Start a goal agent
tasks = agent_service.pip_start_goal_agent(goal="Your goal here")
print(tasks)
```

### Analyzing a task agent

```python
from reworkd_platform.web.api.agent.agent_service.open_ai_agent_service import OpenAIAgentService

# Initialize the OpenAIAgentService
agent_service = OpenAIAgentService(...)

# Analyze a task agent
analysis = agent_service.pip_analyze_task_agent(goal="Your goal here", task="Your task here", tool_names=["tool1", "tool2"])
print(analysis)
```

### Executing a task agent

```python
from reworkd_platform.web.api.agent.agent_service.open_ai_agent_service import OpenAIAgentService

# Initialize the OpenAIAgentService
agent_service = OpenAIAgentService(...)

# Execute a task agent
response = agent_service.pip_execute_task_agent(goal="Your goal here", task="Your task here", analysis=analysis)
print(response)
```

### Creating tasks agent

```python
from reworkd_platform.web.api.agent.agent_service.open_ai_agent_service import OpenAIAgentService

# Initialize the OpenAIAgentService
agent_service = OpenAIAgentService(...)

# Create tasks agent
tasks = agent_service.pip_create_tasks_agent(goal="Your goal here", tasks=["task1", "task2"], last_task="Your last task here", result="Your result here")
print(tasks)
```

### Summarizing task agent

```python
from reworkd_platform.web.api.agent.agent_service.open_ai_agent_service import OpenAIAgentService

# Initialize the OpenAIAgentService
agent_service = OpenAIAgentService(...)

# Summarize task agent
response = agent_service.pip_summarize_task_agent(goal="Your goal here", results=["result1", "result2"])
print(response)
```

### Chatting with agent

```python
from reworkd_platform.web.api.agent.agent_service.open_ai_agent_service import OpenAIAgentService

# Initialize the OpenAIAgentService
agent_service = OpenAIAgentService(...)

# Chat with agent
response = agent_service.pip_chat(message="Your message here", results=["result1", "result2"])
print(response)
```
