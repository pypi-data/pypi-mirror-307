# Simple DBT Flow

This example executes demonstrates how to execute two separate DBT projects in a single flow

# 

# Usage

Run the `./setup.sh` script and follow the instructions.

After editing the `config.py` values, you should be able to execute the flow with the following command
```sh
python dbtflow.py --environment conda run
```

Note: This flow tries to target a local database, so if you need to launch one, you can use the Docker Compose file provided along the examples

```sh
cd ..
docker-compose up
```