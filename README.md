# Universal Unit Converter

A comprehensive command-line unit converter supporting 10 measurement categories with conversion history tracking. Built in pure Python.

## Features

- **10 categories** — Length, Mass, Time, Speed, Area, Volume, Data, Energy, Pressure, Temperature
- **Precise conversion factors** — Sourced from standard references
- **Temperature support** — Non-linear conversions (Celsius, Fahrenheit, Kelvin, Rankine)
- **Conversion history** — Last 50 conversions saved to `history.json`
- **Smart formatting** — Numbers displayed cleanly without unnecessary decimals
- **Colored output** — ANSI-styled terminal UI

## Project Structure

```
UnitConverter/
├── app.py         # CLI entry point and interactive loop
├── units.py       # Unit definitions and conversion factors
├── converter.py   # Conversion engine (linear + temperature)
├── history.py     # Conversion history with JSON persistence
└── history.json   # Auto-generated history file
```

## How to Run

```bash
cd UnitConverter
python app.py
```

No external dependencies required — uses only the Python standard library (Python 3.10+).

## Usage

1. Select a category (by number or name)
2. Choose the source and target units
3. Enter the value to convert

Type `h` to view conversion history or `c` to clear it.

## Supported Categories & Sample Units

| Category    | Sample Units                                      |
|-------------|---------------------------------------------------|
| Length      | meter, kilometer, mile, foot, inch, light_year     |
| Mass        | kilogram, gram, pound, ounce, metric_ton           |
| Time        | second, minute, hour, day, week, year              |
| Speed       | meter_per_second, km/h, mph, knot, mach            |
| Area        | square_meter, hectare, acre, square_mile            |
| Volume      | liter, milliliter, gallon_us, cup_us, cubic_meter  |
| Data        | byte, kilobyte, megabyte, gigabyte, terabyte       |
| Energy      | joule, calorie, kilowatt_hour, btu                 |
| Pressure    | pascal, bar, atmosphere, psi, mmhg                 |
| Temperature | celsius, fahrenheit, kelvin, rankine               |

## Example

```
╔══════════════════════════════════════════╗
║         Universal Unit Converter         ║
╚══════════════════════════════════════════╝

  Select category: 1
  From unit: kilometer
  To unit: mile
  Value to convert: 42

  42 kilometer  =  26.09759 mile
```
