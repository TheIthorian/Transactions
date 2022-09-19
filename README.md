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
-   [License](#license)

# Installation

To install this application, clone the repo and following these steps.

1. Clone the repo

```sh
git clone https://github.com/TheIthorian/Transactions.git
```

2.  Make sure python and node are installed.

```sh
python --version
```

```sh
npm --version
```

3.  Install python dependencies:

It is optional, but recommended to install `pipenv`, a python package manager which makes managing virtual environments easier.
If you chose not to install this, the corresponding commands can be found in `src/Pipfile`.

On Widnows, you'll need to add the following to your PATH environment variable and restart your PC:

-   c:\users\\<username\>\appdata\roaming\python\python310\site-packages
-   c:\users\\<username\>\appdata\roaming\python\python310\scripts

```sh
cd src
pip install --user pipenv
pipenv install
pipenv run migrate
```

4.  Install node modules

```sh
cd web/transactions
npm install
```

## Running

1. Start the flask server

```sh
cd src
pipenv run serve
```

2. Start the node server

```sh
cd web/transactions
npm run start
```

# How to use

## Config.json

This is where all the config for the application is stored. See below for an explanation of each property:

-   `API_KEY `- All requests use this key to validate access to the api.
-   `REQUEST_ORIGIN` - List of allowed request origins. Use `*` to allow all.
-   `HOST` - Which ip the backend server will be hosted on.
-   `PRINT_QUERIES_IN_TESTS` - Log each query when running tests.

## Loading transactions

To load transactions, go to [https://www.moneydashboard.com](https://www.moneydashboard.com) and download all transactions to a csv file. Save this file to the root of the project directory and run `pipenv run import`. This saves all the transactions to the persistent database.

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
