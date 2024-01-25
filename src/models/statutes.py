from pydantic.v1 import BaseModel, Field
from typing import Optional, Sequence


class CompanyIdentification(BaseModel):
    usual_name: str = Field(
        title="Nom Usuel",
        description="Nom utilisé par défaut, peut etre la raison sociale.",
        default="N/A")
    legal_name: str = Field(
        title="Raison Sociale",
        default="N/A")
    status: str= Field(
        title="Statut",
        default="N/A")
    legal_form: str = Field(
        title="Forme Juridique",
        default="N/A")
    country: str = Field(title="Pays",
        default="N/A")
    geographical_zone: str = Field(title="Zone Géographique",
        default="N/A")
    # sigle: Optional[str]
    nom_commercial: Optional[str] = Field(
        title="Nom commercial",
        default="N/A")
    siren_formate: str = Field(title="SIREN",
                               default="N/A")
    siret: str = Field(title="SIRET",
                       default="N/A")
    rcs: str = Field(title="RCS (Ville)",
                     default="N/A")
    last_validation_date: Optional[str]
    company_purpose: Optional[str]
    constitution_date: Optional[str]
    date_of_entry_into_the_group: Optional[str]
    tax_identification_number: Optional[str]
    address_complete: Optional[str]
    capital_currency: Optional[str]
    capital: Optional[str]


class Mandataire(BaseModel):
    nom: Optional[str] = Field(default="Nom")
    prenom: Optional[str] = Field(default="Prenom")
    fonction: Optional[str] = Field(default="CEO")
    nomination: Optional[str]
    nationalite: Optional[str] = Field(default="Française")
    date_de_naissance: Optional[str] = Field(default="20/05/1976")
    lieu: Optional[str] = Field(default="Lille")
    domicile_personnel: Optional[str] = Field(default="Ibiza")


class Societe(BaseModel):
    identification: CompanyIdentification
    mandataires: Sequence[Mandataire]

    class Config:
        arbitrary_types_allowed = True

