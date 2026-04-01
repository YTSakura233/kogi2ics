# kogi2ics

[中文](README.md) | [日本語](README_JP.md) | English

`kogi2ics` is a small tool for exporting KCG.EDU(Kyoto Computer Gakuin, The Kyoto College of Graduate Studies for Informatics) class data as `.ics` calendar files.

This project is centered around two Python files:

- [getkogi.py](/e:/京都情报/getkogi/getkogi.py): the main entry point. It fetches class data from the KCGI Portal API and generates `kogi.json` and `kogi.ics`
- [generate_ics.py](/e:/京都情报/getkogi/generate_ics.py): the conversion module. It converts class JSON into `.ics`

### Flow

1. [getkogi.py](/e:/京都情报/getkogi/getkogi.py) calls the KCGI Portal API
2. The response is saved as `kogi.json`
3. [getkogi.py](/e:/京都情报/getkogi/getkogi.py) calls `write_ics(...)` from [generate_ics.py](/e:/京都情报/getkogi/generate_ics.py)
4. `kogi.ics` is written

### Features

- Fetches KCGI class schedule JSON
- Extracts class title, date, `時限`, and room from `tooltip`
- Converts class periods into actual class times
- Expands room prefixes into campus names
  - `M` = `KCGI百万遍キャンパス南校舎`
  - `H` = `KCGI百万遍キャンパス本部棟`
- Generates a standard `.ics` file in the `Asia/Tokyo` timezone

### Requirements

- Python 3.10+
- `requests`

Install dependencies:

```bash
pip install requests
```

### Usage

Run the main file:

```bash
python getkogi.py -c "YOUR_COOKIE" -x "YOUR_X_CPAUTHORIZE" -t 1
```

Arguments:

- `-c`, `--cookie`: your logged-in cookie
- `-x`, `--x`: the `x-cpauthorize` request header
- `-t`, `--term`: school term, `1` for spring and `2` for autumn

This generates:

- `kogi.json`
- `kogi.ics`

If you already have `kogi.json`, you can also run the conversion module directly:

```bash
python generate_ics.py -i kogi.json -o kogi.ics
```

### Class periods

The class period schedule is embedded directly in the code:

- Period 1 `09:30-11:00`
- Period 2 `11:10-12:40`
- Period 3 `13:30-15:00`
- Period 4 `15:10-16:40`
- Period 5 `16:50-18:20`
- Period 6 `18:30-20:00`
- Period 7 `20:10-21:40`

### Calendar import

#### Apple Calendar

You can use this Shortcut to import the `.ics` file:

`https://routinehub.co/shortcut/7005/`

#### Android calendars

Whether Android can import `.ics` directly depends on the calendar app you use.

- Some apps can open a local `.ics` file directly
- Some apps do not support direct import on the phone itself
- If you use Google Calendar, importing on the web first and then syncing is usually the safer approach

So the best first step is to try opening `kogi.ics` directly. If that does not work, use a web import flow or a third-party calendar app with `.ics` support.
