import pandas as pd
import pymongo as pm
from ml_mongo import DbTable


iris = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

db = DbTable("mongodb://localhost:27017", "my_database", "iris")

db.create_index("Index", pm.ASCENDING, unique=True)
db.create_index("sepal_length", pm.ASCENDING, unique=False)
db.create_index("species", pm.TEXT, unique=False)

print(f"#{len(db.insert_by_chunks((r._asdict() for r in iris.itertuples(index=True))).inserted_ids)} new docs inserted")
