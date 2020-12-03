import re
import sys


def int_field(lower, upper, allow_padding=False):
    def validator(value):
        if not allow_padding and value.startswith("0"):
            return False

        try:
            value = int(value)
            return lower <= value <= upper
        except ValueError:
            return False

    return validator

def valid_height(height):
    value, unit = (height[:-2], height[-2:])

    if unit == "cm":
        validator = int_field(150, 193, allow_padding=True)
    elif unit == "in":
        validator = int_field(59, 76, allow_padding=True)
    else:
        return False

    return validator(value)


def regex_field(regex):
    regex = re.compile(regex)
    return lambda value: regex.fullmatch(value) is not None


def choice_field(options):
    options = set(options)
    return lambda value: value in options


class Passport:

    MANDATORY_FIELDS = [
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
    ]

    VALID_EYE_COLOURS = [
        "amb",
        "blu",
        "brn",
        "gry",
        "grn",
        "hzl",
        "oth",
    ]

    FIELD_VALIDATORS = {
        "byr": int_field(1920, 2002),
        "iyr": int_field(2010, 2020),
        "eyr": int_field(2020, 2030),
        "hgt": valid_height,
        "hcl": regex_field(r"#[0-9a-f]{6}"),
        "ecl": choice_field(VALID_EYE_COLOURS),
        "pid": regex_field(r"\d{9}"),
        "cid": regex_field(r".*")
    }

    def __init__(self, fields):
        self.fields = fields

    def is_valid(self):
        return self._mandatory_fields_present() and self._all_fields_valid()

    def _mandatory_fields_present(self):
        return all(field in self.fields for field in self.MANDATORY_FIELDS)

    def _all_fields_valid(self):
        return all(self._field_value_valid(name, value) for name, value in self.fields.items())

    @classmethod
    def _field_value_valid(cls, name, value):
        return cls.FIELD_VALIDATORS[name](value)


def read_passports(infile):
    for passport_text in infile.read().split("\n\n"):
        fields = dict(
            entry.split(":", 1) for entry in passport_text.split()
        )
        yield Passport(fields)


if __name__ == "__main__":
    passports = read_passports(sys.stdin)
    print(sum(1 for passport in passports if passport.is_valid()))