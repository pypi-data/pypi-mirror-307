from metaflow import step, FlowSpec, dbt, environment, conda_base
from config import DBT_PROFILES

ENVS = {"username": "postgres", "password": "postgres"}


@conda_base(packages={"dbt-postgres": ">=1.7.0"})
class DBTFlow(FlowSpec):
    @step
    def start(self):
        print("Start step for debugging")
        self.next(self.dbt_project, self.jaffle_seed)

    @environment(vars=ENVS)
    @dbt(
        project_dir="./dbt_project",
        profiles=DBT_PROFILES,
        generate_docs=True,
    )
    @step
    def dbt_project(self):
        print("dbt_project DBT run")
        self.next(self.join)

    @environment(vars=ENVS)
    @dbt(command="seed", project_dir="./jaffle_shop", profiles=DBT_PROFILES)
    @step
    def jaffle_seed(self):
        # jaffle_shop example needs to be seeded before 'dbt run' works for its models.
        print("Seeded jaffle_shop")
        self.next(self.jaffle_models)

    @environment(vars=ENVS)
    @dbt(
        project_dir="./jaffle_shop",
        profiles=DBT_PROFILES,
        generate_docs=True,
    )
    @step
    def jaffle_models(self):
        print("jaffle_shop DBT run: models")
        self.next(self.join)

    @step
    def join(self, inputs):
        print("join DBT runs")
        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    DBTFlow()
