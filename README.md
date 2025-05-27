# Root Locus Plotter

A simple Python script that replicates MATLAB's `rlocus` function by taking a transfer function in LaTeX form from the terminal and plotting its root locus diagram.

## Setup

This project uses a virtual environment to manage dependencies:

```bash
# Activate the virtual environment
source venv/bin/activate

# If you need to install dependencies
pip install control numpy matplotlib sympy
```

## Usage

Run the script from the command line:

```bash
python rootlocus.py
```

You can either:
1. Provide the transfer function as a command-line argument:
   ```bash
   python rootlocus.py "\frac{s^2 + 3s + 2}{s^3 + 4s^2 + 5s + 2}"
   ```

2. Or enter it when prompted after running the script without arguments.

## Input Format

The transfer function should be in LaTeX format, for example:
- `\frac{s^2 + 3s + 2}{s^3 + 4s^2 + 5s + 2}`
- `\frac{1}{s^2 + 2s + 1}`
- `\frac{s + 1}{s^2 + 3s + 2}`

## Example

```bash
python rootlocus.py "\frac{s + 1}{s^2 + 2s + 1}"
```

This will display the root locus plot for the given transfer function.
