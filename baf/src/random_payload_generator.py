"""Generator of random payload for testing API."""

import string
import random


class RandomPayloadGenerator:
    """Generator of random payload for testing API."""

    def __init__(self):
        """Initialize the random payload generator."""
        self.iteration_deep = 0
        self.max_iteration_deep = 2
        self.max_dict_key_length = 10
        self.max_string_length = 20
        self.dict_key_characters = string.ascii_lowercase + string.ascii_uppercase + "_"
        self.string_value_characters = (string.ascii_lowercase + string.ascii_uppercase +
                                        "_" + string.punctuation + " ")

    def generate_random_string(self, n, uppercase=False, punctuations=False):
        """Generate random string of length=n."""
        prefix = random.choice(string.ascii_lowercase)
        mix = string.ascii_lowercase + string.digits

        if uppercase:
            mix += string.ascii_uppercase
        if punctuations:
            mix += string.punctuation

        suffix = ''.join(random.choice(mix) for _ in range(n - 1))
        return prefix + suffix

    def generate_random_key_for_dict(self, data):
        """Generate a string key to be used in dictionary."""
        existing_keys = data.keys()
        while True:
            new_key = self.generate_random_string(10)
            if new_key not in existing_keys:
                return new_key

    def generate_random_list(self, n):
        """Generate list filled in with random values."""
        return [self.generate_random_payload((int, str, float, bool, list, dict)) for i in range(n)]

    def generate_random_dict(self, n):
        """Generate dictionary filled in with random values."""
        dict_content = (int, str, list, dict)
        return {self.generate_random_string(10): self.generate_random_payload(dict_content)
                for i in range(n)}

    def generate_random_list_or_string(self):
        """Generate list filled in with random strings."""
        if self.iteration_deep < self.max_iteration_deep:
            self.iteration_deep += 1
            value = self.generate_random_list(5)
            self.iteration_deep -= 1
        else:
            value = self.generate_random_value(str)
        return value

    def generate_random_dict_or_string(self):
        """Generate dict filled in with random strings."""
        if self.iteration_deep < self.max_iteration_deep:
            self.iteration_deep += 1
            value = self.generate_random_dict(5)
            self.iteration_deep -= 1
        else:
            value = self.generate_random_value(str)
        return value

    def generate_random_value(self, type):
        """Generate one random value of given type."""
        generators = {
            str: lambda: self.generate_random_string(20, uppercase=True, punctuations=True),
            int: lambda: random.randrange(100000),
            float: lambda: random.random() * 100000.0,
            bool: lambda: bool(random.getrandbits(1)),
            list: lambda: self.generate_random_list_or_string(),
            dict: lambda: self.generate_random_dict_or_string()
        }
        generator = generators[type]
        return generator()

    def generate_random_payload(self, restrict_types=None):
        """Generate random payload with possibly restricted data types."""
        if restrict_types:
            types = restrict_types
        else:
            types = (str, int, float, list, dict, bool)

        selected_type = random.choice(types)

        return self.generate_random_value(selected_type)
