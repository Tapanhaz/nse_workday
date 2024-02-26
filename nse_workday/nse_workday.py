

'''
;description: Code to calculate days based on NSE Holidays
:author: Tapan Hazarika
:license: MIT
'''
__author__ = "____Tapan Hazarika____"

import os
import pickle
import logging
import calendar
import requests
import warnings
from functools import lru_cache
from datetime import (
    date, 
    time,
    datetime, 
    timedelta 
)
from typing import (
    List, 
    Type, 
    Union, 
    Literal,
    NewType 
)

logging.getLogger(__name__)

DateFormat = NewType(name="%d-%m-%Y", tp=str)

lib_path = os.path.dirname(__file__)

@lru_cache(maxsize=None)
def __get_holylist() -> List[datetime]:
    try:
        file_path = os.path.join(lib_path, "hlist.d")

        with open(file_path, 'rb') as f:
            hlist = pickle.load(f)
        return hlist
    except Exception as e:
        logging.debug("1 : {}".format(e))

@lru_cache(maxsize=None)
def __get_excelist() -> List[datetime]:
    try:
        file_path = os.path.join(lib_path, "exclist.d")
        with open(file_path, 'rb') as f:
            hlist = pickle.load(f)
        return hlist
    except Exception as e:
        logging.debug("1 : {}".format(e))


def __format_input(dateobj : Union[DateFormat,date, datetime]) -> datetime:
    if isinstance(dateobj, str):
        try:
            dt = datetime.strptime(dateobj, "%d-%m-%Y")
            return dt
        except ValueError as e:
            logging.debug(e)
            return
    elif isinstance(dateobj, datetime):
        return dateobj
    elif isinstance(dateobj, date):
        return datetime.combine(dateobj, time())
    else:
        logging.debug("Invalid input type. Expected str, date, or datetime.")
        return

def __get_holidays(start_date : Union[DateFormat,date, datetime],  end_date : Union[DateFormat,date, datetime] = None) -> Union[List[datetime], tuple]:
    start_date = __format_input(start_date)
    if start_date is None:
        logging.debug("Check Input Parameters") 
        return
    holidays = __get_holylist()
    st_yr = start_date.year
    max_yr = max(holidays).year
    warning_raised = False
    if not (max_yr >= st_yr >= 2010):
        warnings.warn("Outside of NSE Holidays range. Calculations are based only on weekend dates.")
        warning_raised = True

    if end_date is not None:
        end_date = __format_input(end_date)
        ed_yr = end_date.year
        if not (max_yr >= ed_yr >= 2010)and not warning_raised:
            warnings.warn("Outside of NSE Holidays range. Calculations are based only on weekend dates.")

        return holidays, start_date, end_date
    return holidays, start_date

def __update_list(input_list : list) -> list:
    update_action = input("Select an option:\n1. Modify a date \n2. Add a date \n3. Remove a date\nEnter option number: ")
    if update_action == "1":
        try:
            item_remove = datetime.strptime(input("Enter old Date to remove (dd-mm-yyyy): "), "%d-%m-%Y")
            item_add = datetime.strptime(input("Enter the new Date to add (dd-mm-yyyy): "), "%d-%m-%Y")
        except ValueError:
            print("Invalid Input.")
            return
        
        if item_remove in input_list:
            input_list.remove(item_remove)
        else:
            print("Input date is not correct")
        if item_add not in input_list:
            input_list.append(item_add)
            input_list.sort()
            return input_list
        else:
            print("Date already exists in the list.")
    elif update_action == "2":
        item = datetime.strptime(input("Enter the Date to add (dd-mm-yyyy): "), "%d-%m-%Y")
        
        if item not in input_list:
            input_list.append(item)
            input_list.sort()
            return input_list
        else:
            print("Date already exists in the list.")
        
    elif update_action == "3":
        item = datetime.strptime(input("Enter the Date to remove (dd-mm-yyyy): "), "%d-%m-%Y")
        
        if item in input_list:
            input_list.remove(item)
            return input_list
        else:
            print("Date does not exist in the list.")
        
    else:
        print("Invalid input.")
        

def __save_list(input_list : list, set : Literal['holidays', 'exceptions']= 'holidays'):
    try:
        file_name = "hlist.d" if set=="holidays" else "exclist.d" if set=="exceptions" else None
        if file_name:
            file_path = os.path.join(lib_path, file_name)
            with open(file_path, "wb") as f:
                pickle.dump(input_list, f)        
            print('Data saved successfully')
        else:
            raise NameError("Invalid set specified.")
    except Exception as e:
        print(f"Error Occured in Saving Data : {e}")

