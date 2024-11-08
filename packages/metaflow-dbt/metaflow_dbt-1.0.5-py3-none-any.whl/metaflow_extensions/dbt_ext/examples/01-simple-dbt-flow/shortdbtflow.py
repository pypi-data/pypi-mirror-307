from metaflow import step, FlowSpec, dbt, environment, secrets
from config import DBT_PROFILES, SECRET_SRC, HOST_ENV

ENVS = {"username": "postgres", "password": "postgres"}


class DBTFlow(FlowSpec):
    @step
    def start(self):
        print("Start step for debugging")
        self.next(self.jaffle_seed)

    @secrets(sources=SECRET_SRC)
    @environment(vars=HOST_ENV)
    @dbt(command="seed", project_dir="./jaffle_shop", profiles=DBT_PROFILES)
    @step
    def jaffle_seed(self):
        # jaffle_shop example needs to be seeded before 'dbt run' works for its models.
        print("Seeded jaffle_shop")
        self.next(self.jaffle_staging)

    @secrets(sources=SECRET_SRC)
    @environment(vars=HOST_ENV)
    @dbt(
        models=["staging"],
        project_dir="./jaffle_shop",
        profiles=DBT_PROFILES,
    )
    @step
    def jaffle_staging(self):
        print("jaffle_shop DBT run: staging")
        self.next(self.jaffle_customers_orders)

    @secrets(sources=SECRET_SRC)
    @environment(vars=HOST_ENV)
    @dbt(
        models=["customers", "orders"],
        project_dir="./jaffle_shop",
        profiles=DBT_PROFILES,
    )
    @step
    def jaffle_customers_orders(self):
        print("jaffle_shop DBT run: customers,orders")
        self.next(self.end)

    @step
    def end(self):
        print("Done! 🏁")


if __name__ == "__main__":
    DBTFlow()
