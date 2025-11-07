# Stack
- Dash (Python 3.14)
- FastApi (Python 3.12)
- MlFlow (Python 3.12)

# Project structure
```
ai-btc/
├── front/
│   ├── Dockerfile
│   ├── .env
│   └── tests/
├── back/
│   ├── Dockerfile
│   ├── .env
│   └── tests/
├── mlflow/
│   ├── Dockerfile
│   ├── .env
│   └── tests/
└── .github/
    └── workflows/
        └── deploy.yml
```

# Goals
- Automate linting and testing for each service on every push to main
- Deploy each service to Render only if tests pass
- Use GitHub Actions for orchestration
- Keep environment variables secure via GitHub Secrets and Render UI

# Flow

When a developer pushes to main, GitHub Actions runs linting and tests for each service.

# Strategy

Our repository is on Github, so we will use Github Actions for CI and Render for CD.

# CD

On Render you will need to create 3 separate `Web Services`:
- front
- back
- mlflow

Then, for each serviced, set the root directory.

After that you have to set `Docker environment`.

You also have to manually add environement variables from .env 

Finally, you need to keep a copy of each service's Deploy Hook URL for CI/CD

# CI

This will be our `deploy.yml`, since we have different Python version (thanks MlFlow), we will use a matrix strategy, so we can run lints and tests in different Python versions.

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [front, back, mlflow]
        include:
          - service: front
            python: "3.14"
          - service: back
            python: "3.12"
          - service: mlflow
            python: "3.12"

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python }}

    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh

    - name: Install dependencies with uv
      run: |
        uv pip install flake8 pytest
        if [ -f "${{ matrix.service }}/requirements.txt" ]; then
          uv pip install -r ${{ matrix.service }}/requirements.txt
        fi

    - name: Lint ${{ matrix.service }}
      run: flake8 ${{ matrix.service }}

    - name: Test ${{ matrix.service }}
      run: pytest ${{ matrix.service }}/tests

  deploy:
    needs: lint-and-test
    runs-on: ubuntu-latest
    steps:
    - name: Trigger Render Deploy
      run: curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

# Secrets

You need to store `RENDER_DEPLOY_HOOK` in GitHub Secrets.

# Conclusion

We have seen how to setup CI/CD with Github Actions + Render.

This will automate the process for deployement.