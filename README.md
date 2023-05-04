[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

# What is this?

**Transactions** is a tool to analyse data from MoneyDashboard ([https://www.moneydashboard.com](https://www.moneydashboard.com)).

I found their app isn't great at exploring transaction data in depth, so I created my own api to add more filter and aggregation functionality.

---

### Built With

[![Next][next.js]][next-url] [![Python][python]][python-url]

## Feature Summary

-   Display all transactions.
-   Display a monthly breakdown of transactions by tag.
-   Display monthly timeline of total in / out by tag.
-   Add a budget and track spending by tag for the current month.

# Contents

-   [Installation](#installation)
-   [Running](##running)
-   [How to use](#how-to-use)
    -   [Config.json](#config.json)
    -   [Loading transactions](#loading-transactions)
-   [Features](#features)
-   [License](#license)

# Installation

To install this application, clone the repo and follow these steps.

1. Clone the repo

```sh
git clone https://github.com/TheIthorian/Transactions.git
```

2.  Make sure `python` and `node.js` are installed.

```sh
python --version
```

```sh
npm --version
```

3.  Install python dependencies:

It is optional, but recommended to install `pipenv`, a python package manager which makes managing virtual environments easier.
If you chose not to install this, the corresponding commands can be found in `src/Pipfile`.

On Windows, you'll need to add the following to your PATH environment variable and restart your PC:

-   c:\users\\<username\>\appdata\roaming\python\python310\site-packages
-   c:\users\\<username\>\appdata\roaming\python\python310\scripts

```sh
cd src
pip install --user pipenv
pipenv install
```

4.  Install node modules

```sh
cd web
npm install
```

5. Rename the `config_example.json` file to `config.json`. In the file, set your password:

```json
"PASSWORD": "my_password"
```

Use this password when logging into your account.

## Running

1. Start the python (flask) server

```sh
cd src
pipenv run serve
```

2. Start the node server

```sh
cd web
npm run prod
```

This will start the app, but by default there are no transactions.

## Loading transactions

You can import import transactions either using the UI or with the CLI.

<details>
<summary>With UI</summary>

Go to the `Upload Transactions` tab in the UI. Upload on or more csv files which contain the transactions and hit submit. This will save all **new** transactions to the database.

Below the upload field, there is a grid which shows all past upload attempts.

At the moment you cannot yet switch accounts or formats from this page. For that, you will need to use the CLI...

</details>

<details>
<summary>With CLI</summary>

To load transactions, go to [https://www.moneydashboard.com](https://www.moneydashboard.com) and download all transactions to a csv file. Save this file to the root of the project directory and run `pipenv run import`. This saves all the transactions to the persistent database.

`import` can be run with the following arguments:

```-h, --help show this help message and exit.
-f FILENAME, --filename FILENAME
    Sets the filename of the transactions csv to import.

-s {moneydashboard,metro}, --source {moneydashboard,metro}
    Sets the source of the transactions. Supported options depend automatically on which readers are registered in import.py.

-a ACCOUNT, --account ACCOUNT
    Sets which account to use.
```

Using a different account creates a new database to store transactions. This is useful if you need to separate accounts.

#### Don't have moneydashboard?

_No problem!_

It is possible to define your own `Reader` to map different csv formats:

1. Make a new reader file in `src/app/importer/`
2. Define a function which returns a Reader instance
    - Make sure to set the `source`, `csv_headers`, and `mapping` attributes
    - `source`: The name of the source. E.g. `'metro bank'`
    - `csv_headers`: A list of each header in the source csv file
    - `mapping`: A function which takes in a csv row, and returns a `dict` containing the following values:
        - Account
        - Date
        - CurrentDescription
        - OriginalDescription
        - Amount
        - L1Tag
        - L2Tag
        - L3Tag
3. In `src/app/importer/register.py`, add your new reader function to the `register` in `register_readers()`
4. See `src/importer/metro_reader.py` for an example on how to do this

You'll then be able to use this as a `--source` argument value when running `pipenv run import`.

</details>

# Additional Info

## Config.json

This is where all the config for the application is stored. See below for an explanation of each property:

-   `API_KEY `- All requests use this key to validate access to the api.
-   `REQUEST_ORIGIN` - List of allowed request origins. Use `*` to allow all.
-   `HOST` - Which ip the backend server will be hosted on.
-   `PRINT_QUERIES` - Log each query for debugging.
-   `PASSWORD` - The password used to log in (for basic security).

## CLI Arguments

Additional arguments can be passed to the `dev` and `serve` commands.

```-h, --help           show this help message and exit
  -d, --dev             Runs in development mode
  --demo                Runs in demo mode which uses fake data
  -a ACCOUNT, --account ACCOUNT
                        Sets which account to use
```

Using a different account creates a new database to store transactions. This is useful if you need to separate accounts.

# Features

## Transaction List

The transaction list displays a detailed list of all transactions.

![The transaction list with the start date filter being changed](./project/list-demo.gif 'Transaction list example')

## Transaction Breakdown

A breakdown of the total transaction amounts under each tag type. The tag level and specificity increases towards the center.

![The transaction breakdown with the start date and tag filter being changed](./project/breakdown-demo.gif 'Transaction breakdown example')

## Transaction Timeline

The total amount by tag across a monthly timeline.

![The transaction timeline with the start date and tag filter being changed](./project/timeline-demo.gif 'Transaction timeline example')

## Filtering

In each data display component, it is possible to filter the results by date and tag (inclusive):

![Two date pickers and a tag filter dropdown used to filter which transactions are included in the data](./project/Filter-example.png 'Filtering example')

# License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/TheIthorian/Transactions.svg?style=for-the-badge
[contributors-url]: https://github.com/TheIthorian/Transactions/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TheIthorian/Transactions.svg?style=for-the-badge
[forks-url]: https://github.com/TheIthorian/Transactions/network/members
[stars-shield]: https://img.shields.io/github/stars/TheIthorian/Transactions.svg?style=for-the-badge
[stars-url]: https://github.com/TheIthorian/Transactions/stargazers
[issues-shield]: https://img.shields.io/github/issues/TheIthorian/Transactions.svg?style=for-the-badge
[issues-url]: https://github.com/TheIthorian/Transactions/issues
[license-shield]: https://img.shields.io/github/license/TheIthorian/Transactions.svg?style=for-the-badge
[license-url]: https://github.com/TheIthorian/Transactions/blob/master/LICENSE
[next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[next-url]: https://nextjs.org/
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://python.org/
