import logging
from os.path import abspath
from pathlib import Path
import pyprojroot
from decouple import config
from sqlalchemy import create_engine as ce
import numpy as np
import pandas as pd

logging.basicConfig(
    format = '%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s', 
    level=logging.DEBUG, 
    filename='alkemy.log',  
    encoding="utf-8"
    )

def insert_into():
    sql = '''INSERT INTO alkemy (cod_localidad, id_provincia, id_departamento, categoría, provincia, localidad, nombre, domicilio, código_postal, codigo_tel, teléfono, mail, web, fuente)
            VALUES 
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    CURRENT_DIR = pyprojroot.here('data')
    files = Path(str(CURRENT_DIR)).glob("**/*.csv")
    for f in files:
        logging.info(f)
        data = pd.read_csv(f,header = 0, sep = ',')
        if 'Departamento' in data.columns:
            data = data.drop(['Departamento'], axis=1)
        if 'Subcategoria' in data.columns:
            data = data.drop(['Subcategoria'], axis=1)
        if 'subcategoria' in data.columns:
            data = data.drop(['subcategoria'], axis=1)
        data = data.rename(columns={data.columns[0]: 'cod_localidad', 
                                    data.columns[1]: 'id_provincia',
                                    data.columns[2]: 'id_departamento',
                                    data.columns[3]: 'ojo',
                                    data.columns[4]: 'categoría',
                                    data.columns[5]: 'provincia',
                                    data.columns[6]: 'localidad',
                                    data.columns[7]: 'nombre',
                                    data.columns[8]: 'domicilio',
                                    data.columns[9]: 'piso',
                                    data.columns[10]: 'código_postal',
                                    data.columns[11]: 'codigo_tel',
                                    data.columns[12]: 'teléfono',
                                    data.columns[13]: 'mail',
                                    data.columns[14]: 'web',
                                    data.columns[15]: 'este',
                                    data.columns[16]: 'fue',
                                    data.columns[17]: 'un',
                                    data.columns[18]: 'comodin',
                                    data.columns[19]: 'fuente',})
        data = data.replace(['s/d'], np.nan)
        data = data.drop(['ojo', 'piso', 'este', 'fue', 'un', 'comodin'], axis=1)
        data = data.iloc[:, :14]
        list_data = data.values.tolist()
        cursor.executemany(sql, list_data)
        connection.commit()
        logging.info('archivo agregado a la tabla')

try:
    pg_engine = ce(config('engine_psql'))
    logging.info("Conexión exitosa.")
    connection = pg_engine.raw_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT version()")
    row = cursor.fetchone()
    logging.info("Versión del servidor de PostgreSQL: {}".format(row))
    with open(str(abspath('table_create.sql')), 'r', encoding='utf-8') as myfile:
        df = myfile.read()
        cursor.execute(df)
    insert_into()
    cursor.execute("select count(id), categoría from alkemy group by categoría order by count desc;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except Exception as ex:
    logging.error("Error durante la conexión: {}".format(ex))

finally:
    pg_engine.dispose()
    logging.info("La conexión ha finalizado.")
    


    