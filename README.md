[![Python application setup with GitHub actions](https://github.com/richardogoma/etl-with-python/actions/workflows/python-app.yml/badge.svg?branch=main&event=push)](https://github.com/richardogoma/etl-with-python/actions/workflows/python-app.yml)

# ETL with Python

**ETL stands for Extract, Transform, Load,** and it refers to the process of extracting data from various sources, transforming it into a format that is suitable for analysis, and loading it into a destination data store, such as a data warehouse or data lake.

This is a secondary project or study of [Mislav Vuletić's daily-expense-manager project](https://github.com/MasterMedo/daily-expense-manager) **with a focus on the processing of the dataset used in the inquest.** The goal of Mislav's case study was to process historical daily expenses data with machine learning algorithms to understand and predict an individual's spending behaviour. 

_**Please refer to this project's wiki for the justification for a secondary study.**_

# Setting up this Project
- This program was developed on a `Ubuntu 22.04.2 LTS` machine in a `Python 3.10.6 virtual environment` 
```bash
# Run on sh - Setup virtual environment locally
lsb_release -a
python --version
python3 -m venv .venv
source .venv/bin/activate
```
- The python program, `etl_program.py` makes HTTP API requests to RapidAPI's Currency Conversion and Exchange Rates endpoints. You require an API key to use this project; this can be obtained by signing up for an account [here](https://rapidapi.com/principalapis/api/currency-conversion-and-exchange-rates)
- Your API key can be added as a secret to [GitHub codespaces](https://docs.github.com/en/codespaces/managing-your-codespaces/managing-encrypted-secrets-for-your-codespaces), or as an environment variable when working locally.
```bash
# Run on codespaces terminal
echo $RAPID_API_KEY

# Run on sh locally 
export rapid_api_key='----Your key goes here-----'
```
- The project has been structured with a scaffolding or `Makefile`. You can setup this project easily by running `make all` in your virtual environment
```bash
# Run on sh 
make all
```
- Grant executable permissions to `etl_program.py` and run the program.
```bash
# Run on sh 
chmod +x etl_program.py
./etl_program.py
```
<img width="527" alt="image" src="https://user-images.githubusercontent.com/108296666/230447530-59c111a7-dbe6-490a-af02-faee9689976a.png">
<img width="731" alt="image" src="https://user-images.githubusercontent.com/108296666/230447589-e008df3a-2584-4593-a226-76cbc9b91d0e.png">

# Input and Output
The input, output and test file paths are accessed by the program via the configuration file- `config.ini`

