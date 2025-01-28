from sys import argv

from app.populate_db import PopulateDB


def check_argv(argument: str, argv: list[str]) -> bool:
    """
    Check if an argument is present in the command line arguments.
    """
    return argument in argv


if __name__ == "__main__":
    if len(argv) > 1:
        if check_argv("--populate", argv) or check_argv("-p", argv):
            if check_argv("--clear", argv) or check_argv("-c", argv):
                populator = PopulateDB(clear=True)
            else:
                populator = PopulateDB()
            populator.run()
