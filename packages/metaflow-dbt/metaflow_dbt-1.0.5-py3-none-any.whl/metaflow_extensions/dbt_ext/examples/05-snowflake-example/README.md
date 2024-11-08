# DBT on Snowflake with Metaflow

This example details how to run a DBT project on Snowflake with Metaflow.

## Setup

1. Run the bootstrapping script for initial setup

```sh
./setup.sh
```

This will clone the `jaffle_shop` DBT project and a barebones `config.py` with placeholder values

2. Create a new secret in AWS Secret Manager. The secret should have the following details that will be used in the `config.py` during runtime:

|key|description|
|--|--|
| account_id | Snowflake Account ID |
| username | Snowflake username that will perform the DBT operations |
| password | password for the user |
| role | Snowflake role that the user will assume |
| dbname | Snowflake database name |
| whname | Snowflake warehouse name |
| schema | Schema name |

If you plan to execute the flow remotely, grant the relevant resources permissions to access the secret as well.

3. Edit the `config.py`. You should only need to edit the `SECRET_SRC` value to the name of the secret you created

## Running the flow

Run the flow locally while authenticated with
```sh
python snowflakedbtflow.py --environment conda run
```

or remotely via

```sh
python snowflakedbtflow.py --environment conda run --with kubernetes
```