#importing all needed libarires
import pandas as pd

from tableau_api_lib import TableauServerConnection
from tableau_api_lib.utils.querying import get_projects_dataframe

from tableauhyperapi import HyperProcess, Connection, TableDefinition, SqlType, Telemetry, Inserter, CreateMode, TableName
from tableauhyperapi import escape_string_literal

import tableauserverclient as TSC

#Get the data; read in csv file
filename = pd.read_csv(['file name goes here'], usecols = ['read in appropriate columns needed'])


#convert all datetime values to appropriate type
#convert data types into their appropriate types and formats
#an example below to convert date
filename['date'] = filename['date'].apply(pd.to_datetime)



# get a list of column names from the csv file
colnames =filename.columns

# get a list of column typesfrom the csv file
coltypes =filename.dtypes

#the above would help with the definition of the schema

#specifying the various data type to be used to define the schema 
field = { 
    'float64' :     SqlType.double(), 
    'float32' :     SqlType.double(),
    'int64' :       SqlType.double(),
    'int32' :       SqlType.double(),
    'object':       SqlType.text(),
    'bool':         SqlType.bool(),
    'datetime64[ns, UTC]':   SqlType.date(),
}


# for each column, add the appropriate info for the Table Definition
column_names = []
column_type = []
for i in range(0, len(colnames)):
    cname = colnames[i] #header of column
    coltype = coltypes[i] #pandas data type of column
    ctype = field.get(str(coltype)) #get corresponding sql column type 

    #store in lists to used for column and schema
    column_names.append(cname)
    column_type.append(ctype)


#name and path to save extract temporarily
PATH_TO_HYPER = 'hyper_extract.hyper'

# Step 1: Start a new private local Hyper instance
with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU, 'myapp' ) as hyper:

# Step 2:  Create the the .hyper file, replace it if it already exists
    with Connection(endpoint=hyper.endpoint, 
                    create_mode=CreateMode.CREATE_AND_REPLACE,
                    database=PATH_TO_HYPER) as connection:

# Step 3: Create the schema(empty)
        connection.catalog.create_schema('Extract')


# Step 4: Create the table definition
        #defining the columns according to the dataframe
        cols = []
        for i, j in zip(column_names, column_type):
            columns = TableDefinition.Column(i, j)
            cols.append(columns)


        #creating schema 
        schema = TableDefinition(table_name=TableName('Extract','Extract'),
                columns= cols)

# Step 5: Create the table in the connection catalog
        connection.catalog.create_table(schema)
    
        with Inserter(connection, schema) as inserter:
            for index, row infilename.iterrows():
                inserter.add_row(row)
            inserter.execute()

    print("The connection to the Hyper file is closed.")     


# Establish a connection to Tableau Server and publish the extract to Tableau Server incase your firm using the Server, else see the authentication to Tableau Online below

tableau_auth = TSC.PersonalAccessTokenAuth('name of API goes here', 'your token secret goes here')
server = TSC.Server('site address')

'''

# Establish a connection to Tableau Online and publish the extract to Tableau Online

tableau_auth = TSC.PersonalAccessTokenAuth('name of API goes here', 'your tokensecret goes here', 'name of site')
server = TSC.Server('site address')

'''

#allow user to input project name for datasource to be published; that is identify the mother project folder to publish the datasource on the server
datasource = input(str('enter name of datasource project directory to publish datasource '))


with server.auth.sign_in(tableau_auth):

     # fetch the corresponding project id 
    ID = ''


    all_project_items, pagination_item = server.projects.get()
    for proj in all_project_items:
        if proj.name == datasource:
            ID = proj.id

    # Use the project id to create new datsource_item
    new_datasource = TSC.DatasourceItem(ID)

    # publish data source (specified in file_path)
    new_datasource = server.datasources.publish(
                    #new_datasource, PATH_TO_HYPER, 'CreateNew')
        
    '''#since datasource exist from prior publish, overwrite it 
    new_datasource = server.datasources.publish(
                    new_datasource, PATH_TO_HYPER, 'Overwrite')'''

#signing out of the tableau server
print('Publishing completed')
server.auth.sign_out()
