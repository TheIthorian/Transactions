# What is this?

**Transactions** is a tool to analyse data from Moneydashborad ([https://www.moneydashboard.com](https://www.moneydashboard.com)).

I found their app isn't great at exploring transaction data in depth, so I created my own api to add more filter and aggregation functionality.

## Features

-   Display all transactions.
-   Display a monthly breakdown of transactions by tag.
-   Display monthly timeline of total in / out by tag.

# Contents

-   [Installation](#installation)
    -   [Running](##running)
-   [How to use](#how-to-use)
    -   [Config.json](#config.json)
    -   [Loading transactions](#loading-transactions)
    -   [Filtering](#filtering)

# Installation

To install this application, clone the repo and following these steps.

1. Make sure python and node are installed.

2. Install python dependencies:

    - `cd src`
    - (optional) Install `pipenv` using `pip install --user pipenv`.  
      This is a python package manager which makes managing virtual environments easier. If you chose not to install this, the corresponding commands can be found in `src/Pipfile`.
      On Widnows, you'll need to add the following to your PATH environment variable and restart your PC
        - c:\users\\<username\>\appdata\roaming\python\python310\site-packages
        - c:\users\\<username\>\appdata\roaming\python\python310\scripts
    - If `pipenv` is installed, run: `pipenv install`
    - Otherwise run `pip install requirements.txt`
    - Create the database
        - `pipenv run migrate`

3. Install node modules
    - `cd web/transactions`
    - `npm install`

## Running

1. Start the flask server

    - `cd src`
    - `pipenv run serve`

2. Start the node server
    - `cd web/transactions`
    - `npm run start`

# How to use

## Config.json

This is where all the config for the application is stored. See below for an explanation of each property:

-   `API_KEY `- All requests use this key to validate access to the api.
-   `REQUEST_ORIGIN` - List of allowed request origins. Use `*` to allow all.
-   `HOST` - Which ip the backend server will be hosted on.
-   `PRINT_QUERIES_IN_TESTS` - Log each query when running tests.

## Loading transactions

To load transactions, go to [https://www.moneydashboard.com](https://www.moneydashboard.com) and dowload all transactions to a csv file. Save this file to the root of the project directory and run `pipenv run import`. This saves all the transactions to the persistent database.

## Filtering

In each data display component, it is possible to filter the results by date and tag (inclusive):
![Two date pcikers and a tag filter dropdown used to filter which transactions are included in the data](./project/Filter-example.png 'Filtering example')
