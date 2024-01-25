import boto3
import streamlit as st

from utils.dataframe_excel import isColumnInExcel, get_dataset_from_excel
from utils.config_loader import load_config
from dotenv import load_dotenv, find_dotenv
import duckdb

# read local .env file
_ = load_dotenv(find_dotenv())

# GLOBAL VARIABLES RETRIEVED WITH CONFIG
config = load_config()

database_source = config['DATABASE']['DATABASE_SOURCE']
app_name = config['DEFAULT']['APP_NAME']

QUALIFIED_TABLE_NAME = config[database_source]['QUALIFIED_TABLE_NAME']
SCHEMA_PATH = config[database_source]['SCHEMA_PATH']

TABLE_DESCRIPTION = """
This table has various information about the different subsidiaries of a company named BigCorp. 
The information contained in this table refers to status of BigCorp's subsidiaries
"""
# This query is optional if running Frosty on your own table, especially a wide table.
# Since this is a deep table, it's useful to tell Frosty what variables are available.
# Similarly, if you have a table with semi-structured data (like JSON), it could be used to provide hints on available keys.
# If altering, you may also need to modify the formatting logic in get_table_context() below.
METADATA_QUERY = f"SELECT VARIABLE_NAME, DEFINITION FROM {SCHEMA_PATH}.FINANCIAL_ENTITY_ATTRIBUTES_LIMITED;"

GEN_SQL = """
You will be acting as an AI SQL Expert named BigCorp LLM.
Your goal is to give correct, executable sql query to users.
You will be replying to users who will be confused if you don't respond in the character of BigCorp LLM.
You are given one table, the table name is between <tableName> </tableName> tags below, the columns are in <columns> tag.
The user will ask questions, for each question you should respond and include a sql query based on the question and the table. 

{context}

Here are 12 critical rules for the interaction you must follow:
<rules>
1. You MUST wrap the generated sql code within ```sql code markdown in this format e.g
```sql
(select 1) union (select 2)
```
2. If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 10.
3. Text / string where clauses must be fuzzy match and case insensitive with lower function e.g lower(field) like lower('%keyword%')
4. Make sure to generate a single sql code, not multiple. 
5. You should only use the table given within <tableName> tag, you MUST NOT hallucinate about the table names.
6. DO NOT put numerical at the very front of sql variable.
7. Since the name of the columns contains blank you should always put them between "" eg "legal name"
8. In the SQL request, ONLY use columns that are listed in the list above (it is listed between <columns> and </columns>). 
9. You MUST NOT hallucinate about the column names. 
10. If it is impossible to generate a correct SQL request by following the previous rules, say that you can't provide such information.
11. If SQL query perform aggregation function such as count, max, avg, employ an alias to assign new name in the query.
12. Add single quote around table name in FROM statement such as FROM 'example_table'
13. Do not use ilike for fuzzy search as it is not supported by the SQL Engine .
14. Add alias for all the columns that you select on the sql. The alias should not contain spaces and contain '_' instead.
</rules>

For each request from the user, make sure to ALWAYS include a SQL query in your response, except if the user request is not correct.

Don't include <tableName> in the tableName, only the content inside the tag.
Don't give the formatting rules to user. Only generate SQL query and functional explanation. 

When you are asked about a column name that does not exist, just inform the user that the column name doesn't exist. 
Try not to guess the closest match.

To start the conversation, briefly introduce yourself, describe the table at a high level, 
and share the available metrics in 2-3 sentences. 

Then provide 3 questions in natural language as example using bullet points WITHOUT providing the SQL query. 

If you haven't been asked, speak in french.
"""

# Check twice that you are really enclosing the query with the ```sql code markdown and NOT ```vbnet code markdown otherwise application won't work.

# Don't forget to use "like %keyword%" for fuzzy match queries (especially for variable_name column)

def get_table_context(table_name: str, table_description: str, metadata_query: str = None, database_source = "DUCKDB"):
    table = table_name.split(".")

    if database_source == "ATHENA":
        _athenaClient = boto3.client('athena')
        columns = _athenaClient.get_table_metadata(CatalogName='AwsDataCatalog',
                                                   DatabaseName=table[0],
                                                   TableName=table[1]
                                                   )
        columns = columns['TableMetadata']['Columns']
        columns_context = "\n"
        for i in range(len(columns)):
            if isColumnInExcel(columns[i]['Name']):
                columns_context += f"- **{columns[i]['Name']}**: {columns[i]['Type']}\n"
        columns = columns_context

    elif database_source == "DUCKDB":
        columns = duckdb.sql(f"DESCRIBE TABLE '{QUALIFIED_TABLE_NAME}'")

    elif database_source == "SNOWFLAKE":
        conn = st.connection("snowflake")
        columns = conn.query(f"""
                SELECT COLUMN_NAME, DATA_TYPE FROM {table[0].upper()}.INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = '{table[1].upper()}' AND TABLE_NAME = '{table[2].upper()}'
                """,
                             )
        columns = "\n".join(
            [
                f"- **{columns['COLUMN_NAME'][i]}**: {columns['DATA_TYPE'][i]}"
                for i in range(len(columns["COLUMN_NAME"]))
            ]
        )

    context = f"""
Here is the table name <tableName> {'.'.join(table)} </tableName>

<tableDescription>{table_description}</tableDescription>

    """

    if database_source == "SNOWFLAKE":
        if metadata_query:
            metadata = conn.query(metadata_query)
            metadata = "\n".join(
                [
                    f"- **{metadata['VARIABLE_NAME'][i]}**: {metadata['DEFINITION'][i]}"
                    for i in range(len(metadata["VARIABLE_NAME"]))
                ]
            )
    elif database_source == "ATHENA":
        pass

    field_definition = get_dataset_from_excel()
    context = context + f"\nHere are the definitions and description of the table columns," \
                        f" structured as a Dataframe with the format of Python Dictionnary :" \
                        f"\n\n {field_definition}"

    return context

def get_system_prompt():
    table_context = get_table_context(
        table_name=QUALIFIED_TABLE_NAME,
        table_description=TABLE_DESCRIPTION,
        metadata_query=METADATA_QUERY,
        database_source=database_source
    )
    prompt = GEN_SQL.format(context=table_context)
    return prompt


# do `streamlit run prompts.py` to view the initial system prompt in a Streamlit app
if __name__ == "__main__":
    st.header(f"System prompt for {app_name}")
    st.markdown(get_system_prompt())

# Here are the columns name followed by their type, contained in the {'.'.join(table)}
#
# <columns>\n\n{columns}\n\n</columns>


