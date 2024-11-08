# Monzy
A Python data pipeline to fetch, transform, and process Monzo transactions and pot data from the Monzo API.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project provides a data pipeline to interact with the Monzo API, retrieve transaction and pot data, transform it into a structured format, and process it for analysis or storage in a PostgreSQL database. It uses the monzo-API Python package developed by Peter MacDonald: https://github.com/petermcd/monzo-api

## Features

- Fetch Monzo transactions and pot data
- Transform and normalize transaction data
- Process transactions to prepare for analysis
- Insert and query data in a PostgreSQL database
- Environment configuration using `.env` files

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/monzy.git
    cd monzy
    ```

2. **Create and activate a virtual environment with Poetry:**
    ```sh
    ./local-setup.sh
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory of the project and add your environment variables:
    ```env
    DB_USERNAME=your_username
    DB_PASSWORD=your_password
    DB_HOST=your_host
    DB_NAME=your_database
    DB_PORT=your_port
    ```

## Usage

### Monzo API Token

...
