# Pandas, DuckDB and DBT

This is an example of loading a Pandas dataframe to DuckDB and using the data as a sort of seed for driving further DBT models in a single Flow.

It includes the movie dataset from the Metaflow tutorials

## Setup

As DuckDB is a file based database, we need a mechanism to pass the created file from one Metaflow step to another before the actual task execution begins.
The example achieves this by mounting a PVC and storing the database file in it.

Run `./setup.sh` for initial setup and follow the instructions.

## Running

Run the flow with the following command

```sh
python duckdbflow.py --environment conda --package-suffixes=.csv run --with kubernetes
```


## Issues

If you encounter the following error with the flow

```
duckdb.duckdb.IOException: IO Error: Trying to read a database file with version number 43, but we can only read version 64.
The database file was created with DuckDB version v0.7.0 or v0.7.1.
```

Then the PVC has an existing DuckDB file that was created with an incompatible version.
You can clean up the old file from the PVC if necessary by supplying an additional `--cleanup=True` parameter to the flow command.
This will delete the DuckDB file before trying to perform any other operations.