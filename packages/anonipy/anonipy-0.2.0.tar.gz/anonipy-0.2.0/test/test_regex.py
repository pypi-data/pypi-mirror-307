import unittest

from anonipy.utils.regex import (
    regex_mapping,
    RegexMapping,
    REGEX_STRING,
    REGEX_INTEGER,
    REGEX_FLOAT,
    REGEX_DATE,
    REGEX_EMAIL_ADDRESS,
    REGEX_PHONE_NUMBER,
    REGEX_WEBSITE_URL,
)
from anonipy.constants import ENTITY_TYPES


# =====================================
# Test Cases
# =====================================

TEST_CASES = [
    {"value": "string", "entity": ENTITY_TYPES.STRING, "regex": REGEX_STRING},
    {
        "value": "integer",
        "entity": ENTITY_TYPES.INTEGER,
        "regex": REGEX_INTEGER,
    },
    {"value": "float", "entity": ENTITY_TYPES.FLOAT, "regex": REGEX_FLOAT},
    {"value": "date", "entity": ENTITY_TYPES.DATE, "regex": REGEX_DATE},
    {
        "value": "email",
        "entity": ENTITY_TYPES.EMAIL,
        "regex": REGEX_EMAIL_ADDRESS,
    },
    {
        "value": "phone_number",
        "entity": ENTITY_TYPES.PHONE_NUMBER,
        "regex": REGEX_PHONE_NUMBER,
    },
    {
        "value": "website_url",
        "entity": ENTITY_TYPES.WEBSITE_URL,
        "regex": REGEX_WEBSITE_URL,
    },
    {"value": "custom", "entity": ENTITY_TYPES.CUSTOM, "regex": ".*"},
    {"value": "test", "entity": "test", "regex": ".*"},
]


# =====================================
# Test Entity
# =====================================


class TestRegex(unittest.TestCase):

    def test_init(self):
        self.assertEqual(regex_mapping.__class__, RegexMapping)
        self.assertEqual(hasattr(regex_mapping, "regex_mapping"), True)

    def test_regex_mapping(self):

        for test_case in TEST_CASES:
            self.assertEqual(regex_mapping[test_case["entity"]], test_case["regex"])
            self.assertEqual(
                regex_mapping[test_case["value"]], regex_mapping[test_case["entity"]]
            )


if __name__ == "__main__":
    unittest.main()
