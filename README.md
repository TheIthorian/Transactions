## Installation

To install this application, clone the repo and following these steps
1. Make sure python and node are installed.

2. Install python dependencies:
   * `cd src`
   * (optional) Install `pipenv` using `pip install --user pipenv`.  
   This is a python package manager which makes managing virtual environments easier. If you chose not to install this, the corresponding commands can be found in `src/Pipfile`.
   If on Widnows, you'll need to add the following to your PATH environment variable and restart your PC
     * c:\users\\<username\>\appdata\roaming\python\python310\site-packages
     * c:\users\\<username\>\appdata\roaming\python\python310\scripts  
   * If `pipenv` is installed, run: `pipenv install`
   * Otherwise run `pip install requirements.txt`
   * Create the database
     * `pipenv run migrate`

3. Install node modules
   * `cd web/transactions`
   * `npm install`

## Running

1. Start the flask server  
   * `cd src`
   * `pipenv run serve`

2. Start the node server
   * `cd web/transactions`
   * `npm run start`

