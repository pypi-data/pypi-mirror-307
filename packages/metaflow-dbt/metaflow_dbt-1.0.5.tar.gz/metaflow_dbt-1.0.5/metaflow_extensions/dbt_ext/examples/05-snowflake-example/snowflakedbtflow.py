from metaflow import step, FlowSpec, dbt, secrets, conda_base
from config import DBT_PROFILES, SECRET_SRC


@conda_base(packages={"dbt-snowflake": ">1.7.0"})
class SnowflakeDBTFlow(FlowSpec):
    @dbt(
        command="seed",
        project_dir="./jaffle_shop",
        profiles=DBT_PROFILES,
    )
    @secrets(sources=SECRET_SRC)
    @step
    def start(self):
        # jaffle_shop example needs to be seeded before 'dbt run' works for its models.
        print("Seeded jaffle_shop")
        self.next(self.jaffle_models)

    @dbt(project_dir="./jaffle_shop", profiles=DBT_PROFILES, generate_docs=True)
    @secrets(sources=SECRET_SRC)
    @step
    def jaffle_models(self):
        print("jaffle_shop DBT run: staging")
        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    SnowflakeDBTFlow()
