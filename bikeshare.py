import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities =    [ 'chicago', 'new york city','washington']
months =    ['jannuary', 'february', 'march','april','may','june','all']
days  =     ['monday','tuesday','wednessday','thursday','friday','saturday','sunday','all']

print('\n')
print('-'*80)   
print('Hello! Let\'s explore some US bikeshare data!')
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        print('\nPossible selections are: ')
        print('', *cities, sep=' | ')
        city = input('Which city do you want to analyse?\n ').lower()        # lower() makes any upper letter to lower letter
    
        if city in cities:
            check = input('You want to analyze: {} (y/n)\n '.format(city.capitalize()))
                
            if check == 'y':
                break
            else:    
                continue
        else:
            print('Any typos? Please try again:\n')
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        print('\nPossible selections are: ')
        print('', *months, sep=' | ')
        month = input('Which month do you want to analyse?\n ').lower()

        if month in months:
            check = input('You want to analyze: {} (y/n)\n '.format(month.capitalize()))
            
            if check == 'y':
                break
            else:    
                continue
        else:
            print('Any typos? Please try again:\n')
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('\nPossible selections are: ')
        print('', *days, sep=' | ')    
        day = input('Which day do you want to analyse?\n ').lower()

        if day in days:
            check = input('You want to analyze: {} (y/n)\n '.format(day.capitalize()))
            
            if check == 'y':
                break
            else:    
                continue
        else:
            print('Any typos? Please try again:\n')
            continue
    print('-'*80)     
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
    
    print('-'*80)   
    print('\nLoading Data starts!\nThis takes up to 15s')
    start_time = time.time()
    df = pd.read_csv(CITY_DATA[city])
    df_raw = df.copy()
    print("\nLoading Data took %s seconds." % round(time.time() - start_time,4))
    print('-'*40)
    
    # check for NaN values
    NaN_overfiew =  df.isnull().sum()
    print('\nSum of NaN values per column without filters applied')
    print(NaN_overfiew,'\n')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['start_hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_ind = months.index(month)

        # filter by month to create the new dataframe
        df_mask = df['month'] == month_ind + 1
        df_month = df[df_mask]
        df = df_month
        #df_fil_mon = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        days_ind = days.index(day)

        # filter by month to create the new dataframe
        df_mask = df['day_of_week'] == days_ind
        df_days = df[df_mask]
        df = df_days
        #df_fil_mon = df[df['month'] == month] 
        
    return df, df_raw

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('The most common...')
    start_time = time.time()

    # display the most common month
    most_month = df['month'].value_counts().index[0]
    print('... Moth is: [ {} ]'.format(months[most_month-1].capitalize())) 

    # display the most common day of week
    most_day = df['day_of_week'].value_counts().index[0]
    print('... Day is:  [ {} ]'.format(days[most_day].capitalize())) 

    # display the most common start hour
    most_hour= df['start_hour'].value_counts().index[0]
    print('... Hour is: [ {} ]'.format(most_hour)) 

    print("\nThis took %s seconds." % round(time.time() - start_time,4))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    print('The most common...')
    start_time = time.time()

    # display most commonly used start station
    most_StartStation = df['Start Station'].value_counts().index[0]    
    print('... Start is: [ {} ]'.format(most_StartStation.capitalize())) 
    print(df['Start Station'].value_counts().iloc[0:4],'\n') 

    # display most commonly used end station
    most_EndStation = df['End Station'].value_counts().index[0]    
    print('... End is:   [ {} ]'.format(most_EndStation.capitalize())) 
    print(df['End Station'].value_counts().iloc[0:4],'\n') 

    # display most frequent combination of start station and end station trip
    df['Combined Station'] = df['Start Station'] + [' --> '] + df['End Station']
    most_Trip = df['Combined Station'].value_counts().index[0]    
    print('... Trip is:  [ {} ]'.format(most_Trip.capitalize())) 

    print("\nThis took %s seconds." % round(time.time() - start_time,4))
    print('-'*40)

def trip_duration_stats(df):
    a = 1
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is: {} days'.format(int(df['Trip Duration'].sum()/60/60/24)))

    # display mean travel time
    print('Mean travel time is: {} minutes'.format(int(df['Trip Duration'].mean()/60)))


    print("\nThis took %s seconds." % round(time.time() - start_time,4))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts().to_string())

    try:
        # Display counts of gender
        print(df['Gender'].value_counts().to_string())

        # Display earliest, most recent, and most common year of birth
        print('\n')
        print('Earliest year of birth is:    {}'.format(int(df['Birth Year'].max())))
        print('Most recent year of birth is: {}'.format(int(df['Birth Year'].min())))
        print('Most common year of birth is: {}'.format(int(df['Birth Year'].mode())))
        print("\nThis took %s seconds." % round(time.time() - start_time,4))
        print('-'*40)    
    except KeyError:
        print('\nThere is no "Gender" and "Birth Year" Columnd in Washington\n')

def display_data(df):
    """ Asks user to show 5 lines of code or not until he tells not to do it"""
    user_request = input('Do you want to see the first 5 lines of the df (y/n)?: ').lower()
    start_ind = 0
    while user_request == 'y':
        print(df.iloc[start_ind:start_ind+5])
        nice_format = input('\nShould a nice table be printed (y/n)?: ').lower()
        if nice_format == 'y':
            print(tabulate(df.iloc[start_ind:start_ind+5], headers='keys', tablefmt='psql'))
            show_code = input('\nDo you want to see the source code to make this table (y/n)?: ').lower()
            if show_code == 'y':
                print('\n --> print(tabulate(df.iloc[start_ind:start_ind+5], headers="keys", tablefmt="psql"))')
        start_ind += 5 
        user_request = input('\nDo you want to see the next 5 lines (y/n)?: ').lower()
        
def main():
    """ This is the main function which calles all the other subfunctions
    
    Args: No arguments needed

    Returns: Only output in the command line is generated
    
    """
    while True:
        city, month, day = get_filters()
        df, df_raw = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df_raw)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        print('-'*80)   
if __name__ == "__main__":
	main()