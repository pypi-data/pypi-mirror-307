import typing as tp

import datetime as dt

class Date(object):
    
    def __init__(self,
                 year: int = dt.date.today().year,
                 month: int = dt.date.today().month,
                 day: int = dt.date.today().day) -> None:
        # Check if month is valid
        if not 1 <= month <= 12:
            raise ValueError(f"month '{month}' does not exist")
        
        # Check if day is valid
        days_per_month = [None, 31, None, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        days_per_month[2] = 29 if year % 4 == 0 else 28
        self.days_per_month = days_per_month
        
        if not 1 <= day <= self.days_per_month[month]:
            raise ValueError(f"day '{day}' of month '{month}' does not exist")
        
        self.year = year
        self.month = month
        self.day = day
    
    def __str__(self) -> str:
        """Represent a day in European format."""
        
        string = f"0{self.day}" if self.day < 10 else str(self.day)
        string += f"-0{self.month}" if self.month < 10 else f"-{self.month}"
        string += f"-{self.year}"
        return string
    
    def __repr__(self) -> str:
        return str(self)
    
    def __add__(self, days: int) -> tp.Self:
        """Add an arbitrary amount of days to a date."""
        
        if not isinstance(days, int):
            raise TypeError("unsupported operand type(s) for '+': "
                            f"'{type(self).__name__}' and '{type(days).__name__}'")
        
        result = Date(self.year, self.month, self.day)
        for day in range(days):
            result.day += 1
            
            # If month or day become too high, reset them to 1 and increase month or year
            if result.day > result.days_per_month[result.month]:
                result.day = 1
                result.month += 1
            
            if result.month > 12:
                result.month = 1
                result.year += 1
        
        return result
    
    def __sub__(self, days: int) -> tp.Self:
        """Subtracts an arbitrary amount of days from a date."""
        
        if not isinstance(days, int):
            raise TypeError("unsupported operand type(s) for '-': "
                            f"'{type(self).__name__}' and '{type(days).__name__}'")
        
        result = Date(self.year, self.month, self.day)
        for day in range(days):
            result.day -= 1
            
            # If day or month become too low, reset them to max and decrease month or year
            if result.day < 1:
                result.month -= 1
                if result.month < 1:
                    result.year -= 1
                    result.month = 12
                result.day = result.days_per_month[result.month]
        
        return result
    
    def __lt__(self, other: tp.Self) -> bool:
        if not isinstance(other, Date):
            raise TypeError("unsupported operand type(s) for '<': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        if self.year < other.year:
            return True
        elif self.year > other.year:
            return False
        elif self.month < other.month:
            return True
        elif self.month > other.month:
            return False
        elif self.day < other.day:
            return True
        else:
            return False
    
    def __le__(self, other: tp.Self) -> bool:
        if not isinstance(other, Date):
            raise TypeError("unsupported operand type(s) for '<=': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        return self == other or self < other
    
    def __eq__(self, other: tp.Self) -> bool:
        if not isinstance(other, Date):
            raise TypeError("unsupported operand type(s) for '==': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        return self.year == other.year and self.month == other.month and self.day == other.day

    def __ne__(self, other: tp.Self) -> bool:
        if not isinstance(other, Date):
            raise TypeError("unsupported operand type(s) for '!=': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        return self.year != other.year or self.month != other.month or self.day != other.day
    
    def __ge__(self, other: tp.Self) -> bool:
        if not isinstance(other, Date):
            raise TypeError("unsupported operand type(s) for '>=': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        return self == other or self > other
    
    def __gt__(self, other: tp.Self) -> bool:
        if not isinstance(other, Date):
            raise TypeError("unsupported operand type(s) for '>': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        if self.year > other.year:
            return True
        elif self.year < other.year:
            return False
        elif self.month > other.month:
            return True
        elif self.month < other.month:
            return False
        elif self.day > other.day:
            return True
        else:
            return False
    
    def difference(self, other: tp.Self) -> int:
        if not isinstance(other, Date):
            raise TypeError("unsupported operand type(s) for difference: "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        newest = max(self, other)
        oldest = min(self, other)
        
        # Iteratively check when oldest date + x is equal to newest
        x = 0
        while oldest + x != newest:
            x += 1
        
        return x
