from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

import datetime

import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# from sklearn import preprocessing 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

import MySQLdb as mysql

import f1_stats.db_settings as f1db

class Command(BaseCommand):

    help = 'Creates prediction for a race'

    def handle(self, *args, **options):

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

        SQLPredict = \
        'SELECT  \
            res.driverId AS driver_id, \
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
             AND r1.date <= r.date) AS TotalGP, \
            (SELECT COUNT(*)  \
                FROM f1db.results res1 \
                INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
             WHERE res1.driverId = res.driverId \
             AND res1.constructorId = res.constructorId \
             AND r1.date <= r.date) AS TotalGPWTeam, \
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
             AND r1.date <= r.date), 0) AS AvgPosSeason, \
            (SELECT COUNT(*)  \
                FROM f1db.results res1 \
                INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
             WHERE res1.driverId = res.driverId \
             AND res1.position = 1 \
             AND r1.date <= r.date) AS TotalWins, \
            (SELECT COUNT(*)  \
                FROM f1db.results res1 \
                INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
             WHERE res1.driverId = res.driverId \
             AND res1.position = 1 \
             AND r1.year = r.year \
             AND r1.date <= r.date) AS TotalWinsSeason, \
            IFNULL((SELECT AVG(res1.grid)  \
                FROM f1db.results res1 \
                INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
             WHERE res1.driverId = res.driverId \
             AND r1.date <= r.date), 0) AS AvgGrid, \
            IFNULL((SELECT AVG(res1.grid)  \
                FROM f1db.results res1 \
                INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
             WHERE res1.driverId = res.driverId \
             AND r1.year = r.year \
             AND r1.date <= r.date), 0) AS AvgGridSeason, \
            (SELECT COUNT(*)  \
                FROM f1db.results res1 \
                INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
             WHERE res1.driverId = res.driverId \
             AND res1.grid = 1 \
             AND r1.date <= r.date) AS TotalPoles, \
            (SELECT COUNT(*)  \
                FROM f1db.results res1 \
                INNER JOIN f1db.races r1 ON r1.raceId = res1.raceId  \
             WHERE res1.driverId = res.driverId \
             AND res1.grid = 1 \
             AND r1.year = r.year \
             AND r1.date <= r.date) AS TotalPolesSeason \
        FROM f1db.results res \
        INNER JOIN f1db.races r ON r.raceId = res.raceId \
        INNER JOIN f1db.drivers d ON d.driverId = res.driverId \
        WHERE res.raceId = 985'

        FC_TABLE = 'forecast_forecast'

        def mysql_conn(dbName):
            db = mysql.connect(f1db.DB_HOST, f1db.DB_ETL_USER, f1db.DB_ETL_USER_PASSWORD, dbName)
            return db


        def tune_modelCV(X, y):
            # Подбор параметров для модели

            from sklearn.model_selection import GridSearchCV
            
            param_grid = { 'criterion' : ['gini', 'entropy'], \
                          'min_samples_leaf' : [1, 2, 5], \
                          'min_samples_split' : [2, 6, 10], \
                          'max_depth': [5, 10, 15], \
                          'n_estimators': [50, 100, 150], \
                          'max_features': ['auto', 'log2', None]}    

            model = RandomForestClassifier(oob_score=True, random_state=42, n_jobs=-1)
            
            gs = GridSearchCV(estimator=model, param_grid=param_grid, scoring='accuracy', verbose=1)
            
            gs = gs.fit(X, y)
            
            print(gs.best_score_)
            # print('\n')
            # print(gs.best_params_)
            # print(gs.cv_results_)


        def getModel(train, labels, params):
            # Создание модели

            data_train, data_test, label_train, label_test = train_test_split(train, labels, test_size=0.3, random_state=753)

            model = RandomForestClassifier(criterion=params['criterion'], \
                                           n_estimators=params['n_estimators'], \
                                           max_features=params['max_features'], \
                                           min_samples_leaf=params['min_samples_leaf'], \
                                           min_samples_split=params['min_samples_split'], \
                                           max_depth=params['max_depth'], \
                                           oob_score=True, random_state=753)

            model.fit(data_train, label_train)
            score = model.score(data_test, label_test)    
            return model, score


        print(datetime.datetime.today(), 'Start')
        # Общие признаки
        commonCols = ['circuitId', 'constructorId', 'Age', 'FirstRound', 'TotalGP', 'TotalGPWTeam']

        # Признаки для гонки
        raceCols = ['grid', 'AvgPos', 'AvgPosSeason', 'TotalWins', 'TotalWinsSeason', \
                    'AvgGrid', 'AvgGridSeason', 'TotalPoles', 'TotalPolesSeason']

        # Результат гонки
        raceLabelCol = ['WinnerR']

        # Признаки квалификации
        qualCols = ['AvgGrid', 'AvgGridSeason', 'TotalPoles', 'TotalPolesSeason']

        # Результат квалификации
        qualLabelCol = ['WinnerQ']

        # Категории
        nominalCols = ['circuitId', 'constructorId']

        # Параметры модели гонки
        RaceParams = {
                        'criterion': 'gini', 
                        'max_depth': 10, 
                        'max_features': 'log2', 
                        'min_samples_leaf': 5, 
                        'min_samples_split': 2, 
                        'n_estimators': 50
                    }

        # Параметры модели квалификации
        QualParams = {
                        'criterion': 'gini', 
                        'max_depth': 5, 
                        'max_features': 'auto', 
                        'min_samples_leaf': 5, 
                        'min_samples_split': 2, 
                        'n_estimators': 50
                    }

        db = mysql_conn(f1db.DB_NAME)

        # Получение известных данных
        df = pd.read_sql(SQLTrain, con=db)

        # Разделение данных на гонку и квалификацию
        dfRace = df[commonCols + raceCols + raceLabelCol]
        dfQual = df[commonCols + qualCols + qualLabelCol]

        # Выделение известных результатов
        dfRaceLabels = dfRace.pop(raceLabelCol[0])
        dfQualLabels = dfQual.pop(qualLabelCol[0])

        # Создание категорий
        dfRace = pd.get_dummies(dfRace, columns=nominalCols)
        dfQual = pd.get_dummies(dfQual, columns=nominalCols)

        # Получение данных для прогноза
        df = pd.read_sql(SQLPredict, con=db, index_col='driver_id')

        # Разделение данных на гонку и квалификацию
        dfRacePredict = df[commonCols + raceCols]
        dfQualPredict = df[commonCols + qualCols]

        # Создание категорий
        dfRacePredict = pd.get_dummies(dfRacePredict, columns=nominalCols)
        dfQualPredict = pd.get_dummies(dfQualPredict, columns=nominalCols)

        df = None
        db.close()

        print(datetime.datetime.today(), 'Data loaded')

        # Создание модели для квалификации
        QualModel, QualScore = getModel(dfQual, dfQualLabels, QualParams)
        print('Qual score:', QualScore)

        # Создание модели для гонки
        RaceModel, RaceScore = getModel(dfRace, dfRaceLabels, RaceParams)
        print('Race score:', RaceScore)
        print(datetime.datetime.today(), 'Models ready')

        emptyColRace = [col for col in list(dfRace) if col not in list(dfRacePredict)]
        emptyColQual = [col for col in list(dfQual) if col not in list(dfQualPredict)]

        for col in emptyColQual:
            dfQualPredict[col] = 0

        for col in emptyColRace:
            dfRacePredict[col] = 0

        # Прогноз для квалификации
        QualResult = QualModel.predict_proba(dfQualPredict)

        # Добавление прогноза квалификации к данным для прогноза гонки
        dfRacePredict['gridProb'] = pd.Series([w for l, w in QualResult], index=dfQualPredict.index)
        dfRacePredict['grid'] = dfRacePredict['gridProb'].rank(ascending=False, method='first').astype('uint8')
        dfRacePredict.drop(['gridProb'], inplace=True, axis=1)

        # Прогноз для гонки
        RaceResult = RaceModel.predict_proba(dfRacePredict)

        # Преобразование вероятности в место на финише
        dfRacePredict['winProb'] = pd.Series([w for l, w in RaceResult], index=dfRacePredict.index)
        dfRacePredict['WinnerR'] = dfRacePredict['winProb'].rank(ascending=False, method='first').astype('uint8')
        dfRacePredict.drop(['winProb'], inplace=True, axis=1)

        dfRacePredict['position'] = dfRacePredict['WinnerR']

        print(datetime.datetime.today(), 'Predictions ready')


        # Запись результата в БД
        db = mysql_conn(f1db.DB_NAME)
        cursor = db.cursor()
        cursor.execute('TRUNCATE TABLE ' + FC_TABLE)
        engine = create_engine('mysql+mysqldb://' + f1db.DB_ETL_USER + ':' \
                                + f1db.DB_ETL_USER_PASSWORD + \
                                '@' + f1db.DB_HOST + '/' + f1db.DB_NAME, echo=False)
        dfRacePredict[['position', 'grid']].to_sql(name=FC_TABLE, con=engine, if_exists='append', schema='f1db')

        db.close()

        print(datetime.datetime.today(), 'Done')
