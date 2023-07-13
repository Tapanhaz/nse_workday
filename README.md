# nse_workday

<div class="cell markdown">

  A library to calculate holidays, workdays and some other functions based
on NSE trading holidays from 2010 - 2023.

It can be installed by:

</div>

<div class="cell markdown">

pip install nse-workday

</div>

<div class="cell code" execution_count="1">

``` python
from nse_workday import *
```

</div>

<div class="cell markdown">

1.  

get_new_holidays(mode='test')

Retrieves list of latest holidays from nse and save it if fetched list
year \> last available holidays year in library

Args::

    mode = 'test' / 'normal' . Default 'test' (will not save data.). 

</div>

<div class="cell code" execution_count="5">

``` python
get_new_holidays(mode='normal')
```

<div class="output stream stdout">

    No Dates to Exclude
    Exceptional Trading Dates (Saturday/Sunday):: ['12-11-2023']
    Holidays list :: ['26-01-2023', '07-03-2023', '30-03-2023', '04-04-2023', '07-04-2023', '14-04-2023', '01-05-2023', '29-06-2023', '15-08-2023', '19-09-2023', '02-10-2023', '24-10-2023', '14-11-2023', '27-11-2023', '25-12-2023']
    Data already exists

</div>

</div>

<div class="cell markdown">

1.  

update_holiday(dates_set = 'holidays')

Modify / Add / Remove a date from holidays or exceptions list (
Exception :: Trading days in Saturday/ Sunday)

Args::

    dates_set : 'holidays' / 'exceptions' . Default 'holidays'    

The date should be entered in dd-mm-yyyy format.

</div>

<div class="cell code" execution_count="2">

``` python
update_holiday()
```

<div class="output stream stdout">

    Select an option:
    1. Modify a date 
    2. Add a date 
    3. Remove a date
    Enter option number: 1
    Enter old Date to remove (dd-mm-yyyy): 28-06-2023
    Enter the new Date to add (dd-mm-yyyy): 29-06-2023
    Do you want to save modified date list?  (Y/N): y
    Data saved successfully

</div>

</div>

<div class="cell markdown">

1.  

isHoliday(input_date)

Check the given date is holiday or not . Return Boolean.

Args::

    input_date : date in %d-%m-%Y/ datetime.date / datetime.datetime format

</div>

<div class="cell code" execution_count="2">

``` python
isHoliday(input_date="29-06-2023")
```

<div class="output execute_result" execution_count="2">

    True

</div>

</div>

<div class="cell markdown">

All below functions returns datetime.datetime item / list.

1.  

workday(input_date, direction)

Will return the nearest workday in the given direction if the input_date
is holiday. If not, will return the same

Args ::

    input_date : date in %d-%m-%Y / datetime.date / datetime.datetime format    

    direction : 'next' / 'prev'

</div>

<div class="cell code" execution_count="4">

``` python
workday(input_date="29-06-2023",direction='prev')
```

<div class="output execute_result" execution_count="4">

    datetime.datetime(2023, 6, 28, 0, 0)

</div>

</div>

<div class="cell markdown">

1.  

get_holidays_list(start_date, end_date)

Returns all holidays as a list within the given range

Args::

    start_date : date in %d-%m-%Y / datetime.date / datetime.datetime format    

    end_date : date in %d-%m-%Y / datetime.date / datetime.datetime format

</div>

<div class="cell code" execution_count="10">

``` python
get_holidays_list(start_date="20-6-2023", end_date="30-6-2023")
```

<div class="output execute_result" execution_count="10">

    [datetime.datetime(2023, 6, 24, 0, 0),
     datetime.datetime(2023, 6, 25, 0, 0),
     datetime.datetime(2023, 6, 29, 0, 0)]

</div>

</div>

<div class="cell markdown">

1.  

get_workdays_list(start_date, end_date)

Returns all workdays as a list within the given range

Args::

    start_date : date in %d-%m-%Y / datetime.date / datetime.datetime format    

    end_date : date in %d-%m-%Y / datetime.date / datetime.datetime format

