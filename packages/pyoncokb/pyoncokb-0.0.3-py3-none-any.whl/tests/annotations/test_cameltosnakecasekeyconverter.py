"""Test CamelToSnakeCaseKeyConverter class."""

import unittest

from pyoncokb.annotations.cameltosnakecasekeyconverter import (
    CamelToSnakeCaseKeyConverter,
)


class CamelToSnakeCaseKeyConverterTestCase(unittest.TestCase):
    """Test CamelToSnakeCaseKeyConverter class."""

    def test_convert(self):
        """Test convert method."""
        camel_dict = {
            "myKey": "value",
            "nestedDict": {
                "anotherKey": "anotherValue",
                "innerNestedDict": {"yetAnotherKey": "yetAnotherValue"},
            },
        }
        snake_dict = CamelToSnakeCaseKeyConverter.convert(camel_dict)
        snake_dict_expected = {
            "my_key": "value",
            "nested_dict": {
                "another_key": "anotherValue",
                "inner_nested_dict": {"yet_another_key": "yetAnotherValue"},
            },
        }
        self.assertTrue(snake_dict == snake_dict_expected)
