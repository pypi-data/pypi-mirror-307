# The secret source should provide the following environment variables
# account_id
# username
# password
# role
# dbname
# whname
# schema
SECRET_SRC = ["replace-with-secret-source"]

DBT_PROFILES = {
    "jaffle_shop": {
        "target": "dev",
        "outputs": {
            "dev": {
                "type": "snowflake",
                "account": "{{ env_var('account_id') }}",
                # User/password auth
                "user": "{{ env_var('username') }}",
                "password": "{{ env_var('password') }}",
                "role": "{{ env_var('role') }}",
                "database": "{{ env_var('dbname') }}",
                "warehouse": "{{ env_var('whname') }}",
                "schema": "{{ env_var('schema') }}",
                "threads": 1,
                "client_session_keep_alive": False,
                "query_tag": "mf-dbt-ext",
                # optional
                "connect_retries": 0,  # default 0
                "connect_timeout": 10,  # default: 10
                "retry_on_database_errors": False,  # default: false
                "retry_all": False,  # default: false
                "reuse_connections": False,  # default: false (available v1.4+)}
            }
        },
    }
}
