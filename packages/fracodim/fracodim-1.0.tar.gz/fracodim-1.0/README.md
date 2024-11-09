# Fractal Correlation Dimension Estimator

This package estimates the correlation dimesion of any N-dimensional dataset.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install fracodim.

```bash
pip install fracodim
```

## Usage

```python
import fracodim

dataset = [[a0,a1,...,an], [b0,b1,...,bn], ...]

fracodim.CorrelationDimension(dataset) # returns a float estimate of the correlation dimension

```

The package accepts N-ary datasets, where each point can have n coordinates.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)