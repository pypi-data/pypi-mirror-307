"""Convert dict key from camel case to snake case."""


class CamelToSnakeCaseKeyConverter:
    """Convert dict key from camel case to snake case."""
    @staticmethod
    def camel_to_snake_case(key):
        """Convert a single camel case string to snake case."""
        result = [key[0].lower()]
        for char in key[1:]:
            if char.isupper():
                result.extend(["_", char.lower()])
            else:
                result.append(char)
        return "".join(result)

    @staticmethod
    def convert(obj):
        """Recursively convert keys in a dictionary to snake case."""
        if isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                new_key = CamelToSnakeCaseKeyConverter.camel_to_snake_case(key)
                new_value = CamelToSnakeCaseKeyConverter.convert(value)
                new_dict[new_key] = new_value
            return new_dict
        elif isinstance(obj, list):
            return [CamelToSnakeCaseKeyConverter.convert(item) for item in obj]
        else:
            return obj
