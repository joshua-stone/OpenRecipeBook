from re import search
from pint import UnitRegistry

pattern = r"(?P<magnitude>\d+(?:\.\d+)?)[ ]?(?P<unit>.+)?"

ureg = UnitRegistry()
AmountWithUnit = ureg.Quantity

ureg.define('none = 1')
ureg.define('serving = 1')

def parse_amount_with_unit(unit_text, default_unit = 'none'):
    m = search(pattern, str(unit_text))

    if m:
        magnitude = float(m.group('magnitude'))
        unit_text = m.group('unit')

        return AmountWithUnit(magnitude, unit_text or default_unit)
    else:
        return None
