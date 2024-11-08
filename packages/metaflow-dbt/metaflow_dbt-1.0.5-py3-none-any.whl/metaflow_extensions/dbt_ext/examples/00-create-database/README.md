# Utility flow; Create database

This flow is meant as an utility if you happen to have a database instance that is not easily accessible from the outside,
and you are missing the necessary database from the instance.

# Usage

Run the setup script `./setup.sh`

After editing the `config.py`, you should be able to run the flow, which will try to create the missing database on the instance if the IAM role has sufficient permissions.

```sh
python createdbflow.py --environment conda run --with kubernetes
```