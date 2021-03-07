Bikeshare github project

### Nanodegree
Programming for Data Science with Python

### Date created
Project and files created: Sunday March 7, 2021

### Software version
Python v3.8

### Project Title
bikeshare data

### Description
The bikeshare data program is a python program that extracts trip and user data from one of three cities (new york city, washington dc, or chicago).

### Files used
City data: chicago.csv, washington.csv, new_york_city.csv

### Bugs log (refactoring)
1. def date_filters()
The quit option is not functional and not a requirement for filter selection.
> removed quit option from user prompts

2. def select_city()
The user input prompt for city selection shows ‘quit’ as a choice. However, if ‘quit’ is entered the program does not quit but continues to the date_filter function.
> modify first if statement
> add if statement to main function for restart option

3. def raw_data()
function keeps prompting for more data even at end of dataframe.
> modified while and if statements to check for end of dataframe.
> show total no. of records

### Credits
Forked repo: udacity/pdsnd_github

### References
Reference materials used for the Bikeshare project:

Books
> Python Crash Course by Eric Matthes
> Automate the Boring Stuff with Python by Al Sweigart

Websites
> StackOverflow
> GeeksforGeeks
> W3 School

YouTube Videos
> Pandas for Your Grandpa
> Numpy for Your Grandma
