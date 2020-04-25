import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('This is an interactive portal that presents statistics for the bikeshare data you are interested in.')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
#     valid_city = ['chicago', 'new york city', 'washington']

#     user_input = input('\nWould you like to see data for Chicago, New york city, or Washington?')
#     while not user_input or str(user_input).lower() not in valid_city:
#         user_input = input('\nWould you like to see data for Chicago, New york city, or Washington?')

    city = str(input('\nWould you like to see data for Chicago, New york city, or Washington?')).lower()

    valid_city = ['chicago', 'new york city', 'washington']
    while city not in valid_city:
        print(city)
        print('\nplease enter one valid city name from the three cities provided below')
        city = str(input('\nWould you like to see data for chicago, new york city, or washington?')).lower()


    filter_month_day = str(input('\nWould you like to filter the data by month, day, both or not at all? Type "None" for no time filter.')).lower()
    valid_filter = ['month', 'day', 'both', 'none']
    while filter_month_day not in valid_filter:
        print('\nplease enter either \"month\", \"day\", \"both\" or \"none\".')
        filter_month_day = str(input('\nWould you like to filter the data by month, day, both or not at all? Type "None" for no time filter.')).lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    valid_month = ['january', 'february', 'march', 'april', 'may', 'june']
    valid_day = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    if filter_month_day == 'both':
        month = str(input('\nWhich month? January, February, March, April, May, June?')).lower()
        while month not in valid_month:
            print('\nplease enter a valid month')
            month = str(input('\nWhich month? January, February, March, April, May, June?')).lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day = str(input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.')).lower()
        while day not in valid_day:
            print('\nplease enter a valid day')
            day = str(input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.')).lower()


    elif filter_month_day == 'month':
        day = 'all'
        month = str(input('\nWhich month? January, February, March, April, May, June?')).lower()
        while month not in valid_month:
            print('\nplease enter a valid month')
            month = str(input('\nWhich month? January, February, March, April, May, June?')).lower()


    elif filter_month_day == 'day':
        month = 'all'
        day = str(input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.')).lower()
        while day not in valid_day:
            print('\nplease enter a valid day')
            day = str(input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.')).lower()


    else:
        month = 'all'
        day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df = df[df['day_of_week'] == day.lower().title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = df['month'].mode()[0]
    count_month = df['month'].value_counts()[popular_month]
    print("\nThe most common month is", months[popular_month-1], ', Count is', count_month)

    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    count_day = df['day_of_week'].value_counts()[popular_day_of_week]
    print("\nThe most common day of week is", popular_day_of_week, ', Count is', count_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    count_hour = df['hour'].value_counts()[popular_hour]
    print("\nThe most common start hour is", popular_hour, ', Count is', count_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("\nThe most commonly used start station is", popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("\nThe most commonly used end station is", popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    comb_station = df.groupby(['Start Station', 'End Station']).size().reset_index(name = 'Time')
    popular_comb_station_name = comb_station[comb_station['Time'] == comb_station['Time'].max()]
    start = list(popular_comb_station_name['Start Station'])
    end = list(popular_comb_station_name['End Station'])

    combination = zip(start, end)

    for c in combination:
        print('\nThe most frequent combination of start station and end station trip is', c)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    m, s = divmod(total_duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)
    total_trip_duration = "\nTotal trip duration: %d years %02d days %02d hrs %02d min %02d sec" % (y, d, h, m, s)
    print(total_trip_duration)

    # TO DO: display mean travel time
    mean_duration = df['Trip Duration'].mean()
    m, s = divmod(mean_duration, 60)
    h, m = divmod(m, 60)
    mean_trip_duration = "\nMean trip duration: %02d hrs %02d min %02d sec" % (h, m, s)
    print(mean_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    print('\nCalculating Gender...\n')
    while True:
        try:
            gender = df['Gender'].value_counts()
            print(gender)
        except KeyError:
            print('\nNo gender data available.')
        break

    # TO DO: Display earliest, most recent, and most common year of birth
    print('\nCalculating earliest, most recent, and most common year of birth...\n')

    while True:
        try:
            earliest_bd = df['Birth Year'].min()
            most_recent_bd = df['Birth Year'].max()
            most_common_bd = df['Birth Year'].value_counts().index[0]

            print('\nEarliest year of birth is', earliest_bd)
            print('\nMost recent year of birth is', most_recent_bd)
            print('\nMost common year of birth is',most_common_bd)

        except KeyError:
            print('\nNo birth year data available.')
        break


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    raw_data_start = input('\nDo you want to see 5 rows of data? Enter yes or no.').lower()
    if raw_data_start != 'yes':
        return
    else:
        i = 0
        m = len(df.index)
        #print(m)
        while i < m:
            start = i
            end = min(i+5, m)
            print(df.iloc[start:end])
            if end == m:
                print('\nThis is the end of the dataset.')
                return
            raw_data_more = input('\nDo you want to see more data? Enter yes or no.').lower()
            if raw_data_more == 'yes':
                i += 5
            else:
                return



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        print('\nThanks for playing with exploring the data.')
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("\nBye!")
            break


if __name__ == "__main__":
    main()
