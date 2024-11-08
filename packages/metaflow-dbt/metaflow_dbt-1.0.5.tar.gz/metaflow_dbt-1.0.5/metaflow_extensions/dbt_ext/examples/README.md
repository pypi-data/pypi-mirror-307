# DBT Decorator usage examples

## Setup

The examples require valid DBT projects to be present in order for the flows to run. You can bootstrap the required DBT projects by running
```sh
./setup.sh
```
which will create the following projects
- `examples/dbt_project`
- `examples/jaffle_shop`

along with a placeholder `config.py` which you can fill with further constants as needed.

Note: DBT version 1.7.0 is the minimum required version to support generating documentation as part of the flow with `generate_docs=True`