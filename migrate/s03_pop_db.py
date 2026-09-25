#imports
import pandas as pd
import numpy as np
from psycopg2.extras import execute_values
from psycopg2 import sql
from s02_init_db import connect_with_retry
from s01_download_n_unzip import static_pth 


#read all 11 .csv files rand transform into pandas datasets.
all_dfs = {}

for f in static_pth.glob('*.csv'):
    all_dfs[f.stem] = pd.read_csv(f)
#create table names called the filename and column names = column names. 
#   done 

#all_dfs.keys()
#dict_keys(['calendar_dates', 'stop_times', 'stops', 'calendar', 'shapes', 'trip_notes', 'trips', 'agency', 'routes', 'translations'])

#importing agency
del all_dfs['feed_info'] #skipped completely
all_dfs.keys()

conn = connect_with_retry()

with conn.cursor() as cursor:
    translations_df = all_dfs['translations']
    
    #for why this is nessecary see migrate/big_fat_schema.sql around where these two dfs respective tables are defined.
    stop_translations = translations_df[
        (translations_df['table_name'] == 'stops') &
        (translations_df['field_name'] == 'stop_name')][['record_id', 'language', 'translation']].copy()

    stop_translations['record_id'] = ( #somehow turns into float values, and failing on FK with another table
        pd.to_numeric(stop_translations['record_id'], errors='coerce').astype(int).astype(str)
    )
    
    stop_translations = stop_translations.rename(columns={'record_id':'stop_id'})

    headsign_translations = translations_df[
        (translations_df['table_name'] == 'trips') &
        (translations_df['field_name'] == 'trip_headsign')][['field_value', 'language', 'translation']].rename(columns={'field_value':'original'}) 
    
    #merge translation dfs w renamed columns back 
    all_dfs['stops_translations'] = stop_translations
    all_dfs['trips_headsign_translations'] = headsign_translations
    
    #cleanup
    del all_dfs['translations']

    for table_name, df in all_dfs.items():
        df_cleaned = df.where(df.notnull(), None)
        columns = list(df_cleaned.columns) #col_names
    
        
        records = [
            tuple(None if(isinstance(val, float) and np.isnan(val)) or str(val).lower() == 'nan' else val for val in row) #clenaing float nans
            for row in df_cleaned.itertuples(index=False, name=None)
        ]

        q = sql.SQL("""INSERT INTO {table} ({fields}) VALUES %s""").format(
            table = sql.Identifier(table_name),
            fields = sql.SQL(',').join(map(sql.Identifier, columns))
        )
        execute_values(cursor, q, records)

        print(f"{table_name} is done")
    #re adding these fk constraints i commented out earlier bc issues with blk importing the data. since we have zero orphans, we can do it now :)
    q = """
    ALTER TABLE trips
    ADD CONSTRAINT fk_trips_routes
    FOREIGN KEY (route_id) REFERENCES routes(route_id);


    ALTER TABLE stop_times
    ADD CONSTRAINT fk_stop_times_trips
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id);



    ALTER TABLE stop_times
    ADD CONSTRAINT fk_stop_times_stops
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id);


    ALTER TABLE trip_notes
    ADD CONSTRAINT fk_trip_notes_trips
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id);
    """
    cursor.execute(q)
    conn.commit()
conn.close()