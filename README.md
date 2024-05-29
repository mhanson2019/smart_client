# smart_client

This code integrates the KeyManagement module with Smartsheet's API to manage and manipulate data in Smartsheet sheets.

## Classes

### `SmShBase`

A base class for interacting with Smartsheet API.

#### Methods

- `__init__(self, key=None)`: Initializes the `SmShBase` class with an API key.

  - `key` (str, optional): The key to retrieve the API key from the KeyManagement module.

### `DataHandler`

A class for handling data operations on Smartsheet sheets. Inherits from `SmShBase`.

#### Methods

- `__init__(self, key=None)`: Initializes the `DataHandler` class and sets up the Smartsheet client.

  - `key` (str, optional): The key to retrieve the API key from the KeyManagement module.

- `get_sheet(self)`: Retrieves a sheet by its ID and filters rows based on the column filter.

  - **Returns**: A list of filtered rows if a column filter is provided; otherwise, returns all rows.

- `update_rows(self, updateDict: dict)`: Updates specified cells in select rows in the sheet.

  - `updateDict` (dict): A dictionary where keys are row IDs and values are dictionaries of column IDs and cell values. Example: `{rowID: {colID: value}}`

#### Properties

- `sheetID`: Gets or sets the sheet ID for the Smartsheet.
- `colFilter`: Gets or sets the column filter for filtering rows in the sheet.

## Example Usage

```python
if __name__ == "__main__":
    key = "your_api_key_here"
    actions = DataHandler(key)
    actions.sheetID = "your_sheet_id_here"
    actions.colFilter = {'ColumnTitle': ['FilterValue1', 'FilterValue2']}
    
    # Get the filtered sheet
    sheet = actions.get_sheet()
    
    # Update rows
    update_dict = {
        row_id: {
            col_id: {'value': new_value, 'link': 'optional_link'}
        }
    }
    actions.update_rows(update_dict)
