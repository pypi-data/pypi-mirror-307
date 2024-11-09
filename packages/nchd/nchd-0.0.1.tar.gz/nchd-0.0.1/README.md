# NCHD: A dead simple, colourised netCDF file header viewer

My use case for ncdump is *almost exclusively* `ncdump -h $FILE`. 

This presents two mild inconveniences:

1. Output is not colourised. This is kind of annoying.
2. It's too many characters to type.

This tool solves these glaring errors, by providing shorter command name, and colourising the output. It mostly exists because I wanted to write a CLI tool.

## Installation

`pip install nchd`

## Usage

```bash
nchd $FILE
```

## Options

- `--help`: Show help message and exit

## Contributing

Feel free to contribute! With that in mind, this tool is intentionally simple.
