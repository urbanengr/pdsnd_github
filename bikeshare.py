# Bike Share project
# Valerie Gilbert Data Science with Python

import pandas as pd
import time
from datetime import datetime as dt
import calendar


cities = {'nyc': 'new_york_city.csv',
          'chi': 'chicago.csv',
          'dc': 'washington.csv'}

months = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6}
weekdays = {'sun': 6, 'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'none': 7}
dayofweek = pd.Series([0, 1, 2, 3, 4, 5, 6, 7],
                      index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'none'])


def select_city():
    """ function asks user to select desired city, then loads that city's data """

    sel_city = ''
    # --- city_choice adds flexibility to user choices to minimize input errors
    city_choice = ('nyc', 'new york city', 'chi', 'chicago', 'dc', 'washington dc')

    # --- city input and error checking loop
    while sel_city != 'quit':
        sel_city = input("\nWhat city? Enter chicago or CHI, new york city or NYC, "
                         "washington dc or DC, or quit): ").lower()
        if sel_city == 'quit':
            break
        elif sel_city not in city_choice:
            print("Incorrect selection, please try again."
                  "\nIf you would like to quit program, type 'quit'")
        else:
            print("You selected: ", sel_city)
            break
    # --- pull in city data
    if sel_city in ('nyc', 'new york city'):
        city_data = pd.read_csv(cities['nyc'])
    elif sel_city in ('chi', 'chicago'):
        city_data = pd.read_csv(cities['chi'])
    else:
        city_data = pd.read_csv(cities['dc'])

    print('-' * 40)
    return city_data, sel_city


def date_filters():
    """function determines if filtering by month, day of week or no filters"""

    city_date = ''
    date_filter = ['m', 'month', 'd', 'day', 'b', 'both', 'n', 'none']

    # --- filter input and error checking loop
    while city_date != 'quit':
        city_date = input(
            "Do you want to filter by month (enter 'm'), day of the week (enter 'd'),"
            "\n both month and day of the week (enter 'b') or none (enter 'n')?: ").lower()

        if city_date not in date_filter:
            print("\nIncorrect selection, please try again.\n")
            continue
        else:
            print("\nYou are filtering by:", city_date)

    # --- Month only filter
        if city_date in ('m', 'month'):
            month_in = input("\nWhich month? Enter using one of the following abbreviations"
                             " - jan, feb, mar, apr, may, jun: ").lower()

            if month_in not in months:
                print(
                    "\nIncorrect selection, please check spelling and try again.")
                continue
            else:
                print("Selected month is: ", month_in)
                print("Selected weekday is: none")
                weekday = 'none'
            break

    # --- Weekday only filter
        elif city_date in ('d', 'day'):
            weekday = input("\nWhat day of the week are you interested in? Enter: sun, mon, tue, wed, thu, fri, sat: ")

            if weekday not in weekdays:
                print(
                    "\nIncorrect selection, please check spelling and try again.")
                continue
            else:
                print("Selected day of week is: ", weekday)
                print("Selected month is: none")
                month_in = 'none'
            break

    # --- Month and weekday filter
        elif city_date in ('b', 'both'):
            month_in = input(
                "\nWhich month? Enter using one of the following abbreviations - jan, feb, mar, apr, may, jun: ").lower()
            weekday = input(
                "What day of the week are you interested in?"
                "\n Enter one the 3-letter abbreviations: sun, mon, tue, wed, thu, fri, or sat: ").lower()

            if (month_in not in months) or (weekday not in weekdays):
                print("\nIncorrect selection, please try again.\n")
                continue
            else:
                print("Selected month is: ", month_in)
                print("Selected day of week is: ", weekday)
            break

    # --- No filter selected
        else:
            month_in = 'none'
            weekday = 'none'
            print("No data filters selected")
            city_date = 'quit'

    print('-' * 40)

    return month_in, weekday


def date_sel(city_data, month_in, weekday):
    """function filters city data based on selected date filters"""

    df_c_data = pd.DataFrame(city_data)
    df_f_data = pd.DataFrame(columns=['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station',
                                      'User Type', 'Gender', 'Birth Year'])

    df_c_d = pd.to_datetime(df_c_data['Start Time'])
    df_c_d.month = df_c_d.dt.month
    df_c_d.weekday = df_c_d.dt.weekday

    month = months.get(month_in)
    wday = weekdays.get(weekday)


    for i in range(len(df_c_d)):
        if df_c_d.month[i] == month and weekday == 'none':
            df_f_data.loc[i] = (df_c_data.iloc[i])

        if df_c_d.weekday[i] == wday and month_in == 'none':
            df_f_data.loc[i] = (df_c_data.iloc[i])

        if df_c_d.month[i] == month and df_c_d.weekday[i] == wday:
            df_f_data.loc[i] = (df_c_data.iloc[i])

        elif month_in == 'none' and weekday == 'none':
            df_f_data = df_c_data

    return df_f_data, wday


