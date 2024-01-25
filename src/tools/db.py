from typing import Optional

from pydantic import BaseModel, Field


class Corporation(BaseModel):
    code: Optional[int]
    usual_name: Optional[str]
    legal_name: Optional[str]
    status: Optional[str]
    legal_form: Optional[str]
    country: Optional[str]
    geographical_zone: Optional[str]
    last_validation_date: Optional[str]
    presence_of_employees: Optional[bool]
    shareholder_agreement: Optional[bool]
    company_purpose: Optional[str]
    constitution_date: Optional[str]
    duration: Optional[int]
    unlimited_duration: Optional[bool]
    date_of_entry_into_the_group: Optional[str]
    siren: Optional[str]
    siret: Optional[str]
    code_ape: Optional[str]
    rcs_town: Optional[str]
    tax_identification_number: Optional[str]
    managed_company: Optional[bool]
    type: Optional[str]
    address_complete: Optional[str]
    position: Optional[str]
    start_date: Optional[str]
    term_date: Optional[str]
    end_date: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    auditor_usual_name: Optional[str]
    representative: Optional[str]
    statutory_advisor_end_date: Optional[str]
    capital_currency: Optional[str]
    capital: Optional[int]
    issued_capital: Optional[int]

class CorporationByCodeInput(BaseModel):
    code: int = Field(..., description="Corporation code (code) of enterprise")


class CorporationByNameInput(BaseModel):
    usual_name: str = Field(..., description="Usual name of enterprise")


class CorporationRetriever:
    def get_corporation_by_code(self, code: int) -> dict:
        raise NotImplementedError("Subclasses should implement this!")

    def get_all_usual_name(self):
        raise NotImplementedError("Subclasses should implement this!")

    def get_corporation_by_usual_name(self, usual_name: str) -> dict:
        raise NotImplementedError("Subclasses should implement this!")

    def run_query(self, query):
        raise NotImplementedError("Subclasses should implement this!")


