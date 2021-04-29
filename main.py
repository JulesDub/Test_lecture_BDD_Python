import psycopg2
import pandas as pd

import psycopg2

def main() :
    data_list_a = csv_cleaner("CSV_file/import_colonies_fev2021.csv", "secteur_nom_fr", "longitude", "latitude", ";")
    conn = psycopg2.connect("dbname=simm_lieux port=5432 user=super_user password=admin")
    print("Database opened successfully")
    cur = conn.cursor()
    i = len(data_list_a)
    for x in range (i) :
        sql = f"""INSERT INTO lieux_site_web(LIEU_LIBELLE) VALUES ('{data_list_a[x][0]}') """
        cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("La connexion PostgreSQL est fermée")


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
    main()