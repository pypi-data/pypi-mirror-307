from enum import Enum

class IntegrationTypes(Enum):
    CSV = 'CSV'
    EXCEL = 'EXCEL'
    GOOGLESPREADSHEET = 'GOOGLE SPREADSHEET'

class IntegrationModes(Enum):
    READ = 'READ'
    WRITE = 'WRITE'