from enum import Enum
from rich.table import Table

from montyalex.console_tools import richconsole
from montyalex.fs_tools import cancel
from montyalex.time_tools import func_time
from montyalex.typing_tools import Any, Generator


print = richconsole.print


class BaseName(Enum):
    BINARY = 2
    TERNARY = 3
    QUATERNARY = 4
    QUINARY = 5
    SENARY = 6
    SEPTENARY = 7
    OCTAL = 8
    NONARY = 9
    DECIMAL = 10
    UNDECIMAL = 11
    DUODECIMAL = 12
    TRIDECIMAL = 13
    TETRADECIMAL = 14
    PENTADECIMAL = 15
    HEXADECIMAL = 16
    VIGESIMAL = 20
    DUOVIGESIMAL = 22
    TETRAVIGESIMAL = 24
    TRIGESIMAL = 30
    DUOTRIGESIMAL = 32
    TETRAGESIMAL = 40
    QUADRAGESIMAL = 48
    SEXAGESIMAL = 60
    TETRASEXAGESIMAL = 64
    CENTESIMAL = 100

    @classmethod
    def get_name(cls, base: int) -> str:
        for name, value in cls.__members__.items():
            if value.value == base:
                return name.lower()
        return "unknown"

class DigitPreset:
    def __init__(self, digit: int, preset: str) -> None:
        self.digit = digit
        self.preset = preset

    def __str__(self) -> str:
        return self.preset

    def generate_base_dict(self, base: int) -> dict[str, Any]:
        chars = (
            "0123456789"
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "!@#$%^&*()-=_+[]{}|;:'\",.<>?\\/"
            "±§µ¢£€¥¤©®™✓✗♥♦♣♠♪♫◊")
        max_value = base ** self.digit
        base_dict = {}
        for i in range(max_value):
            val = ""
            num = i
            while num > 0:
                val = chars[num % base] + val
                num //= base
            base_dict[val.zfill(self.digit)] = i
        return base_dict

    def __call__(self, base: int, zero_exclusive=True) -> dict[str, Any]:
        base_dict = self.generate_base_dict(base)
        if zero_exclusive:
            base_dict = {k: v for k, v in base_dict.items() if k != ("0" * self.digit)}
        return base_dict

    @staticmethod
    def display_range_with_decimal(base_dict: dict) -> None:
        for base_value, decimal_value in base_dict.items():
            print(f"{base_value} = {decimal_value}")

    @staticmethod
    def range_length(
        dict_length: int, range_name: str, show_wz_range: bool = False) -> tuple[str, str, str]:
        if show_wz_range:
            return "(%%)", f"{range_name} size", f"[blue1]±{dict_length}[/]"
        return "(++)", f"{range_name} size", f"[cyan]±{dict_length}[/]"

    def _get_base_dict(self, base: int, show_wz_range: bool = False) -> dict:
        base_dict = self(base, not show_wz_range)
        return base_dict

    def base_dict_length(self, base: int, show_wz_range: bool = False) -> int:
        length = base ** self.digit
        if show_wz_range:
            length += 1
        return length

    def set_of_base(self, base: int, show_wz_range: bool = False) -> set[str]:
        base_dict = self._get_base_dict(base, show_wz_range)
        return set(base_dict.keys())

    def ul_of_base(self, base: int, show_wz_range: bool = False) -> list[str]:
        return list(self.set_of_base(base, show_wz_range))

    def ol_of_base(self, base: int, show_wz_range: bool = False) -> list[str]:
        return sorted(self.ul_of_base(base, show_wz_range))

class DoubleDigitPreset(DigitPreset):
    def __init__(self) -> None:
        super().__init__(2, 'Double')

class TripleDigitPreset(DigitPreset):
    def __init__(self) -> None:
        super().__init__(3, 'Triple')

class QuadrupleDigitPreset(DigitPreset):
    def __init__(self) -> None:
        super().__init__(4, 'Quadruple')

