# birtchart

Small Python script that generates interactive astronomical charts using `ephem` and `plotly`.

## Features

- Heliocentric 2D view
- Geocentric polar view (with coordinates)
- Heliocentric 3D view

<img width="450" height="323" alt="Image" src="https://github.com/user-attachments/assets/15f5398c-4c30-4a83-a34b-398b4b9a9550" />

<details>
  <summary>PLOT IMGs</summary>
  
<img width="1756" height="851" alt="Image" src="https://github.com/user-attachments/assets/2d28cf15-1755-4cb1-b97a-e36282f92cd9" />

<img width="1756" height="851" alt="Image" src="https://github.com/user-attachments/assets/6be13e21-65ef-4ff1-8158-430235c925bf" />

<img width="1756" height="851" alt="Image" src="https://github.com/user-attachments/assets/842b06e9-43ef-4bf3-b5b5-1f12d0956a0d" />

</details>

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

