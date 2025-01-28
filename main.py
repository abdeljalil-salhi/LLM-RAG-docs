from sys import argv

from app.populate_db import PopulateDB

if __name__ == "__main__":
    if len(argv) > 1:
        if argv[1] in ["--populate", "-p"]:
            populator = PopulateDB()
            populator.run()
