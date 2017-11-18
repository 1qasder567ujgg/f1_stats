import datetime

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import MySQLdb as mysql

import db_settings.py

SQLTrain = \
'SELECT  \
    r.circuitId, \
    res.constructorId,  \
    DATEDIFF(r.date, d.dob) AS Age, \
    res.grid, \
    CASE  \
        WHEN r.round = 1 THEN 1 \
        ELSE 0 \
    END AS FirstRound, \
    (SELECT COUNT(*)  \
        FROM f1db.results res1 \
        INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
     WHERE res1.driverId = res.driverId \
     AND r1.date < r.date) AS TotalGP, \
    (SELECT COUNT(*)  \
        FROM f1db.results res1 \
        INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
     WHERE res1.driverId = res.driverId \
     AND res1.constructorId = res.constructorId \
     AND r1.date < r.date) AS TotalGPWTeam, \
    IFNULL((SELECT AVG(res1.position)  \
        FROM f1db.results res1 \
        INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
     WHERE res1.driverId = res.driverId \
     AND r1.date < r.date), 0) AS AvgPos, \
    IFNULL((SELECT AVG(res1.position)  \
        FROM f1db.results res1 \
        INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
     WHERE res1.driverId = res.driverId \
     AND r1.year = r.year \
     AND r1.date < r.date), 0) AS AvgPosSeason, \
    (SELECT COUNT(*)  \
        FROM f1db.results res1 \
        INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
     WHERE res1.driverId = res.driverId \
     AND res1.position = 1 \
     AND r1.date < r.date) AS TotalWins, \
    (SELECT COUNT(*)  \
        FROM f1db.results res1 \
        INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
     WHERE res1.driverId = res.driverId \
     AND res1.position = 1 \
     AND r1.year = r.year \
     AND r1.date < r.date) AS TotalWinsSeason, \
    IFNULL((SELECT AVG(res1.grid)  \
        FROM f1db.results res1 \
        INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
     WHERE res1.driverId = res.driverId \
     AND r1.date < r.date), 0) AS AvgGrid, \
    IFNULL((SELECT AVG(res1.grid)  \
        FROM f1db.results res1 \
        INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
     WHERE res1.driverId = res.driverId \
     AND r1.year = r.year \
     AND r1.date < r.date), 0) AS AvgGridSeason, \
    (SELECT COUNT(*)  \
        FROM f1db.results res1 \
        INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
     WHERE res1.driverId = res.driverId \
     AND res1.grid = 1 \
     AND r1.date < r.date) AS TotalPoles, \
    (SELECT COUNT(*)  \
        FROM f1db.results res1 \
        INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
     WHERE res1.driverId = res.driverId \
     AND res1.grid = 1 \
     AND r1.year = r.year \
     AND r1.date < r.date) AS TotalPolesSeason, \
     CASE \
        WHEN res.position = 1 THEN 1 \
        ELSE 0 \
    END AS WinnerR, \
     CASE \
        WHEN res.grid = 1 THEN 1 \
        ELSE 0 \
    END AS WinnerQ \
      \
FROM f1db.results res \
INNER JOIN f1db.races r ON r.raceId = res.raceId AND r.year >= 2012 \
INNER JOIN f1db.drivers d ON d.driverId = res.driverId'

SQLPredict = ''

def mysql_conn_etl(dbName):
    db = mysql.connect(DB_HOST, DB_ETL_USER, DB_ETL_USER_PASSWORD, dbName)
    return db


def getModel(train, labels):
    data_train, data_test, label_train, label_test = train_test_split(train, labels, test_size=0.3, random_state=753)

    e = 100
    f = None
    n = 7
    s = 2

    model = RandomForestClassifier(n_estimators=e, \
                                   max_features=f, \
                                   min_samples_leaf=n, \
                                   min_samples_split=s, \
                                   oob_score=True, random_state=753)

    model.fit(data_train, label_train)
    score = model.score(data_test, label_test)    
    return score


print(datetime.datetime.today(), 'Start')

db = mysql_conn_etl(DB_NAME)
df = pd.read_sql(SQLTrain, con=db)
db.close()

print(datetime.datetime.today(), 'Data loaded')

commonCols = ['circuitId', 'constructorId', 'Age', 'FirstRound', 'TotalGP', 'TotalGPWTeam']
raceCols = ['grid', 'AvgPos', 'AvgPosSeason', 'TotalWins', 'TotalWinsSeason', \
            'AvgGrid', 'AvgGridSeason', 'TotalPoles', 'TotalPolesSeason']
raceLabelCol = ['WinnerR']
qualCols = ['AvgGrid', 'AvgGridSeason', 'TotalPoles', 'TotalPolesSeason']
qualLabelCol = ['WinnerQ']

dfRace = df[commonCols + raceCols + raceLabelCol]

dfQual = df[commonCols + qualCols + qualLabelCol]

# print(dfRace.corr()[raceLabelCol[0]].sort_values(ascending=False))
# print(dfQual.corr()[qualLabelCol[0]].sort_values(ascending=False))

dfRaceLabels = dfRace.pop(raceLabelCol[0])
dfQualLabels = dfQual.pop(qualLabelCol[0])

print(datetime.datetime.today(), 'DFs ready')

print(datetime.datetime.today(), 'Qual model score', getModel(dfQual, dfQualLabels))
print(datetime.datetime.today(), 'Race model score', getModel(dfRace, dfRaceLabels))