from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class MtaxTime:
    def __init__(self, timezone: str = 'Etc/Greenwich') -> None:
        self.timezone: str = timezone
        try:
            self.tzinfo: ZoneInfo = ZoneInfo(self.timezone)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"Invalid timezone name: {self.timezone}") from exc
        self.now: datetime = datetime.now(self.tzinfo)

        self.year: int = self.now.year
        self.month: int = self.now.month
        self.day: int = self.now.day
        self.name: str = self.now.strftime('%a').upper()
        self.daynum_ofweek: int = self.now.weekday()
        self.daynum_ofyear: int = self.now.timetuple().tm_yday

        self.hour: str = f'{self.now.hour:02}'
        self.minute: str = f'{self.now.minute:02}'
        self.second: str = f'{self.now.second:02}'
        self.microsecond: int = self.now.microsecond
        self.millisecond: int = self.microsecond // 1000

        self.tzname: str = self.now.tzname()
        self.tzoffset: str = self.now.strftime('%z')

        self.date: str = f'{self.daynum_ofyear}/{self.year}'
        self.time: str = f'{self.hour}:{self.minute}:{self.second}.{self.microsecond}'

    def __repr__(self) -> str:
        r = (
            f'{self.year}, {self.month}, {self.day}, '
            f'{self.time}, {self.tzname}{self.tzoffset}')
        return f'montyalex.MtaxTime({r})'

    def __str__(self) -> str:
        return self.timestamp()

    def __format__(self, format_spec: str) -> str:
        return self.timestamp(format_spec)

    def timestamp(self, format = None):
        if format is None:
            return f'{self.tzname}/{self.name}-{self.date}T{self.time}{self.tzoffset}'
        return datetime.strftime(self.now, format)
