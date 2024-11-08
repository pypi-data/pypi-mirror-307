from metaflow import step, FlowSpec, dbt, kubernetes, conda_base, Parameter, card
from config import DBT_PROFILES, DUCKDB_PATH, PVC_NAME, PVC_MOUNT
import os


@conda_base(libraries={"dbt-duckdb": "1.7.0", "pandas": "2.2.0"})
class DuckDBFlow(FlowSpec):
    cleanup = Parameter(
        "cleanup", default=False, help="Clean up old DuckDB file from volume"
    )

    @kubernetes(persistent_volume_claims={PVC_NAME: PVC_MOUNT})
    @step
    def start(self):
        if self.cleanup:
            print("cleaning up old DuckDB file")
            os.remove(DUCKDB_PATH)

        print("Read data to a dataframe and save it into DuckDB")
        import duckdb
        import pandas as pd

        dataframe = pd.read_csv("data.csv")

        with duckdb.connect(DUCKDB_PATH) as con:
            con.sql("CREATE TABLE IF NOT EXISTS raw_data AS SELECT * FROM dataframe")
            con.sql("INSERT INTO raw_data SELECT * FROM dataframe")

        self.next(self.custom_models)

    @card
    @kubernetes(persistent_volume_claims={PVC_NAME: PVC_MOUNT})
    @dbt(project_dir="./duckdb_project", profiles=DBT_PROFILES)
    @step
    def custom_models(self):
        print("Run custom DBT models on DuckDB after Dataframe load.")

        print("Loading DuckDB contents as dataframe")
        import duckdb

        with duckdb.connect(DUCKDB_PATH) as con:
            self.post_2000_movies = con.sql("SELECT * FROM post_2000_movies").df()
        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    DuckDBFlow()
