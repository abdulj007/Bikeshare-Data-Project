import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
st.title("Bikeshare Data Exploration")

st.markdown("""
This app shows different statistics of Bikeshare data from three cities - Chicago,
New york city and Washington. 
- Please select your desired parameters from the left sidebar
""")
st.write('-' * 40)
st.sidebar.header('Select desired City, Month and Day')
city = st.sidebar.selectbox("Select City", ("chicago", "new york city", "washington"))
month = st.sidebar.selectbox("Select Month", ("all", "january", "february","march", "april", "may", "june"))
day = st.sidebar.selectbox("Select Day",("all", "Sunday","Monday", "Tuesday","Wednesday","Thursday","Friday","Saturday"))

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
    df = pd.read_csv(CITY_DATA[city])
    st.dataframe(df.head())
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")

    # filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week
    if day != 'all':
        # filter by day of week to create the new dataframe

        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.

    Args:
        param (df): The filtered dataset to work with

    Returns:
        None
    """
    st.subheader("Stats for the most frequent times of travel ")
    st.write('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]


    months_dict  = {1:'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june'}

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.strftime("%A")
    popular_dayofweek = df['day_of_week'].mode()[0]

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    st.write("The most popular month is: ", months_dict[popular_month])
    st.write('The most popular day is: ', popular_dayofweek)
    st.write('The most popular hour is: ', popular_hour)
    st.write("\nThis took %s seconds." % round((time.time() - start_time),2))
    st.write('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.

    Args:
        param (df): The filtered dataset to work with

    Returns:
        None
    """

    st.subheader("Stats for the most popular stations and trip")
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]


    # TO DO: display most frequent combination of start station and end station trip
    popular_start_end_station = df[['Start Station', 'End Station']].mode()

    st.write('Calculating The Most Popular Stations and Trip...')
    st.write('The most popular start station is: ', popular_start_station)
    st.write('The most popular end station is: ', popular_end_station)
    st.write('The most popular trip is: ', popular_start_end_station)
    st.write("\nThis took %s seconds." % round((time.time() - start_time), 2))
    st.write('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.

    Args:
        param (df): The filtered dataset to work with

    Returns:
        None
    """
    st.subheader("Trip Duration statistics")
    st.write('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = ((df['Trip Duration']).sum()) / 3600

    # TO DO: display mean travel time
    Average_travel_time = ((df['Trip Duration']).mean()) / 60


    st.write('Total travel time is: {}{}'.format(round(total_travel_time,2), ' hours'))
    st.write('Average travel time is: {}{}'.format(round(Average_travel_time,2), ' minutes'))
    st.write("\nThis took %s seconds." % round((time.time() - start_time), 3))
    st.write('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users.

    Args:
        param (df): The filtered dataset to work with

    Returns:
        None
    """

    st.subheader("Users statistics")
    start_time = time.time()
    st.write('\nCalculating User Stats...\n')
    # TO DO: Display counts of user types
    user_types =df['User Type'].value_counts()

    st.write('The user types count are: ',user_types)
    # TO DO: Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()

        st.write('The gender count is: ',gender_count)
    except KeyError:

        st.write('Sorry, Gender data doesn\'t exist for the specified city')
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        df['Year'] = df['Birth Year']

        earliest_year = int(df['Year'].min())
        recent_year = int(df['Year'].max())
        common_year = int(df['Year'].mode()[0])

        st.write('The earliest user birth year is: ', earliest_year)
        st.write('The most recent user birth year is: ', recent_year)
        st.write('The most common user birth year is: ', common_year)
        st.write("\nThis took %s seconds." % round((time.time() - start_time), 2))
        st.write('-' * 40)
    except KeyError:
        print('Sorry, Birth Year data doesn\'t exist for the specified city')
        st.write('Sorry, Birth Year data doesn\'t exist for the specified city')
    st.write('-' * 40)


def display_data(df):
    """Display five rows of data from the user filtered dataset. """
    st.subheader("Check the raw data")
    counter = 0
    userQuestion = st.radio("Do you want to see raw data?", ('Yes', 'No'))

        # ques = st.radio("Do you want to see more raw data?", ('Yes', 'No'))
    if userQuestion == 'Yes':

        counter =int(st.number_input("Click the + button to add 5 more rows of data",min_value=0, max_value=df.shape[0], step=5, key=0))
        st.dataframe(df.head(counter))

    elif userQuestion == 'No':
        st.write("Moving On...")

def main():


    df = load_data(city, month, day)

    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    display_data(df)

if __name__ == "__main__":
 	main()


