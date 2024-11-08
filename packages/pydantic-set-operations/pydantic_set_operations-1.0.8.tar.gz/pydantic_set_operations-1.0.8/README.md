# Pydantic-Set-Operations

`Pydantic-Set-Operations` provides an enhanced version of Pydantic's `BaseModel`, allowing for advanced model manipulations, such as field unions, exclusions, and intersections. `ExtendedBaseModel` introduces bitwise operations (like `|`, `&`, and `-`) for combining, intersecting, and excluding fields between models.

This package is ideal for projects that require dynamic model restructuring or filtering based on specific fields.

### Key Model Features

1. **Field Union (`union` method)**: Combines fields from two models, prioritizing fields from the initiating model if overlaps exist.
2. **Field Exclusion (`omit` method)**: Creates a new model excluding specified fields or fields present in another model.
3. **Field Intersection (`pick` method)**: Creates a model containing only fields shared between two models.

### Key Instance Features

1. **Field Union (`|` operator)**: Returns an instance combining fields from both instances.
2. **Field Exclusion (`-` operator)**: Returns an instance excluding fields present in another instance.
3. **Field Intersection (`&` operator)**: Returns an instance containing only fields shared between two instances.

## Installation

Install using `pip install -U pydantic-set-operations`.

## Usage

For more info about how to use this package, please visit the [Wiki](https://github.com/P1etrodev/pydantic-set-operations/wiki).