import re
import sys


class IntValidator:
    def __init__(self, lower, upper, allow_padding=True):
        self._lower = lower
        self._upper = upper
        self._allow_padding = allow_padding

    def __call__(self, value):
        if not self._allow_padding and value.startswith("0"):
            return False

        try:
            value = int(value)
            return self._lower <= value <= self._upper
        except ValueError:
            return False


class HeightValidator:
    def __call__(self, height):
        value, unit = (height[:-2], height[-2:])

        if unit == "cm":
            validator = IntValidator(150, 193)
        elif unit == "in":
            validator = IntValidator(59, 76)
        else:
            return False

        return validator(value)


class RegexValidator:
    def __init__(self, regex):
        self._regex = re.compile(regex)

    def __call__(self, value):
        return self._regex.fullmatch(value) is not None


class ChoiceValidator:
    def __init__(self, options):
        self._options = set(options)

    def __call__(self, value):
        return value in self._options


class AnyValidator:
    def __call__(self, value):
        return True


class NoneValidator:
    def __call__(self, value):
        return False


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
        "byr": IntValidator(1920, 2002, allow_padding=False),
        "iyr": IntValidator(2010, 2020, allow_padding=False),
        "eyr": IntValidator(2020, 2030, allow_padding=False),
        "hgt": HeightValidator(),
        "hcl": RegexValidator(r"#[0-9a-f]{6}"),
        "ecl": ChoiceValidator(VALID_EYE_COLOURS),
        "pid": RegexValidator(r"\d{9}"),
        "cid": AnyValidator()
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
        validator = cls.FIELD_VALIDATORS.get(name, NoneValidator())
        return validator(value)


def read_passports(infile):
    for passport_text in infile.read().split("\n\n"):
        fields = dict(
            entry.split(":", 1) for entry in passport_text.split()
        )
        yield Passport(fields)


if __name__ == "__main__":
    passports = read_passports(sys.stdin)
    print(sum(1 for passport in passports if passport.is_valid()))