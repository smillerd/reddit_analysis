# reddit_analysis
Uses reddit's praw module to download data about posts. It tracks that data over time and stores the timeseries in a MySQL database

There are currently two modules that are important in this process: rQuery and rRecord. rQuery is the bot that gathers the reddit data each time it is run, it formats the data, and it stores the data in a temporary csv file (later tempfile module will be used).

rRecord takes that temporary csv and writes it to a MySQL database (be sure to enter your database details).

These modules will eventually be made more versatile so that similar processes could work with other webscrapers, for example.
