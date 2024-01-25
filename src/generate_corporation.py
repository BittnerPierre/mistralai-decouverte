from faker import Faker
from enum import Enum
from faker_enum import EnumProvider
import pandas as pd
import random

class Status(Enum):
    ABSORBED = "Absorbed"
    ARCHIVED = "Archived"
    CEDED = "Ceded"
    DISSOLVED = "Dissolved"
    LIQUIDATED = "Liquidated"
    CLOSED = "Closed"
    ACTIVE = "Active"
    SLEEPING = "Sleeping"

class GeoZone(Enum):
    AFRICA = "AFRICA"
    NORTH_AMERICA = "NORTH_AMERICA"
    SOUTH_AMERICA = "SOUT_AMERICA"
    ASIA = "ASIA"
    PACIFIC = "PACIFIC"
    OCEANIA_ANTARTIC = "OCEANIA_ANTARTIC"
    EUROPE_NON_UE = "EUROPE_NON_EU"
    EUROPEAN_UNION = "EUROPEAN_UNION"
    MIDDLE_EAST = "MIDDLE_EAST"

class LegalForm(Enum):
    EI = "Entrepreneur individuel (EI)"
    EURL = "Entreprise unipersonnelle à responsabilité limitée (EURL)"
    SARL = "Société à responsabilité limitée (SARL)"
    SASU = "Société par actions simplifiée unipersonnelle (SASU)"
    SAS = "Société par actions simplifiée (SAS)"
    SA = "Société anonyme (SA)"
    SNC = "Société en nom collectif (SNC)"
    SCS = "Société en commandite simple (SCS)"
    SCA = "Société en commandite par actions (SCA)"

class CorporationGenerator:
    def __init__(self, num_records):
        self.num_records = num_records
        self.fake = Faker('fr_FR')

    def generate_data(self):
        data = []
        for _ in range(self.num_records):
            record = {
                "code": self.fake.unique.random_int(10000, 99999),
                "usual_name": self.fake.company(),
                "legal_name": self.fake.company_suffix(),
                "status": self.fake.random_element(Status.__members__.values()).value,
                "legal_form": self.fake.random_element(LegalForm.__members__.values()).value,
                "country": self.fake.country(),
                "geographical_zone": self.fake.random_element(GeoZone.__members__.values()).value,
                "last_validation_date": self.fake.date() if random.choice([True, False]) else None,
                "presence_of_employees": random.choice([True, False]) if random.choice([True, False]) else None,
                "shareholder_agreement": random.choice([True, False]) if random.choice([True, False]) else None,
                "company_purpose": self.fake.sentence() if random.choice([True, False]) else None,
                "constitution_date": self.fake.date() if random.choice([True, False]) else None,
                "duration": random.randint(1, 100) if random.choice([True, False]) else None,
                "unlimited_duration": random.choice([True, False]) if random.choice([True, False]) else None,
                "date_of_entry_into_the_group": self.fake.date() if random.choice([True, False]) else None,
                "siren": self.fake.siren() if random.choice([True, False]) else None,
                "siret": self.fake.siret() if random.choice([True, False]) else None,
                "code_ape": self.fake.bothify(text='####?') if random.choice([True, False]) else None,
                "rcs_town": self.fake.city() if random.choice([True, False]) else None,
                "tax_identification_number": self.fake.vat_id() if random.choice([True, False]) else None,
                "managed_company": random.choice([True, False]) if random.choice([True, False]) else None,
                "type": self.fake.word() if random.choice([True, False]) else None,
                "address_complete": self.fake.address() if random.choice([True, False]) else None,
                "position": self.fake.job() if random.choice([True, False]) else None,
                "start_date": self.fake.date() if random.choice([True, False]) else None,
                "term_date": self.fake.date() if random.choice([True, False]) else None,
                "end_date": self.fake.date() if random.choice([True, False]) else None,
                "first_name": self.fake.first_name() if random.choice([True, False]) else None,
                "last_name": self.fake.last_name() if random.choice([True, False]) else None,
                "auditor_usual_name": self.fake.name() if random.choice([True, False]) else None,
                "representative": self.fake.name() if random.choice([True, False]) else None,
                "statutory_advisor_end_date": self.fake.date() if random.choice([True, False]) else None,
                "capital_currency": self.fake.currency_code() if random.choice([True, False]) else None,
                "capital": random.randint(1000, 100000) if random.choice([True, False]) else None,
                "issued_capital": random.randint(500, 50000) if random.choice([True, False]) else None,
            }
            data.append(record)
        return data

    def to_parquet(self, filename):
        data = self.generate_data()
        df = pd.DataFrame(data)
        df.to_parquet(filename, index=False)

# Example usage
generator = CorporationGenerator(100)  # Generate 100 fake records
generator.to_parquet('../data/duckdb/corporations.parquet')