def time_stats(df_f_data):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df_f_data = (pd.to_datetime(df_f_data['Start Time']))

    popular_hour = df_f_data.dt.hour.mode()[0]
    popular_day_n = df_f_data.dt.weekday.mode()[0]
    popular_day = dayofweek.index[popular_day_n]
    popular_month = df_f_data.dt.month.mode()[0]

    print("\nMost Popular Hour: ", popular_hour)
    print("Most Popular day: ", popular_day)
    print("Most Popular month: ", calendar.month_name[popular_month])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df_f_data):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    sta_con = (df_f_data['Start Station'])
    end_con = (df_f_data['End Station'])

    frames = [sta_con, end_con]
    both_con = pd.concat(frames, axis=1)

    sta_trips = sta_con.describe().loc[['freq']]
    end_trips = end_con.describe().loc[['freq']]
    both_trips = both_con.describe().loc[['freq']]
    both_trips_2 = both_trips['Start Station'].value_counts()

    print("Most popular start station(s)\n", sta_con.mode())
    print(f"# of trips from start station(s): {sta_trips}\n")

    print("Most popular end station(s)\n", end_con.mode())
    print(f"# of trips to end station(s): {end_trips}\n")

    print("Most popular end-to-end trips\n", both_con.mode())
    print(f"# of end-to-end trips: {both_trips_2}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(sel_city, month_in, wday, df_f_data):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()
    day_name = dayofweek.index[wday]
    print(f"\n--- Travel times in {sel_city} for month {month_in} on {day_name} --- \n")

    #--- display total travel time
    min_con = ((df_f_data['Trip Duration'].sum()) / 60)

    print(f"\nTotal travel time is {min_con} minutes")

    #--- display mean travel time
    avg_trip_con = df_f_data['Trip Duration']
    avg_con = avg_trip_con.mean()/60
    print(f"\nAverage travel time is {avg_con} minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df_f_data, sel_city, month_in, wday):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_t = df_f_data['User Type']

    # --- Display counts of user types
    user_t_ct = user_t.value_counts()
    print(f"\n User type counts for city {sel_city} in month {month_in} on {wday}")
    print(user_t_ct)

    # --- Display counts of gender
    if sel_city in ['dc', 'washington dc']:
        df_f_data['Gender'] = "no gender info"
        df_f_data['Birth Year'] = "no birth yr info"
        gender_ct = 0
        print(f"\nno gender data")
    else:
        gender_ct = df_f_data['Gender'].value_counts()

    day_name = dayofweek.index[wday]
    print(f"\nGender count for {sel_city} in month of {month_in} on {day_name} is:\n", gender_ct)

    # --- Display earliest, most recent, and most common year of birth
    min_bd = df_f_data["Birth Year"].min()
    max_bd = df_f_data["Birth Year"].max()
    comm_bd = df_f_data["Birth Year"].mode()

    print(f"Birth Year data for {sel_city} in month of {month_in} on day {day_name}")
    print(f"\nEarliest birth year is: {min_bd}")
    print(f"Most recent birth year is: {max_bd}")
    print(f"Most common birth year is: {comm_bd}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(sel_city, df_f_data):
    """ function asks if raw trip data desired, if yes prints out 5 records each time """

    req_in = 'yes'
    i = 0
    while req_in != 'no':
        req_in = input("Do you want raw trip data? Enter yes or no ('no' will exit program).").lower()

        while req_in != 'no':
            if req_in == 'yes':
                print(f"Raw Trip for city of {sel_city}")
                print(df_f_data[i:i+5])
                i = i+5
                req_in = input("Want more data? ('yes' or 'no')").lower()
        else:
            req_in = 'no'


def main():
    while True:
        city_data, sel_city = select_city()
        if sel_city == 'quit':
            restart = input("\nWould you like to restart? Enter 'yes'' or 'no'.\n")
            if restart.lower() != 'yes':
                break
            else:
                continue
        month_in, weekday = date_filters()
        df_f_data, wday = date_sel(city_data, month_in, weekday)
        time_stats(df_f_data)
        station_stats(df_f_data)
        trip_duration_stats(sel_city, month_in, wday, df_f_data)
        user_stats(df_f_data, sel_city, month_in, wday)
        raw_data(sel_city, df_f_data)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
