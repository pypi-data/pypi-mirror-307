# TableHockeyTools
### this package is in early development and is lacking in functionality
**TableHockeyTools** is a Python package designed to gather data related to Table Hockey. TableHockeyTools provides convenient functions to make working with Table Hockey data straightforward.

## Features

- **Data Gathering:** Easily gather data related to Table Hockey players, such as points and rank.
- **Examples Provided:** The `examples` folder demonstrates usage for various functions.

## Installation

this project is available on [pypi](https://pypi.org/project/TableHockeyTools/) and can be installed using 'pip':

```bash
pip install TableHockeyTools
```

Alternativeley, you can clone this repository and install using `pip`:

```bash
git clone https://github.com/Benginy-lab/TableHockeyTools.git
cd TableHockeyTools
pip install .
```



## Usage

Import the package `THTools` and use the functions as needed:

```python
import THTools as tht

# Example usage
player_names = ['Evigeny Matansev', 'Rainers Kalnins']
player_ids = []
for player_name in player_names:
    player_ids.append(tht.GetPlayerID(player_name))
for player_id, player_name in zip(player_ids, player_names):
    player_points = tht.GetPlayerPoints(player_id)
    print(f"{player_name} has {player_points} points.")
    
```

Check out the `examples` folder for more detailed usage.

## Documentation

For full documentation of functions, see the manpage 'Manpage.md or visit the [pypi documentation](https://pypi.org/project/TableHockeyTools/) if available, the documentation is not yet any different from this readme.

### Example Functions

- **GetPlayerID(Name):** retrieves the ITHF player ID for a given player name.
- **GetPlayerPoints(ID):** retrieves the points for a given player ID.
- **GetPlayerRank(ID):** retrieves the rank for a given player ID.
  
Each function documented in `THTools.py` and `examples/`.

## Development

Feel free to contribute! To install the package in development mode just add -e:

```bash
pip install -e .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions, reach out via GitHub issues or contact me directly.
