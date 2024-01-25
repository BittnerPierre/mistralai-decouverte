# Mistral AI Découverte


## Overview

In this project, we will build an LLM-powered assistant with Mistral AI that performs data exploration and question answering 
by writing and executing SQL queries on data (Duckdb).
The application can also edit and fix data on the database base on statutes and KBIS that you
upload in an embedded Chroma DB.
The application uses Streamlit, langchain and is plugged into your Mistral AI Platform.

## Dependencies
In order to run the application you should install streamlit, mistralai, langchain, 
chromadb and duckdb. See requirements.txt.

I'm using python 3.9.13 and conda for environment management.

Create env with conda
```sh
conda create -n mistralai-decouverte python=3.9
```

Activate the env:
```sh
conda activate mistralai-decouverte          
```

Once python installed, update the pip version by typing :
```sh
python -m pip install --upgrade pip
```

Then install the project dependencies by typing :
```sh
run pip install -r requirements.txt
```

## Credentials
Application is looking a .env file within the PATH of the project that contains following variables:
* MISTRAL_API_KEY=

## setup
Application can be setup with the file conf/config.ini

Data catalog can be extended with excel in 'data/data-catalog/data-catalog.xlsx'.
I use this file because I didn't find a way to list all field with duckdb and parquet 
(unlike Frosty with snowflake where they query the metadata directly).

You can add field definition (technical and business) to help LLM understanding of schema.

A cache directory is used for LLM generated company in 'data/cache'.

## Run the app

Once environment is set up and secrets are configured (MistralAI) in a .env file 
within the application path, the app can be run by:

```sh
streamlit run src/Hello.py
```

## Additional informations


### Chat
Example of **streamlit** with LLM on their [github](https://github.com/streamlit/llm-examples)

### Query
Query use case is based on [Frosty](https://github.com/Snowflake-Labs/sfguide-frosty-llm-chatbot-on-streamlit-snowflake/blob/main/src/frosty_app.py)
Behaviour of Mistral does not look very stable.
You can create additional field in tools/db.py (the model) and tools/duck.py (the select sql query)
You can generate new data in data/duckdb/corporations.parquet with :
```sh
python generate_corporation.py
```
and update data-catalog.xlsx if you add more fields.
The data generation script is very dummy but somehow functional. I use faker for that. 

### Data Extraction
You can use this [KBIS](https://www.economie.gouv.fr/files/files/PDF/2020/Annexe1-1-K-bisCMB.pdf) as example for data extraction or any corporate statutes.

