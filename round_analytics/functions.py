import os
from dotenv import load_dotenv


load_dotenv()


def check_env(*args: str):
    for name in args:
        if os.getenv(name) is None:
            raise KeyError(
                f"No environment variable with name {name}. "
                f"{args} must be specified."
            )