class QuintupleDigitPreset(DigitPreset):
    def __init__(self) -> None:
        super().__init__(5, 'Quintuple')

class SextupleDigitPreset(DigitPreset):
    def __init__(self) -> None:
        super().__init__(6, 'Sextuple')

class SeptupleDigitPreset(DigitPreset):
    def __init__(self) -> None:
        super().__init__(7, 'Septuple')

class OctupleDigitPreset(DigitPreset):
    def __init__(self) -> None:
        super().__init__(8, 'Octuple')

class NonupleDigitPreset(DigitPreset):
    def __init__(self) -> None:
        super().__init__(9, 'Nonuple')

class DecupleDigitPreset(DigitPreset):
    def __init__(self) -> None:
        super().__init__(10, 'Decuple')


class Preset:
    digit_default_dict = {
        "single": DigitPreset(1, 'Single'),
        "double": DoubleDigitPreset(),
        "triple": TripleDigitPreset(),
        "quadruple": QuadrupleDigitPreset(),
        "quintuple": QuintupleDigitPreset(),
        "sextuple": SextupleDigitPreset(),
        "septuple": SeptupleDigitPreset(),
        "octuple": OctupleDigitPreset(),
        "nonuple": NonupleDigitPreset(),
        "decuple": DecupleDigitPreset()
    }

    def __init__(
        self,
        kind: str,
        *,
        name: str = None,
        formatted: str | bool = False,
        numbase: int = 10) -> None:
        self.kind = kind

        self.name = name
        self.format = formatted
        self.numbase = numbase
        self.preset: DigitPreset | object = None

        if self.kind == 'digit':
            if self.name is None:
                self.name = 'triple'
            self.preset = self.digit_default_dict[self.name]

    def __len__(self) -> int:
        if self.kind == 'digit':
            return self.preset.base_dict_length(self.numbase, False)
        return 0

    def _get_base_dict(self, base: int, show_wz_range: bool = False) -> dict:
        base_dict = self.digit_default_dict[self.name](base, not show_wz_range)
        return base_dict

    def _table_items_generator(self, show_wz_range: bool) -> Generator[tuple[dict, int], Any, None]:
        base_dict = self._get_base_dict(self.numbase, show_wz_range)
        yield base_dict

    @func_time('took; to generate')
    def table(self, show_wz_range: bool = False) -> Table:
        target_base_name = BaseName.get_name(self.numbase)
        rows = []
        for base_dict in self._table_items_generator(show_wz_range):
            rows.append(self.preset.range_length(len(base_dict), target_base_name, show_wz_range))
        t = Table(
            show_header=False,
            pad_edge=False,
            highlight=True,
            title=f'{self.name.capitalize()} Digit Range',
            title_style="bold turquoise2",
            title_justify="left"
        )
        t.add_column("1", no_wrap=True)
        t.add_column("2", no_wrap=True)
        t.add_column("3", justify="right", no_wrap=True)
        for row in rows:
            t.add_row(*row)
        return t

binary_single = Preset('digit', name='single', numbase=2)
binary_double = Preset('digit', name='double', numbase=2)
binary_triple = Preset('digit', name='triple', numbase=2)
binary_quadruple = Preset('digit', name='quadruple', numbase=2)
binary_quintuple = Preset('digit', name='quintuple', numbase=2)
binary_sextuple = Preset('digit', name='sextuple', numbase=2)
binary_septuple = Preset('digit', name='septuple', numbase=2)
binary_octuple = Preset('digit', name='octuple', numbase=2)
binary_nonuple = Preset('digit', name='nonuple', numbase=2)
binary_decuple = Preset('digit', name='decuple', numbase=2)

ternary_single = Preset('digit', name='single', numbase=3)
ternary_double = Preset('digit', name='double', numbase=3)
ternary_triple = Preset('digit', name='triple', numbase=3)
ternary_quadruple = Preset('digit', name='quadruple', numbase=3)
ternary_quintuple = Preset('digit', name='quintuple', numbase=3)
ternary_sextuple = Preset('digit', name='sextuple', numbase=3)
ternary_septuple = Preset('digit', name='septuple', numbase=3)
ternary_octuple = Preset('digit', name='octuple', numbase=3)
ternary_nonuple = Preset('digit', name='nonuple', numbase=3)
ternary_decuple = Preset('digit', name='decuple', numbase=3)

