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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    question = 'What is the  city name, please choose one of the following (chicago, new york city, washington): '
    city = input_validation(CITY_DATA.keys(), question)

    # get user input for month (all, january, february, ... , june)
    question = 'What is the  required month, please choose one of the following (all, january, february, ... , june): '
    validation_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input_validation(validation_list, question)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    question = 'What is the  required day, please choose one of the following (all, monday, tuesday, ... sunday): '
    validation_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input_validation(validation_list, question)

    print('-'*40)
    return city, month, day

def input_validation (valid_list, question):
    """
    Return a valid input from the user
    Args:
        valid_list: This is the list of the accepted input
        question: This is initial user prompt

    Returns:
        The function return the accepted user input
    """
    error_message = 'Invalid input, ' + question.lower()
    user_input = input(question).lower()
    while True:
        if user_input not in valid_list:
            user_input = input(error_message).lower()
        else:
            break
    return user_input


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])  # weekday_name

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def check_data(df):
    """
    This function check if the user want to check the data or not
    Args:
        df: DataFrame

    """
    question = 'Would you like to check the row data? '
    validation_list = ['yes', 'no', 'y', 'n']
    answer = input_validation(validation_list, question)
    if answer in ['yes', 'y']:
        start_index = 0
        pd.set_option('display.max_columns', 200)
        while True:
            print (df[start_index:(start_index+5)])
            question = 'Would you like to check more row data? '
            validation_list = ['yes', 'no', 'y', 'no']
            answer = input_validation(validation_list, question)
            start_index+=5
            if answer in ['no', 'n']:
                break


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most Common Month: ', df['month'].mode()[0])

    # display the most common day of week
    print('Most Common Day: ', df['day_of_week'].mode()[0])

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Commonly Used Start Station: ', df['Start Station'].mode()[0])


    # display most commonly used end station
    print('Most Commonly Used End Station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['trip'] = '(' + df['Start Station'] + ') - (' + df['End Station']+')'
    print('Most frequent combination of start station and end station trip: ', df['trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: {:,.2f} hours'.format(df['Trip Duration'].sum()/3600))

    # display mean travel time
    print('Mean travel time: {:.0f} sec'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    for i, v in user_type.items():
        print('Number of {}: {}'.format(i, v))

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        for i, v in gender.items():
            print('Number of {}: {}'.format(i, v))


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of birth: {:.0f}'.format(df['Birth Year'].min()))
        print('Most recent year of birth: {:.0f}'.format(df['Birth Year'].max()))
        print('Most common year of birth: {:.0f}'.format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        #city, month, day = "chicago", "june", "sunday" # this is used for the testing
        df = load_data(city, month, day)
        check_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        yes_list = ['yes', 'Yes', 'y']
        no_list = ['no', 'No', 'n']
        valid_inputs = yes_list + no_list
        if restart.lower() not in valid_inputs:
            while True:
                restart = input('\n Invalid input, would you like to restart? Enter yes or no.\n')
                if restart.lower() in valid_inputs:
                    break
        if restart.lower() not in ['yes', 'Yes', 'y']:
            break


if __name__ == "__main__":
	main()
