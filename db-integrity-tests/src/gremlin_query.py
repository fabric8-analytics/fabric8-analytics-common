"""Simple wrapper over Gremlin language."""


class GremlinQuery:
    """Simple wrapper over Gremlin language."""

    def __init__(self):
        """Initialize the object with a start of query."""
        self.query = 'g.V()'

    def has(self, name, value):
        """Add (another) 'has' clause into the query."""
        self.query += '.has("{name}", "{value}")'.format(name=name, value=value)
        return self

    def out(self, name):
        """Add an 'out' clause into the query."""
        self.query += '.out("{name}")'.format(name=name)
        return self

    def valueMap(self):
        """Append a clause to retrieve map of values to the query."""
        self.query += '.valueMap()'
        return self

    def count(self):
        """Add a 'count' clause at the end of the query."""
        self.query += '.count()'
        return self

    def first(self):
        """Append a clause to get the first result from a list."""
        self.query += '[0]'
        return self

    def value(self, value):
        """Append a clause to read the given value from the dictionary."""
        self.query += '.value("{value}")'.format(value=value)
        return self

    def __repr__(self):
        """Return an official represenation of the object, same as __str__ here."""
        return self.query

    def ___str___(self):
        """Return an informal represenation of the object, same as __repr__ here."""
        return self.query