quaternary_single = Preset('digit', name='single', numbase=4)
quaternary_double = Preset('digit', name='double', numbase=4)
quaternary_triple = Preset('digit', name='triple', numbase=4)
quaternary_quadruple = Preset('digit', name='quadruple', numbase=4)
quaternary_quintuple = Preset('digit', name='quintuple', numbase=4)
quaternary_sextuple = Preset('digit', name='sextuple', numbase=4)
quaternary_septuple = Preset('digit', name='septuple', numbase=4)
quaternary_octuple = Preset('digit', name='octuple', numbase=4)
quaternary_nonuple = Preset('digit', name='nonuple', numbase=4)
quaternary_decuple = Preset('digit', name='decuple', numbase=4)

quinary_single = Preset('digit', name='single', numbase=5)
quinary_double = Preset('digit', name='double', numbase=5)
quinary_triple = Preset('digit', name='triple', numbase=5)
quinary_quadruple = Preset('digit', name='quadruple', numbase=5)
quinary_quintuple = Preset('digit', name='quintuple', numbase=5)
quinary_sextuple = Preset('digit', name='sextuple', numbase=5)
quinary_septuple = Preset('digit', name='septuple', numbase=5)
quinary_octuple = Preset('digit', name='octuple', numbase=5)
quinary_nonuple = Preset('digit', name='nonuple', numbase=5)

senary_single = Preset('digit', name='single', numbase=6)
senary_double = Preset('digit', name='double', numbase=6)
senary_triple = Preset('digit', name='triple', numbase=6)
senary_quadruple = Preset('digit', name='quadruple', numbase=6)
senary_quintuple = Preset('digit', name='quintuple', numbase=6)
senary_sextuple = Preset('digit', name='sextuple', numbase=6)
senary_septuple = Preset('digit', name='septuple', numbase=6)
senary_octuple = Preset('digit', name='octuple', numbase=6)
senary_nonuple = Preset('digit', name='nonuple', numbase=6)

septenary_single = Preset('digit', name='single', numbase=7)
septenary_double = Preset('digit', name='double', numbase=7)
septenary_triple = Preset('digit', name='triple', numbase=7)
septenary_quadruple = Preset('digit', name='quadruple', numbase=7)
septenary_quintuple = Preset('digit', name='quintuple', numbase=7)
septenary_sextuple = Preset('digit', name='sextuple', numbase=7)
septenary_septuple = Preset('digit', name='septuple', numbase=7)
septenary_octuple = Preset('digit', name='octuple', numbase=7)

octal_single = Preset('digit', name='single', numbase=8)
octal_double = Preset('digit', name='double', numbase=8)
octal_triple = Preset('digit', name='triple', numbase=8)
octal_quadruple = Preset('digit', name='quadruple', numbase=8)
octal_quintuple = Preset('digit', name='quintuple', numbase=8)
octal_sextuple = Preset('digit', name='sextuple', numbase=8)
octal_septuple = Preset('digit', name='septuple', numbase=8)

nonary_single = Preset('digit', name='single', numbase=9)
nonary_double = Preset('digit', name='double', numbase=9)
nonary_triple = Preset('digit', name='triple', numbase=9)
nonary_quadruple = Preset('digit', name='quadruple', numbase=9)
nonary_quintuple = Preset('digit', name='quintuple', numbase=9)
nonary_sextuple = Preset('digit', name='sextuple', numbase=9)
nonary_septuple = Preset('digit', name='septuple', numbase=9)

