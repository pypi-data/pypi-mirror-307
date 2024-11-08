# 2) Tutorial -  Advanced integration of a data set

## General workfow steps

Convert data and manage quality

- Convertion to numerical format
- define units of entities
- Recognizable identifiers for regions (ISO + predefined regions)

Mapping of meta data

- Mapping to required meta data: entity, category, scenario, model, source
- Storing additional meta data as required
- Tracking of who processed the data and when
- Origin of data ( URL for download or website)

Transparent documentation of read-in (ToDo)

## Data download
Human development index from https://hdr.undp.org/data-center

Old file name: "HDR21-22_Composite_indices_complete_time_series.csv"


## Understanding the data structure
- What is the naming convention?
- Is the data structured in columns or rows?
- What is the bests approach to read the required data?
- How to approach the conversion to the naming convention?


## Excercises: Data Read-in

Steps:

- Download meta data
- Find mapping for column names to extract the indices for the individual 
datatables
- Extract data for
   - Inequality-adjusted Human Development index
   - Gender Inequality Index
   - Life Expectancy at Birth (years)
   - Gross National Income Per Capita (2017 PPP$)
- Create data source and commit table   

````


----- Solution below ----



















import os
import datatoolbox as dt
import pandas as pd


# config
year = 2024
source = f'HDI_{year}'
raw_folder = "/Users/andreasgeiges/Downloads"


# reading raw data
data_file = os.path.join(raw_folder, 'HDR23-24_Composite_indices_complete_time_series.csv')
meta_file = os.path.join(raw_folder, 'HDR23-24_Composite_indices_metadata.xlsx')


# mapping of entity naming
entity_mapping  = {'hdi' : 'Human_development_index',
                   'gii' : 'Gender_inequality_index',
                  'le' : 'Life_expectandy_birth', #Life Expectancy at Birth (years)
                  'gnipc' : 'Gross_national_income_per_capity', #Gross National Income Per Capita 
                }
                
# mapping of units
unit_mapping  = {'hdi' : '',
                   'gii' : '',
                  'le' : 'years',
                  'gnipc' : 'USD_ppp_2017'
                }
              
              
# convert  index to regional ISO codes

data = pd.read_csv(data_file, index_col=list(range(4)),encoding = "ISO-8859-1")
index_to_read = data.index.unique('iso3').intersection(dt.mapping.getValidSpatialIDs())

# extract individual entities

tables_to_commit = list()

# loop over individual entitiess
for code, code_name in entity_mapping.items():

    # select columns of entity
    columns_to_read = [col for col in data.columns if col[:-5] == code]
    
    # subselect data
    df = data.loc[index_to_read,columns_to_read]
    
    # prepare columns as integer yearss
    df.columns = [int(x.split('_')[1]) for x in df.columns]
    
    # prepare index

    df = df.idx.project('iso3')
    
    meta ={'entity' : code_name,
           'scenario' : 'Historic',
           'source' : source,
           'unit' : unit_mapping[code]} 
    

    #create and add table

    table = dt.Datatable(df, meta = meta)
    
    tables_to_commit.append(table)       
    
    
    
# create source meta


sourceMeta = {
    'SOURCE_ID':source,
    'collected_by': 'AG',
    'date': dt.core.get_date_string(),
    'source_url': 'http://hdr.undp.org/en/data',
    'licence': 'open source',
}

# commit final tables
dt.commitTables(tables_to_commit, sourceMetaDict = sourceMeta, message='HDI_2024 data')
    
```

