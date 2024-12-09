import pandas as pd

def convert_to_json(cell_value):
    """
    Converts a cell value to a JSON-compatible list.
    """
    if pd.isna(cell_value) or not cell_value.strip():
        return []
    return [item.strip() for item in cell_value.split(',')]
