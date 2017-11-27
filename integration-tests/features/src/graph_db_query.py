"""Simple wrapper over Gremlin language."""


class Query:
    """Simple wrapper over Gremlin language."""

    def __init__(self):
        """Initialize the object with a start of query."""
        self.query = 'g.V()'

    def has(self, name, value):
        """Add (another) 'has' clause into the query."""
        self.query += '.has("{name}", "{value}")'.format(name=name, value=value)
        return self

    def count(self):
        """Add a 'count' clause at the end of the query."""
        self.query += '.count()'
        return self

    def __repr__(self):
        """Return an official represenation of the object, same as __str__ here."""
        return self.query

    def ___str___(self):
        """Return an informal represenation of the object, same as __repr__ here."""
        return self.query
