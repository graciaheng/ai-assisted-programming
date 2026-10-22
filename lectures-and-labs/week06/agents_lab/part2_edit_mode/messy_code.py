"""
Messy Code - Refactor me!

This code works but is poorly written. Use Copilot Edit mode to refactor it.

Instructions:
1. Select all the code
2. Press Ctrl+I / Cmd+I
3. Ask Copilot to refactor following best practices
4. Compare before and after
"""

import json


def calc(numbers):
    """Return the average, maximum, minimum, and sum of the numbers."""
    total = 0
    maximum = 0
    minimum = 0

    for number in numbers:
        total += number
        if number > maximum:
            maximum = number
        if minimum == 0:
            minimum = number
        elif number < minimum:
            minimum = number

    average = total / len(numbers)
    return {
        'avg': average,
        'max': maximum,
        'min': minimum,
        'sum': total,
    }


def _process_active_record(record):
    """Build the processed representation of an active record."""
    value = record['value']
    return {
        'id': record['id'],
        'value': value * 1.1,
        'priority': 'high' if value > 100 else 'low',
    }


def proc_data(data):
    """Process and return only active records."""
    processed_records = []
    for record in data:
        if record['status'] == 'active':
            processed_records.append(_process_active_record(record))
    return processed_records


def _partition_by_status(records):
    """Split records into active and inactive lists."""
    active_records = []
    inactive_records = []

    for record in records:
        if record['status'] == 'active':
            active_records.append(record)
        else:
            inactive_records.append(record)

    return active_records, inactive_records


def get_stuff(filename):
    """Load records from a JSON file and split them by status."""
    with open(filename, 'r') as input_file:
        records = json.load(input_file)

    return _partition_by_status(records)


# Test code
if __name__ == '__main__':
    numbers = [10, 20, 30, 40, 50]
    result = calc(numbers)
    print(result)

    data = [
        {'id': 1, 'status': 'active', 'value': 150},
        {'id': 2, 'status': 'active', 'value': 80},
        {'id': 3, 'status': 'inactive', 'value': 200},
    ]

    processed = proc_data(data)
    print(processed)
