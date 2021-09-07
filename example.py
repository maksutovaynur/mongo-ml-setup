import pandas as pd
import pymongo as pm
import sys
from ml_mongo import DbTable


db = DbTable("mongodb://localhost:27017", "my_database", "iris")
db.create_index("Index", pm.ASCENDING, unique=True)
db.create_index("sepal_length", pm.ASCENDING, unique=False)
db.create_index("species", pm.TEXT, unique=False)

command = sys.argv[1]

if command == "populate":
    iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
    print(iris.head())
    print(f"#{len(db.insert_by_chunks((r._asdict() for r in iris.itertuples(index=True))).inserted_ids)} new docs inserted")
elif command == "filter":
    print(',\n'.join(map(str, db.find_many(
            {
                'species': 'setosa',
                'petal_length': {'$gt': 1.2},
                'sepal_width': {'$lte': 3.4},
                'Index': {'$in': [10, 11, 12, 13, 14, 15]}
            }
    ))))
elif command == 'insert':
    print(db.insert_one({'Index': 999, 'additional_field': ['val1', 'val2', 'val3'], 'species': 'virginica'}).inserted_id)
elif command == 'remove':
    print(db.remove_many({'additional_field': 'val1'}))
