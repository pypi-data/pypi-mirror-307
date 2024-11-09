# CosinorAge

[![Documentation Status](https://readthedocs.org/projects/cosinorage/badge/?version=latest)](https://cosinorage.readthedocs.io/en/latest/?badge=latest)

A Python package that calculates **CosinorAge**.

## Environment

## Installation

Clone the repository and install the package with:

```bash
git clone https://github.com/yourusername/cosinorage.git
cd cosinorage
pip install .
```

## Package Functionalities

### Data Loading

`AccelerometerDataLoader` object can be used to load raw accelerometer data from a directory containing hourly csv
files.

```python
reader = AccelerometerDataLoader(input_dir_path='../data/62164/')
```

The `ENMODataLoader` object can be used to load minute-level ENMO data from a csv file.

```python
reader = ENMODataLoader(input_file_path='../data/62164.csv')
```

The `load_data()` method reads the data from the input directory/file and calculates minute-level ENMO values (if not
already available) and stores it in a pandas DataFrame.

```python
acc_reader.load_data()
```

The `save_data()` method saves the minute-level data to a csv file.

```python
acc_reader.save_data(output_file_path='../data/62164_ENMO.csv')
```

### Preprocessing

### Wearable Feature Computation

### Biological Age Prediction

### CosinorAge Computation
