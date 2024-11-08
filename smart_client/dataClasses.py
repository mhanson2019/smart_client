from KeyManagement.getKeys import main as getKeys
import smartsheet as sm
import os, requests

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
    # refactor on 2024-11-06 to separate filtering and getting sheet
    def filter_sheet(self, returnMap = False):
        """Filter a sheet based on a dictionary of column filters"""
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

        if returnMap:
            return self.sheetFiltered, self._colMap
        else:
            return self.sheetFiltered
    
    def get_attachments(self, attachDict: dict, directory: str):
        """
        Download attachments from a dictionary of attachment IDs into a directory
         - attachDict: {filename: attachmentID}
        """
        for file in attachDict.keys():
            urlObj = self.client.Attachments.get_attachment(self._sheetID, attachDict[file])
            self.client.Attachments.download_attachment(urlObj, f"{directory}")
            print (f"Attachment {file} downloaded into {directory}")
            
    def update_rows(self, updateDict: dict):
        """
        Update specified cells from select rows in the sheet
         - updateDict: {rowID: {colID: {value: value, link: optional}}
        """
        rowUpdateList = []
        
        for r, value in updateDict.items():
            update_row = sm.models.Row()
            update_row.id = r
            
            for col, val in value.items():
                update_cell = sm.models.Cell()
                update_cell.column_id = col
                
                if type(val['value']) == dict:
                    update_cell.value = str(val['value'])
                else:
                    update_cell.value = val['value']
                if 'link' in val.keys():
                    update_cell.hyperlink = {'url': val['link']}
                
                update_row.cells.append(update_cell)    
                    
            rowUpdateList.append(update_row)
        
        self.client.Sheets.update_rows(self._sheetID, rowUpdateList)

    def add_attachment(self, attchDict: dict):
        """
        Add attachments to rows in the sheet based on an input dictionary
         - attachDict: {rowID: {file: value}}
        """
        successList = []
        failList = []
        for rowID, attachList in attchDict.items():
            
            for file in attachList:
                # get file type from extension
                fileExt = file.split('.')[-1]
                response = self.client.Attachments.attach_file_to_row(self._sheetID, rowID, 
                                                                    (os.path.basename(file), open(file, 'rb'), 
                                                                    'application/'+fileExt))
                if response.message == 'SUCCESS':
                    print(f"Attachment added to row {rowID}")
                    successList.append(file)
                else:
                    print(f"Attachment failed to add to row {rowID}")
                    failList.append(file)
        return (successList, failList)
            
    def add_discussion(self, commentDict: dict):
        """
        Add comment to specified cells from select rows in the sheet
         - commentDict: {rowID: discussion object}
        """
        for r, value in commentDict.items():
            self.client.Discussions.create_discussion(self._sheetID, r, value)
    
    def add_image(self, row_id, col_id, image_url):
        """
        Add image to specified cells from select rows in the sheet
         - updateDict: {rowID: {colID: value}}
        """
        sheet_id = self._sheetID
        file_type = os.path.basename(image_url).split('.')[-1]
        self.client.Cells.add_image_to_cell(sheet_id, row_id, col_id, image_url, file_type)
    
    @staticmethod
    def download(url: str, dest_folder: str, filename: str):
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)  # create folder if it does not exist

        #filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
        file_path = os.path.join(dest_folder, filename)

        r = requests.get(url, stream=True)
        if r.ok:
            print("saving to", os.path.abspath(file_path))
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
        else:  # HTTP status code 4XX/5XX
            print("Download failed: status code {}\n{}".format(r.status_code, r.text))
    
    @staticmethod
    def getRowAttachID(client, sheetID, rowID):
        """Method for downloading designated row attachment to temporary local data dir"""
        attachObj = client.Attachments.list_row_attachments(sheetID, rowID)
        attachID = [a.id for a in attachObj.data]
        attachNames = [a.name for a in attachObj.data]
        return(attachID, attachNames)
    
    @staticmethod
    def downloadAttach(client, sheetID, attachID, localDir):
        """use sheet and attachID to download attach to localDir"""
        if not os.path.isdir(localDir): os.makedirs(localDir)
        response = client.Attachments.get_attachment(sheetID, attachID)
        DataHandler.download(url=response.url, dest_folder=localDir, filename=response.name)
    
if __name__ == "__main__":
    key = ""
    actions = DataHandler(key)
    actions.sheetID = "3445054769155972"
    actions.colFilter = {'Registered': None}
    #sheet = actions.get_sheet()
    
    attchDict = {'ATLX-01_1.pdb': 8346171275956100}
    actions.get_attachments(attchDict, './')
    pass
        
        
        
