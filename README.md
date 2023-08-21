# pl_scraper
Web scraper that scrapes all sorts of data from the Premier League website

## Requirements
 - **Python 3.7.3** or higher
 - **requests 2.21.0** or higher

## Quickstart guide
0. Install the `requests` module. This is commonly done by running `pip3 install requests` in your terminal.
1. Download the `pl_scraper.py` script and place it in the same directory as your program.
2. At the top of your program, type `import pl_scraper as pl`.
3. Get Premier League information to your heart's desire!

## Configuration
Configurable setting can be found in the first couple of lines of the script. They are mainly for developer purposes. Do not change them unless you know what you are doing!

## Basic functions
> Please note that this is not a complete list. There may be functions not mentioned here due to them being in active development or because they are mainly for internal use.

### pl.teams()
Returns a list of all the teams in the current season of the Premier League.

**Example response:**
```
['Arsenal', 'Aston Villa', 'AFC Bournemouth', 'Brentford', 'Brighton & Hove Albion', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton ', 'Fulham', 'Liverpool', 'Luton Town', 'Manchester City', 'Manchester United', 'Newcastle United', 'Nottingham Forest', 'Sheffield United', 'Tottenham Hotspur', 'West Ham United', 'Wolverhampton Wanderers']
```

### pl.matchweek()
Returns information about the current matchweek.

**Example response:**
```
{
  'matches': [
    {
      'teams': {
        'home': {
          'name': 'Nottingham Forest',
          'club': {
            'name': 'Nottingham Forest',
            'shortName': "Nott'm Forest",
            'abbr': 'NFO',
            'id': 15
          },
          'teamType': 'FIRST',
          'shortName': "Nott'm Forest",
          'id': 15,
          'altIds': {
            'opta': 't17'
          }
        },
        'away': {
          'name': 'Sheffield United',
          'club': {
            'name': 'Sheffield United',
            'shortName': 'Sheffield Utd',
            'abbr': 'SHU',
            'id': 18
          },
          'teamType': 'FIRST',
          'shortName': 'Sheffield Utd',
          'id': 18,
          'altIds': {
            'opta': 't49'
          }
        }
      },
    'score': {
      'home': 1,
      'away': 0
    },
    'id': 93337,
    'timestamp': 1692384300000,
    'completeness': 3
    'clock': {
      'secs': 5880,
      'label': "90 +8'00"
    },
    'result': 'H';
  },
  {
    'teams': {
...
```
