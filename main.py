import pandas as pd
import psycopg2
import json
from flask import Flask, render_template, url_for


conn = psycopg2.connect("dbname=SIMM_LIEUX port=5432 user=admin password=admin")
cur = conn.cursor()

app = Flask(__name__)

@app.route('/')
def map_func():
    return render_template('home.html')

@app.route('/leaflet')
def leaflet():
    data_list_a = csv_cleaner("CSV_file/import_colonies_fev2021.csv", "secteur_nom_fr", "longitude", "latitude", ";")
    data_list_b = csv_cleaner("CSV_file/Export_Rinbio.csv", "LIEU_LIBELLE", "LONGITUDE", "LATITUDE", ",")
    print("Database opened successfully")
    df = create_pandas_table(
        "SELECT LIEU_LIBELLE, st_asgeojson(lieu_position_point), lieu_dispositif FROM lieux_site_web")
    data_from_db = df.values.tolist()
    for i in range(len(data_from_db)):
        data_from_db[i][1] = json.loads(data_from_db[i][1])
    '''write_SQL(data_list_a, 159)
    write_SQL(data_list_b, 117)
    conn.commit()
    cur.close()
    conn.close()'''
    print("Database closed successfully")
    return render_template('leaflet.html', data=json.dumps(data_from_db))


def write_SQL(list_csv, dispositif):
    for x in range(len(list_csv)):
        sql_write_tab = f"""
        INSERT INTO LIEUX_SITE_WEB(lieu_libelle, lieu_position_point, lieu_dispositif) 
            VALUES 
            ('{list_csv[x][0]}',
            'POINT({list_csv[x][2]} {list_csv[x][1]})',
            {dispositif});
        """
        cur.execute(sql_write_tab)

def create_pandas_table(sql_query, database = conn):
    table = pd.read_sql_query(sql_query, database)
    return table

def csv_cleaner(path_csv, nom, lng, lat, sep):
    data = pd.read_csv(path_csv, usecols=[nom, lng, lat], sep=sep, encoding="utf8")
    new_data = data.replace(["'", '		'], [" ", ''], regex=True)  # removing " ' " char and multiple spaces unwanted which create bug on json object
    new_data = new_data.dropna()  # for cleaning empty data in csv
    for x in new_data.index:
        if new_data.loc[x, lng] > 180:  # for cleaning wrong lng in csv
            new_data.drop(x, inplace=True)
        elif new_data.loc[x, lng] < -180:
            new_data.drop(x, inplace=True)
        if new_data.loc[x, lat] > 90:  # for cleaning wrong lat in csv
            new_data.drop(x, inplace=True)
        elif new_data.loc[x, lat] < -90:
            new_data.drop(x, inplace=True)
    data_frame_f = pd.DataFrame(new_data, columns=[nom, lat, lng])
    data_list_f = data_frame_f.values.tolist()
    return data_list_f

if __name__ == '__main__':
    app.run(debug=True)

"""    for x in range(len(data_list_b)):
        xp_a = x + 1
        xp_b = xp_a + len(data_list_a)
        sql_write_tab_b = f
        UPDATE lieux_site_web
        SET lieu_position_point = 'POINT({data_list_b[x][2]} {data_list_b[x][1]})', lieu_libelle = '{data_list_b[x][0]}'
        WHERE lieu_uid = {xp_b};
        """