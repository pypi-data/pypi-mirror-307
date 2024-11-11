import os


def get_env_or_raise(env_name: str):
    value = os.getenv(env_name)
    if not value:
        raise ValueError(f"Environment variable [{env_name}] is not set.")
    return value
