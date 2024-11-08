# Remote DBT Flow

This example is a follow-up on the previous, where we execute the DBT models remotely, targeting a remote database.

# 

# Usage

Run the `./setup.sh` script and follow the instructions.

For our example we use AWS Secrets Manager for storing credentials to an RDS Postgres instance. You need to replace the values in `config.py` with the correct secret key, and db host. When this is done, the following flow should execute successfully.

```sh
python remotedbtflow.py --environment conda run --with kubernetes
```

the flow should work just as well with `batch`, `step-functions` and `argo-workflow`

Alternatively you can define a base Docker image that has the necessary requirements for executing DBT. You can try using the official DBT images as follows:

```sh
export METAFLOW_DEFAULT_CONTAINER_REGISTRY="ghcr.io/dbt-labs"
export METAFLOW_DEFAULT_CONTAINER_IMAGE="dbt-postgres:1.7.0"
python remotedbtflow.py run --with kubernetes
```