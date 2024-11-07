import os
from datetime import datetime
from ffquant.utils.Logger import stdout_log

__ALL__ = ['MyCalendar']

class MyCalendar:
    def __init__(self):
        self.base_url = f"{os.environ.get('FINTECHFF_CALENDAR_BASE_URL', 'http://192.168.25.98')}"
        pass

    """
    Checks if a given stock symbol is tradable at a specific date and time.

    Parameters:
        symbol (str): The stock symbol to check.
        dt (str): The date and time(Hong Kong timezone) to check. Format: 'YYYY-mm-dd HH:MM:SS'.

    Returns:
        bool: True if the symbol is tradable, False otherwise.
    """
    def isSymbolTradable(self, symbol: str, dt: str):
        broker = None
        if str(symbol).__contains__('@'):
            symbol, broker = symbol.split('@')

        # futu strategy is running on CAPITALCOM:HK50 data feed. Actual exchange time should be determined by symbol HKEX:HSI1!
        if str(symbol).upper() == 'CAPITALCOM:HK50' and broker is not None and str(broker).lower() == 'futu':
            symbol = 'HKEX:HSI1!'

        dtime = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        if str(symbol).upper() == 'CAPITALCOM:HK50':
            return True
        elif str(symbol).upper() == 'HKEX:HSI1!':
            morning_start_dt = dtime.replace(hour=9, minute=30, second=0, microsecond=0)
            morning_end_dt = dtime.replace(hour=12, minute=0, second=0, microsecond=0)

            afternoon_start_dt = dtime.replace(hour=13, minute=0, second=0, microsecond=0)
            afternoon_end_dt = dtime.replace(hour=16, minute=0, second=0, microsecond=0)
            return (dtime >= morning_start_dt and dtime < morning_end_dt) or (dtime >= afternoon_start_dt and dtime < afternoon_end_dt)
        return True


if __name__ == "__main__":
    calendar = MyCalendar()
    for hour in range(24):
        for minute in range(60):
            dt = f'2024-10-29 {hour:02d}:{minute:02d}:00'
            stdout_log(dt + ": " + ("Tradable" if calendar.isSymbolTradable('CAPITALCOM:HK50@tv', dt) else "Untradable"))