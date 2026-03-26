# Ezra Take-Home Submission

## Running Tests

## Project Structure

## Design Decisions

- Page Object Model
- Environment Variables - credentials in .env, never committed

## Installation Instructions

```bash

# Install Poetry if you haven't already
https://python-poetry.org/docs/

# Configure the venv to be added in the repo
poetry config virtualenvs.in-project true

# Install dependencies
poetry install

# Install Browsers
poetry run playwright install chromium
poetry run playwright install firefox
poetry run playwright install webkit


# Copy env example to real env file location
cp .env.example .env

```
