# https://python.langchain.com/docs/integrations/document_loaders/duckdb
import openai
from tools.db import Corporation, CorporationRetriever
import duckdb

from utils.config_loader import load_config
import os
import sys
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


config = load_config()

openai.api_key = os.environ['OPENAI_API_KEY']
QUALIFIED_TABLE_NAME = config['DUCKDB']['QUALIFIED_TABLE_NAME']


requete_sql_template = f"""
SELECT 
    code,
    usual_name,
    legal_name,
    status,
    legal_form,
    country,
    geographical_zone,
    last_validation_date,
    presence_of_employees,
    shareholder_agreement,
    company_purpose,
    constitution_date,
    duration,
    unlimited_duration,
    date_of_entry_into_the_group,
    siren,
    siret,
    code_ape,
    rcs_town,
    tax_identification_number,
    managed_company,
    type,
    address_complete,
    position,
    start_date,
    term_date,
    end_date,
    first_name,
    last_name,
    auditor_usual_name,
    representative,
    statutory_advisor_end_date,
    capital_currency,
    capital,
    issued_capital
FROM read_parquet('{QUALIFIED_TABLE_NAME}')
"""

# see https://github.com/langchain-ai/langchain/issues/11341 for tools

class DuckCorporationRetriever(CorporationRetriever):

    def get_corporation_by_code(self, code: int) -> dict:
        """Fetch corporation info from Corporation database for a given code."""

        sql_where = f""" where "code" = {code} limit 1"""
        _requete_sql = requete_sql_template + sql_where

        df = self.run_query(_requete_sql)

        liste_modeles = [Corporation(**row) for row in df.to_dict(orient='records')]

        corp = None
        if liste_modeles:
            corp = liste_modeles[0]

        return corp

    def get_all_usual_name(self):
        """Fetch all corporation usual name from Corporation database."""

        _requete_sql = f"""
            SELECT distinct "usual name" as usual_name FROM '{QUALIFIED_TABLE_NAME}' order by "usual name" asc
            """

        response = self.run_query(_requete_sql)

        # Convertir la colonne 'usual_name' en liste
        usual_names_list = response['usual_name'].tolist()

        return usual_names_list

    # @tool("get_dilitrust_by_usual_name", args_schema=DilitrustByNameInput)
    def get_corporation_by_usual_name(self, usual_name: str) -> dict:
        """Fetch corporation info from database for a given usual name."""

        sql_where = f""" where "usual name" like '%{usual_name}%' limit 1"""
        _requete_sql = requete_sql_template + sql_where

        df = self.run_query(_requete_sql)

        liste_modeles = [Corporation(**row) for row in df.to_dict(orient='records')]

        corp = None
        if liste_modeles:
            corp = liste_modeles[0]

        return corp

    def run_query(self, query):
        """
        Returns:
            - Pandas DataFrame
        """
        try:
           # Retrieving the data from parquet file with duckdb
            with open(QUALIFIED_TABLE_NAME, 'rb') as parquet_file:
                results_df = duckdb.sql(query).df()

            print("Query completed, data retrieved successfully!")
        except Exception as e:
            print(f"Something went wrong... the error is:{e}")
            raise Exception(e)

        return results_df


def main():
    retriever = DuckCorporationRetriever()
    print(retriever.get_corporation_by_code(code=942))
    print(retriever.get_corporation_by_code(20213))
    print(retriever.get_corporation_by_usual_name(usual_name="CIE FINANCIÈRE DE BOULANGER"))


if __name__ == "__main__":
    main()