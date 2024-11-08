#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Provide common helper functions."""

import csv
import json


def read_csv(
    file_name: str
) -> list:
    """Read CSV file and convert to dictionaries."""
    with open(file_name, 'r') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    return data


def dicts_to_csv(
    data: list
) -> list:
    """Convert dicts data to CSV list."""
    csv_data = [list(data[0].keys())]
    for row in data:
        csv_data.append(list(row.values()))
    return csv_data


def export_csv(
    data: list,
    file: str
) -> None:
    """Export data to CSV file."""
    with open(file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def read_json(
    file_name: str
) -> dict:
    """Read JSON file."""
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data


def write_json_dict(
    file_name: str,
    data: dict
) -> None:
    """Write JSON to file."""
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4, default=str)


def write_json_str(
    file_name: str,
    data: str
) -> None:
    """Write JSON strings to file."""
    with open(file_name, 'w') as f:
        f.write(data)


def main():
    """Execute main function."""
    pass


if __name__ == '__main__':
    main()
