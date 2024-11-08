# rangeutils

`rangeutils` is a Python package that provides utilities for converting, manipulating, and processing Python `range` objects and boolean lists. This package includes a variety of functions to convert between boolean lists and ranges, merge adjacent ranges, find complementary ranges, and trim ranges based on specific conditions.

## Features

- **Convert lists to ranges**: Convert `[start, end]` lists to Python range objects, with optional handling for `None` values.
- **Boolean list to ranges**: Converts a boolean list to a list of range objects representing `True` or `1` sequences.
- **Ranges to boolean list**: Converts a list of ranges back to a boolean list of specified length.
- **Flip ranges**: Generate complementary ranges that are not covered by input ranges.
- **Fill ranges**: Fill ranges that are within a specified gap size.
- **Trim ranges**: Perform trimming on ranges based on length, percentage, or a specified trimming size.

## Installation

You can install `rangeutils` using pip:

```bash
pip install rangeutils