</div>

<div class="cell code" execution_count="11">

``` python
get_workdays_list(start_date="20-6-2023", end_date="30-6-2023")
```

<div class="output execute_result" execution_count="11">

    [datetime.datetime(2023, 6, 20, 0, 0),
     datetime.datetime(2023, 6, 21, 0, 0),
     datetime.datetime(2023, 6, 22, 0, 0),
     datetime.datetime(2023, 6, 23, 0, 0),
     datetime.datetime(2023, 6, 26, 0, 0),
     datetime.datetime(2023, 6, 27, 0, 0),
     datetime.datetime(2023, 6, 28, 0, 0),
     datetime.datetime(2023, 6, 30, 0, 0)]

</div>

</div>

<div class="cell markdown">

1.  

get_month_weekdays(input_date, required_weekday, filtered=True)

Return all occurences of the required weekday from the given date month

Args::

    input_date : date in %d-%m-%Y / datetime.date / datetime.datetime format    

    required_weekday : Weekday name (eg. 'Sunday'/'sunday').    

    filtered : bool . Default True ( Will return the previous work day if a required weekday is holiday.) 

</div>

<div class="cell code" execution_count="12">

``` python
get_month_weekdays(input_date="21-6-2023", required_weekday='thursday')
```

<div class="output execute_result" execution_count="12">

    [datetime.datetime(2023, 6, 1, 0, 0),
     datetime.datetime(2023, 6, 8, 0, 0),
     datetime.datetime(2023, 6, 15, 0, 0),
     datetime.datetime(2023, 6, 22, 0, 0),
     datetime.datetime(2023, 6, 28, 0, 0)]

</div>

</div>

<div class="cell markdown">

1.  

month_last_weekday(input_date, last_weekday, filtered=True)

Return last occurence of the required weekday from the given date month

Args::

    input_date : date in %d-%m-%Y / datetime.date / datetime.datetime format    

    last_weekday : Weekday name (eg. 'Sunday'/'sunday').    

    filtered : bool . Default True (Will return the previous work day if a last weekday is holiday.) 

</div>

<div class="cell code" execution_count="14">

``` python
month_last_weekday(input_date="21-6-2023", last_weekday='thursday')
```

<div class="output execute_result" execution_count="14">

    datetime.datetime(2023, 6, 28, 0, 0)

</div>

</div>

<div class="cell markdown">

1.  

get_weekdays(start_date, end_date, required_weekday, filtered=True)

Return all occurences of the required weekday from the given range

Args::

    start_date : date in %d-%m-%Y / datetime.date / datetime.datetime format    

    end_date : date in %d-%m-%Y / datetime.date / datetime.datetime format    

    required_weekday : Weekday name (eg. 'Sunday'/'sunday').    

    filtered : bool . Default True ( Will return the previous work day if a required weekday is holiday.)

</div>

<div class="cell code" execution_count="15">

``` python
get_weekdays(start_date="21-3-2023", end_date="30-6-2023", required_weekday='friday')
```

<div class="output execute_result" execution_count="15">

    [datetime.datetime(2023, 3, 24, 0, 0),
     datetime.datetime(2023, 3, 31, 0, 0),
     datetime.datetime(2023, 4, 6, 0, 0),
     datetime.datetime(2023, 4, 13, 0, 0),
     datetime.datetime(2023, 4, 21, 0, 0),
     datetime.datetime(2023, 4, 28, 0, 0),
     datetime.datetime(2023, 5, 5, 0, 0),
     datetime.datetime(2023, 5, 12, 0, 0),
     datetime.datetime(2023, 5, 19, 0, 0),
     datetime.datetime(2023, 5, 26, 0, 0),
     datetime.datetime(2023, 6, 2, 0, 0),
     datetime.datetime(2023, 6, 9, 0, 0),
     datetime.datetime(2023, 6, 16, 0, 0),
     datetime.datetime(2023, 6, 23, 0, 0),
     datetime.datetime(2023, 6, 30, 0, 0)]

</div>

</div>
