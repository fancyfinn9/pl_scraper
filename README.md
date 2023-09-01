# pl_scraper
Web scraper that scrapes all sorts of data from the Premier League website

## Requirements
 - **Python 3.7.3** or higher
 - **requests 2.21.0** or higher

## Quickstart guide
0. Install the `requests` module. This is commonly done by running `pip3 install requests` in your terminal.
1. Download the `pl_scraper.py` script and place it in the same directory as your program.
2. At the top of your program, type `import pl_scraper as pl`.
3. Get Premier League information to your heart's desire! (try running pl.matchweek() for all the details about the current matchweek!)

## Configuration
Configurable setting can be found in the first couple of lines of the script. They are mainly for developer purposes. Do not change them unless you know what you are doing!

## Basic functions

### teams()

Returns all the teams in the current season of the Premier League

### matchweek()

Returns the matchweek number and all the matches in the current matchweek in a list

### fixture(id)

Returns information about the given match 

### player(id)

Returns information about the given player

## Legal notice
This program uses data from the Premier League website.

This program is not affiliated with or endorsed by the Premier League.

The Premier League retains all rights to the data scraped by this program.
