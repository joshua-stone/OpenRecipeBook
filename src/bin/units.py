from re import search

class Unit:
    def __init__(self, type, coefficient):
        self.type = type
        self.coefficient = coefficient

    def __mul__(self, multiplier):
        return Unit(type, self.coefficient * multiplier)

class AmountWithUnit:
    PATTERN = r"(?P<magnitude>\d+(?:\.\d+)?)[ ]?(?P<unit>.+)?"

    def __init__(self, amount, unit_text, unit):
        self.amount = amount
        self.unit_text = unit_text
        self.unit = unit

    def is_unit_supported(self):
        return self.unit != UNSUPPORTED_UNIT

MILLIGRAM = Unit('mass', 1)
GRAM      = MILLIGRAM * 1000
KILOGRAM  = GRAM * 1000
OUNCE     = MILLIGRAM * 28349.5231
POUND     = OUNCE * 16

MILLILITER  = Unit('volume', 1)
LITER       = MILLILITER * 1000
TEASPOON    = MILLILITER * 4.92892159
TABLESPOON  = TEASPOON * 3
FLUID_OUNCE = MILLILITER * 28.413075

NO_UNIT          = Unit('no unit', 1)
SERVING          = Unit('serving', 1)
UNSUPPORTED_UNIT = Unit('unsupported', 1)

UNIT_MAPPINGS = {
    # Mass
    'mg':         MILLIGRAM,
    'milligram':  MILLIGRAM,
    'milligrams': MILLIGRAM,
    'g':          GRAM,
    'gram':       GRAM,
    'grams':      GRAM,
    'kg':         KILOGRAM,
    'kilogram':   KILOGRAM,
    'kilograms':  KILOGRAM,
    'oz':         OUNCE,
    'ounce':      OUNCE,
    'ounces':     OUNCE,
    'lb':         POUND,
    'pound':      POUND,
    'pounds':     POUND,

    # Volume
    'mL':           MILLILITER,
    'milliliter':   MILLILITER,
    'milliliters':  MILLILITER,
    'L':            LITER,
    'liter':        LITER,
    'liters':       LITER,
    'tsp':          TEASPOON,
    'teaspoon':     TEASPOON,
    'teaspoons':    TEASPOON,
    'tbsp':         TABLESPOON,
    'tablespoon':   TABLESPOON,
    'tablespoons':  TABLESPOON,
    'floz':         OUNCE,
    'fluid ounce':  OUNCE,
    'fluid ounces': OUNCE,

    # Other
    'serving':  SERVING,
    'servings': SERVING
}

def get_unit_by_text(unit_text, default_unit = NO_UNIT):
    if unit_text is None:
        return default_unit

    return UNIT_MAPPINGS.get(unit_text, UNSUPPORTED_UNIT)

def parse_amount_with_unit(input_text, **kwargs):
    m = search(AmountWithUnit.PATTERN, str(input_text))

    if m:
        magnitude = float(m.group('magnitude'))
        unit_text = m.group('unit')

        return AmountWithUnit(magnitude, unit_text, get_unit_by_text(unit_text, **kwargs))
    else:
        return None
