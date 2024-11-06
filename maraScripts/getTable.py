import smartsheet as sm
import os
import ast
import pandas as pd


def get_sheet(sheetID, api_key = None, filter = None):
    """Get a sheet by ID"""
    api_key = api_key
    client = sm.Smartsheet(api_key)
    sheetRaw = client.Sheets.get_sheet(sheetID)
    colMap = {x.title: x.id for x in sheetRaw.columns}
    colMapInv = {v: k for k, v in colMap.items()}
    
    if filter is not None:
        rowIDselect = []
        for i, (key, value) in enumerate(filter.items()):
            colID = colMap[key]
            
            rows = [x for x in sheetRaw.rows if x.get_column(colID).value in value]
            rows = [x.id for x in rows]
            
            if i == 0:
                rowIDselect.extend(rows)
            else:
                # find intersection of new filter and previous filter
                rowsN = set(rows)
                rowsO = set(rowIDselect)
                rowIDselect = list(rowsN.intersection(rowsO))
        
        sheetFiltered = [x for x in sheetRaw.rows if x.id in rowIDselect]
    
    return sheetFiltered, colMap, colMapInv

def sheet_to_df(sheet, column_names: list = None):
    """Convert a sheet to a pandas DataFrame
        with column names as the column values
    """
    data = []
    for row in sheet:
        row_data = []
        for cell in row.cells:
            row_data.append(cell.value)
        row_data.append(row.id)
        data.append(row_data)
    
    df = pd.DataFrame(data)
    df.columns = column_names
    print(df)
    return df

def run(sheetID, api_key = None, filter = None):
    if type(filter) == str:
        # convert string to dictionary
        filter = ast.literal_eval(filter)
        
    sheet, colMap, colMapInv = get_sheet(sheetID, api_key, filter)
    colnames = list(colMap.keys())
    colnames.append('RowID')
    df = sheet_to_df(sheet, colnames)
    
    # reduce the columns to only those listed
    colList = ["CompoundID", "smiles", "CDD name", 
               "Vendor / Location", "Collection", 
               "Docked", "Structural Model", "Score"]
    df = df[colList]
    # write to csv 
    # df.to_csv('data.csv', index =
    filename = f"{sheetID}-{filter}.csv"
    # convert to csv with an index column 
    df.to_csv(filename, index = True)
    print(df)
    return filename

if __name__ == '__main__':
    sheetID = '6827322187403140'
    api_key = 'WXV5WGHPI6pwgWSn1MfeInJy2bJMqt2SknsOb'
    filter = "{'Source': ['Atelier']}"
    df = run(sheetID, api_key, filter)
    print(df)