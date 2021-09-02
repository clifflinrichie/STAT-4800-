# STAT-4800
## Setup:
- Download the data zip, and extract it. Place folder in the same directory as the 4800 STAT repository

## Formatting
- column_names.json can be formatted by pressing `SHIFT-ALT-F` in the file


# Homework 1
## The Basics

1. Get to know the data. Use the associated PDF to figure out what the variables are, what challenges there are in the way the variables were coded, what variables will be important for the current assignment, etc.

2. Make sure you understand how the yard line works in the dataset. It’s not the usual way of doing things. You can either transform that yard line system to one that works (I typically use a 0 to 100 system from the perspective of the offensive team (it’s easier to do math that way)).

3. Filter the data to only include plays from the first and third quarters (and check if there is any remaining plays coded as “garbage time” which you should also remove). Restricting to the first and third quarters makes sure we are in “infinite time” mode, where teams are optimizing to add points to the board, and not to engineer a win. There is a slight issue here in that getting rid of the second and fourth quarters might leave some drives “lingering” without a score. Just throw those out. 

4. Determine how you will group the data. This can be sophisticated (taking into consideration the difference between the redzone and the open field) or not (a basic binning of the data) but you should make your choices explicit. You may wish to first figure everything out with an “easy”system for grouping your states, and then make it more sophisticated if you have time

5. Calculate the necessary entries for your table (or even better, write a function that takes a certain scenario (e.g. EP(2, 7, 32, “own”) for the expected points for second down with 7 yards to go on your own 32). The function will convert the field position to the 0-100 system, determine the state group for the particular scenario (i.e. 2nd down with anything from 7 to 10 yards remaining and anywhere from the own 30-40 yard line) and then use your empirical model to spit out an expectation ).