decimal_single = Preset('digit', name='single')
decimal_double = Preset('digit', name='double')
decimal_triple = Preset('digit', name='triple')
decimal_quadruple = Preset('digit', name='quadruple')
decimal_quintuple = Preset('digit', name='quintuple')
decimal_sextuple = Preset('digit', name='sextuple')
decimal_septuple = Preset('digit', name='septuple')
decimal_octuple = Preset('digit', name='octuple')
decimal_nonuple = Preset('digit', name='nonuple')
decimal_decuple = Preset('digit', name='decuple')

duodecimal_single = Preset('digit', name='single', numbase=12)
duodecimal_double = Preset('digit', name='double', numbase=12)
duodecimal_triple = Preset('digit', name='triple', numbase=12)
duodecimal_quadruple = Preset('digit', name='quadruple', numbase=12)
duodecimal_quintuple = Preset('digit', name='quintuple', numbase=12)
duodecimal_sextuple = Preset('digit', name='sextuple', numbase=12)

hexadecimal_single = Preset('digit', name='single', numbase=16)
hexadecimal_double = Preset('digit', name='double', numbase=16)
hexadecimal_triple = Preset('digit', name='triple', numbase=16)
hexadecimal_quadruple = Preset('digit', name='quadruple', numbase=16)
hexadecimal_quintuple = Preset('digit', name='quintuple', numbase=16)

base32_single = Preset('digit', name='single', numbase=32)
base32_double = Preset('digit', name='double', numbase=32)
base32_triple = Preset('digit', name='triple', numbase=32)
base32_quadruple = Preset('digit', name='quadruple', numbase=32)

base64_single = Preset('digit', name='single', numbase=64)
base64_double = Preset('digit', name='double', numbase=64)
base64_triple = Preset('digit', name='triple', numbase=64)

LPR: dict[str, Preset] = {
    'single': binary_single,
    'double': binary_double,
    'triple': binary_triple,
    'quadruple': binary_quadruple,
    'quintuple': binary_quintuple,
    'sextuple': binary_sextuple,
    'septuple': binary_septuple,
    'octuple': binary_octuple,
    'nonuple': binary_nonuple,
    'decuple': binary_decuple
}
GPR: dict[str, Preset] = {
    'single': base64_single,
    'double': base64_double,
    'triple': base64_triple,
    'quadruple': base32_quadruple,
    'quintuple': hexadecimal_quintuple,
    'sextuple': duodecimal_sextuple,
    'septuple': nonary_septuple,
    'octuple': septenary_octuple,
    'nonuple': senary_nonuple,
    'decuple': quaternary_decuple
}
MCR: dict[str, Preset] = {
    'single': decimal_single,
    'double': decimal_double,
    'triple': decimal_triple,
    'quadruple': decimal_quadruple,
    'quintuple': decimal_quintuple,
    'sextuple': decimal_sextuple,
    'septuple': decimal_septuple,
    'octuple': decimal_octuple,
    'nonuple': decimal_nonuple,
    'decuple': decimal_decuple
}
# ---------------------------------------------------------------------------
# | Example Usage
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    def main():
        digits = (
            '(single|double|triple|quadruple|quintuple|'
            'sextuple|septuple|octuple|nonuple|decuple)')
        digits_input = input(
            f'How many digits should be used? {digits}: ').lower().strip()
        base = input('Which base should be used? (10:default|2-64): ').strip()
        if base == '' or not base.isnumeric():
            base = 10
        else:
            base = int(base)
            if base > 64 or base < 2:
                print(f'Base {base} not allowed')
                cancel()

        double_up_input = input(
            'Do you want to double the folder name? (a=aa, y|N): ').lower().strip()
        zeroith_input = input('Do you want to include a zeroith folder? (y|N): ').lower().strip()
        _preset = MCR[f'{digits_input}'].preset.ol_of_base(base, bool(zeroith_input == 'y'))
        for b in _preset:
            print(b)
            if double_up_input == 'y':
                print(f'{b}_{b}')
        if double_up_input == 'y':
            print(f'len({len(_preset) * 2})')
        else:
            print(f'len({len(_preset)})')
