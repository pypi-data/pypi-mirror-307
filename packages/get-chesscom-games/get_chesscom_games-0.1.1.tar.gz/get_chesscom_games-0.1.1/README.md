# get-chesscom-games

A Python API Wrapper for Chess.com to fetch chess games.

This library allows you to retrieve chess games from a Chess.com user’s profile going back a specified number of months. It's designed to be simple to use, and simplifies of interactions with Chess.com's API.

## Usage
- Fetch games from a Chess.com user's profile.
- Specify the number of months back to fetch games.
- Handle authentication and API requests internally.

Using get_chess_games.(Username, monthsago, optional user agent) -> returns a list of chess PGNS from X months ago until today

# Example Usage: 
import get_chess_games
get_chess_games.getgames('Wins',6) #returns all chess games froms 'Wins' in the last 6 months

## Installation

You can install `get-chesscom-games` directly from the Python Package Index (PyPI) or from source.

### Using `pip` (PyPI)
```bash
pip install get-chesscom-games

