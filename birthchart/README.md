# birtchart

Small Python script that generates interactive astronomical charts using `ephem` and `plotly`.

## Features

- Heliocentric 2D view
- Geocentric polar view (with coordinates)
- Heliocentric 3D view

<img width="450" height="323" alt="Image" src="https://github.com/user-attachments/assets/15f5398c-4c30-4a83-a34b-398b4b9a9550" />

## Requirements

- Python 3.10+
- `ephem`
- `numpy`
- `plotly`

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install ephem numpy plotly
```

## Run

```bash
python3 main.py
```

Then choose one option from the menu:

- `1` Heliocentric 2D
- `2` Geocentric Polar
- `3` Heliocentric 3D

The chart opens in an interactive Plotly window.

## Notes

- The birth date is hardcoded in `DEFAULT_NASC`
- The current time is read in UTC at runtime
- The chart uses a dark theme with high-contrast colors

