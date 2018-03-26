"""Module with various utility functions."""


def store_list(filename, a_list):
    """Store the list into a file."""
    with open(filename, "w") as fout:
        for item in a_list:
            fout.write(item)
            fout.write("\n")


def read_list(filename):
    """Read list from file."""
    with open(filename, "r") as fin:
        items = fin.readlines()
        return [item.strip() for item in items]
