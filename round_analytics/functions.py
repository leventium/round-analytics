import os


def check_env(*args: str):
    for name in args:
        if os.getenv(name) is None:
            raise KeyError(
                f"No environment variable with name {name}. "
                f"{args} must be specified."
            )


def get_content_from_dir(path: str) -> dict[str, bytes]:
    path = path.strip("/")
    res = {}
    filenames = [
        f"{path}/{f}" for f in os.listdir(f"{path}/")
        if os.path.isfile(f"{path}/{f}")
    ]
    for filename in filenames:
        with open(filename, "r") as file:
            res[filename.split("/")[1]] = file.read()
    return res