def __fetch_holidays() -> dict:
    base_url = "https://www.nseindia.com"
    holiday_url = f"{base_url}/api/holiday-master?type=trading"
    headers = {
        'Origin': 'https://www.nseindia.com',
        'Referer' : 'https://www.nseindia.com/',
        'User-Agent': 'Chrome/111.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    s = requests.Session()
    try:
        s.headers.update(headers)
        r = s.get(base_url, timeout=5)
        r = s.get(holiday_url, timeout=5)
        if r.status_code == 200:
            return r.json()['CM']
    except Exception as e:
        print(f"Error Fetching Holidays list :: {e}")

def __format_dict_dates(cm_dict : dict) -> dict:
    exception_list = []
    trading_dates = []
    for item in cm_dict:
        trading_date_str = item.get('tradingDate', '')
        if trading_date_str:
            try:
                trading_date = datetime.strptime(trading_date_str, '%d-%b-%Y')
            except ValueError:
                try:
                    trading_date = datetime.strptime(trading_date_str, '%d-%B-%Y')
                except ValueError:
                    print(f"Unable to process date :: {trading_date}")
                    pass

            if isinstance(trading_date, datetime):
                weekday = trading_date.strftime('%A')
                description = item.get('description', '')
                if '*' in description:
                    if weekday == 'Saturday' or weekday == 'Sunday':
                        exception_list.append(trading_date)
                else:
                    if weekday != 'Saturday' or weekday != 'Sunday':
                        trading_dates.append(trading_date)
    if exception_list:
        print(f"Exceptional Trading Dates (Saturday/Sunday):: {exception_list}")
    if trading_dates:
        print(f"Holidays list :: {trading_dates}")

    return trading_dates, exception_list

def get_new_holidays(mode : Literal['test', 'normal'] = 'test'):
    try:
        holi_dict = __fetch_holidays()
        holi_list, exc_list = __format_dict_dates(cm_dict=holi_dict)
        if mode=='normal':
            holi_yr = holi_list[0].year
            old_holidays = __get_holylist()
            max_yr = max(old_holidays).year
            if holi_yr <= max_yr:
                print("Data already exists")
                return
            else:
                choice = input("Do you want to save these holidays data ?  (Y/N): ").lower()
                assert choice in ['y', 'n'], "Invalid choice. Please enter 'Y' or 'N'."
                if choice == 'y':                    
                    if holi_list:
                        new_holiday_list = list(set(old_holidays + holi_list))
                        __save_list(input_list=new_holiday_list)
                    if exc_list:                        
                        new_exception_list = list(set(__get_excelist() + exc_list))
                        __save_list(input_list=new_exception_list, set='exceptions') 
                    __get_holylist.cache_clear()
                    __get_excelist.cache_clear()
                    __get_holylist()                    
                    __get_excelist()                                   
                elif choice == 'n':
                    print("Saving of holidays aborted")
                    return
    except Exception as e:
        print(f"Error getting new holidays :: {e}")

def update_holiday(dates_set : Literal['holidays', 'exceptions'] = 'holidays'):
    assert dates_set in ('holidays', 'exceptions'), "Invalid dates_set specified."
    if dates_set == 'holidays':
        date_list = __get_holylist()
        mod_list = __update_list(input_list=date_list)
        if mod_list:
            choice = input("Do you want to save modified date list?  (Y/N): ").lower()
            assert choice in ['y', 'n'], "Invalid choice. Please enter 'Y' or 'N'."
            if choice == 'y': 
                __save_list(input_list=mod_list)
                __get_holylist.cache_clear()
                __get_holylist()
            elif choice == 'n':
                print("Date modification cancelled")
        else:
            print("Error in data")
    elif dates_set == 'exceptions':
        date_list = __get_excelist()
        mod_list = __update_list(input_list=date_list)
        if mod_list:
            choice = input("Do you want to save modified exception list? ?  (Y/N): ").lower()
            assert choice in ['y', 'n'], "Invalid choice. Please enter 'Y' or 'N'."
            if choice == 'y': 
                __save_list(input_list=mod_list, set='exceptions')
                __get_excelist.cache_clear()
                __get_excelist()
            elif choice == 'n':
                print("Date modification cancelled")
        else:
            print("Error in data")

def workday(input_date: Union[DateFormat,date, datetime], direction:Literal["prev", "next"]) -> datetime:
    """Return nearest workday of the input_date if input_date is a holiday .. if not will return the same """     
    if direction not in ["prev", "next"]:
        logging.debug("Please input direction 'prev' or 'next'")
        return
    try:
        holidays, input_date = __get_holidays(start_date=input_date)
        expc_days = __get_excelist()
    except Exception as e:
        logging.debug("3 : {}".format(e))
        return
    weekend_list = [5, 6] 

    direction = 1 if direction == "next" else -1
    
    while True:
        if input_date.weekday() in weekend_list and input_date not in expc_days or input_date in holidays:
            input_date += timedelta(days=direction)
        else:
            break
    return input_date

def get_holidays_list(start_date : Union[DateFormat,date, datetime],  end_date : Union[DateFormat,date, datetime]) -> List[datetime]:
    """Return all holidays of the given range as a datetime.datetime list"""    
    try:
        holidays, start_date, end_date = __get_holidays(start_date=start_date, end_date=end_date)
        expc_days = __get_excelist()
    except Exception as e:
        logging.debug("4 : {}".format(e))
        return
    
    holidays_in_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1) 
                if (start_date + timedelta(days=i)).weekday() >= 5 and 
                (start_date + timedelta(days=i)) not in expc_days
                ]+ [dt for dt in holidays if start_date <= dt <= end_date]

    return  sorted(holidays_in_range)

