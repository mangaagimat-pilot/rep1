from ingestion.landing_to_bronze import run_ingestion


if __name__ == "__main__":
    print(run_ingestion([{"id": 1, "source": "landing"}], source="landing"))
