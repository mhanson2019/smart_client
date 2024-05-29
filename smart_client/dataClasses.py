from KeyManagement.getKeys import main as getKeys
import smartsheet as sm

class SmShBase:
    def __init__(self, key = None):
        self.__api_key = getKeys(key)['SmartSheet']
        self.__client = sm.Smartsheet(self.__api_key)

class DataHandler(SmShBase):
    def __init__(self,key = None):
        super().__init__(key)
        self.client = self._SmShBase__client
        self._sheetID: str
        self._colFilter: dict
        self.sheetRaw: sm.models.Sheet
        self.sheetFiltered: list
        self._colMap: dict
        self._colMapInv: dict
        
    @property
    def sheetID(self):
        return self._sheetID
    @sheetID.setter
    def sheetID(self, value):
        self._sheetID = value
    
    @property
    def colFilter(self):
        return self._colFilter
    @colFilter.setter
    def colFilter(self, value):
        self._colFilter = value
    
    def get_sheet(self):
        """Get a sheet by ID"""
        self.sheetRaw = self.client.Sheets.get_sheet(self._sheetID)
        self._colMap = {x.title: x.id for x in self.sheetRaw.columns}
        self._colMapInv = {v: k for k, v in self._colMap.items()}
        if self._colFilter:
            rowIDselect = []
            for i, (key, value) in enumerate(self._colFilter.items()):
                colID = self._colMap[key]
                
                rows = [x for x in self.sheetRaw.rows if x.get_column(colID).value in value]
                rows = [x.id for x in rows]
                
                if i == 0:
                    rowIDselect.extend(rows)
                else:
                    # find intersection of new filter and previous filter
                    rowsN = set(rows)
                    rowsO = set(rowIDselect)
                    rowIDselect = list(rowsN.intersection(rowsO))
            
            self.sheetFiltered = [x for x in self.sheetRaw.rows if x.id in rowIDselect]
        else:
            self.sheetFiltered = self.sheetRaw.rows
        
        return self.sheetFiltered

    def update_rows(self, updateDict: dict):
        """
        Update specified cells from select rows in the sheet
         - updateDict: {rowID: {colID: value}}
        """
        rowUpdateList = []
        
        for r, value in updateDict.items():
            update_row = sm.models.Row()
            update_row.id = r
            
            for col, val in value.items():
                update_cell = sm.models.Cell()
                update_cell.column_id = col
                
                update_cell.value = val['value']
                if 'link' in val.keys():
                    update_cell.hyperlink = {'url': val['link']}
                
                update_row.cells.append(update_cell)    
                    
            rowUpdateList.append(update_row)
        
        self.client.Sheets.update_rows(self._sheetID, rowUpdateList)

    
if __name__ == "__main__":
    key = ""
    actions = DataHandler(key)
    actions.sheetID = ""
    actions.colFilter = {'Registered': None}
    sheet = actions.get_sheet()
    pass
        
        
        