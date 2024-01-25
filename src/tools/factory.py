from tools.duck import DuckCorporationRetriever


def retriever_factory(source_type):
    if source_type == "DUCKDB":
        return DuckCorporationRetriever()
    else:
        raise ValueError("Unknown source type")