def get_workdays_list(start_date : Union[DateFormat,date, datetime],  end_date : Union[DateFormat,date, datetime]) -> List[datetime]:
    """Return all workdays of the given range as a datetime.datetime list"""
    try:
        holidays, start_date, end_date = __get_holidays(start_date=start_date, end_date=end_date)
        expc_days = __get_excelist()
    except Exception as e:
        logging.debug("5 : {}".format(e))
        return
    holidays_list = [start_date + timedelta(days=i) for i in 
                     range((end_date - start_date).days + 1) 
                     if (start_date + timedelta(days=i)).weekday() >= 5
                     and (start_date + timedelta(days=i)) not in expc_days
                     ] + [dt for dt in holidays if start_date <= dt <= end_date]
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    workdays = [date for date in date_range if date not in holidays_list]
    
    return sorted(workdays)

def isHoliday(input_date: Union[DateFormat,date, datetime]) -> Union[bool, None]:
    """Check the input_date is holiday or not . Output Bool"""
    try:
        holidays, input_date = __get_holidays(start_date=input_date)
        expc_days = __get_excelist()
    except Exception as e:
        logging.debug("isHoliday Error  : {}".format(e))
        return
    return input_date in holidays or input_date.weekday() >= 5 and input_date not in expc_days

def month_last_weekday(input_date: Union[DateFormat,date, datetime], last_weekday: str, filtered :bool = True) -> datetime:
    """Return last occurences of the given weekday in the month of the input_date as datetime.datetime .
    if filtered True it will return previous workday if the calculated weekday is holiday"""
    try:
        date_obj = __format_input(input_date)
        month = date_obj.month
        year = date_obj.year

        _, last_day = calendar.monthrange(year, month)

        weekdays = list(calendar.day_name)
        target_weekday = weekdays.index(last_weekday.capitalize())

        last_appearance = next((current_date for day in range(last_day, 0, -1) if (current_date := datetime(year, month, day)).weekday() == target_weekday), None)
        if filtered:
            return workday(input_date=last_appearance,direction="prev")

        return last_appearance
    except Exception as e:
        logging.debug("Error in month last weekday : {}".format(e))
        return

def get_month_weekdays(input_date: Union[DateFormat,date, datetime], required_weekday: str, filtered :bool = True) -> List[datetime]:
    """Return all occurences of the given weekday in the month of the input_date as a datetime.datetime list.
    if filtered True it will return previous workday if any calculated weekday is holiday"""
    try:
        date_obj = __format_input(input_date)
        month = date_obj.month
        year = date_obj.year

        start_date = datetime(year, month, 1)

        weekday_dates = []
        current_date = start_date
        
        if filtered:
            end_date = start_date.replace(day=calendar.monthrange(year, month)[1]) + timedelta(days=6)
            weekday_dates = [
            current_date
            for current_date in (start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1))
            if current_date.strftime("%A") == required_weekday.capitalize()
        ]
            filtered_days = [workday(input_date=dt, direction="prev") for dt in weekday_dates]
            filtered_workdays = [dt for dt in filtered_days if dt.month == month]
            return filtered_workdays
        else:
            end_date = start_date.replace(day=calendar.monthrange(year, month)[1])
            weekday_dates = [
            current_date
            for current_date in (start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1))
            if current_date.strftime("%A") == required_weekday.capitalize()
        ]

            return weekday_dates
    except Exception as e:
        logging.debug("Error in monthly weekday : {}".format(e))
        return

def get_weekdays(start_date : Union[DateFormat,date, datetime], end_date : Union[DateFormat,date, datetime], required_weekday: str, filtered :bool = True) -> List[datetime]:
    """Return all occurences of the given weekday in the range of start_date <-> end_date as a datetime.datetime list.
    if filtered True it will return previous workday if any calculated weekday is holiday"""
    try:
        start_date = __format_input(start_date)
        end_date = __format_input(end_date)

        weekday_dates = []
        current_date = start_date
        
        if filtered:
            end_date2 = end_date + timedelta(days=6)
            weekday_dates = [
            current_date
            for current_date in (start_date + timedelta(days=n) for n in range((end_date2 - start_date).days + 1))
            if current_date.strftime("%A") == required_weekday.capitalize()
        ]
           
            filtered_workdays = [dt for dt in [workday(input_date=dt, direction="prev") 
                                               for dt in weekday_dates] if start_date.month <= dt.month <= end_date.month 
                                               and start_date <= dt <= end_date]
            return filtered_workdays
        else:
            weekday_dates = [
            current_date
            for current_date in (start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1))
            if current_date.strftime("%A") == required_weekday.capitalize()
        ]

            return weekday_dates
    except Exception as e:
        logging.debug("Error in weekday range : {}".format(e))
        return