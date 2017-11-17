from django.db import connection


def getTotalWins():
    with connection.cursor() as cursor:
        cursor.execute('SELECT d.driverId, d.forename, d.surname, COUNT(r.resultId) AS Wins \
                        FROM f1db.results r \
                        INNER JOIN f1db.drivers d ON d.driverId = r.driverId \
                        WHERE r.position = 1 \
                        GROUP BY d.driverId, d.forename, d.surname \
                        ORDER BY 4 DESC \
                        LIMIT 20')
        report = cursor.fetchall()
    return report


def getTotalPoints():
    with connection.cursor() as cursor:
        cursor.execute('SELECT d.driverId, d.forename, d.surname, SUM(r.points) AS Points \
                        FROM f1db.results r \
                        INNER JOIN f1db.drivers d ON d.driverId = r.driverId \
                        GROUP BY d.driverId, d.forename, d.surname \
                        ORDER BY 4 DESC \
                        LIMIT 20')
        report = cursor.fetchall()
    return report


def getTotalParticipants():
    with connection.cursor() as cursor:
        cursor.execute('SELECT rs.year, COUNT(DISTINCT r.constructorId) AS Teams, COUNT(DISTINCT r.driverId) AS Drivers \
                        FROM f1db.results r \
                        INNER JOIN f1db.races rs ON rs.raceId = r.raceId \
                        GROUP BY rs.year \
                        ORDER BY rs.year')
        report = cursor.fetchall()
    return report


def getMonacoLapTime2():
    with connection.cursor() as cursor:
        cursor.execute("SELECT r.year, \
                            CAST(CAST(TIME_FORMAT(CONCAT('0:', res.fastestLapTime), '%i') AS UNSIGNED) * 60000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', res.fastestLapTime), '%s') AS UNSIGNED) * 1000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', res.fastestLapTime), '%f') AS UNSIGNED) / 1000 \
                                AS UNSIGNED) AS RaceTime, \
                            CAST(CAST(TIME_FORMAT(CONCAT('0:', COALESCE(q.q3, q.q2, q.q1)), '%i') AS UNSIGNED) * 60000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', COALESCE(q.q3, q.q2, q.q1)), '%s') AS UNSIGNED) * 1000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', COALESCE(q.q3, q.q2, q.q1)), '%f') AS UNSIGNED) / 1000 \
                                AS UNSIGNED) AS QualTime \
                        FROM f1db.races r \
                        INNER JOIN f1db.results res ON res.raceId = r.raceId AND res.rank = 1 \
                        INNER JOIN f1db.qualifying q ON q.raceId = r.raceId AND q.position = 1 \
                        WHERE r.circuitId = 6 \
                        ORDER BY r.year")
        report = cursor.fetchall()
    return report


def getMonacoLapTime():
    with connection.cursor() as cursor:
        cursor.execute("SELECT r.year, \
                            CAST(CAST(TIME_FORMAT(CONCAT('0:', res.fastestLapTime), '%i') AS UNSIGNED) * 60000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', res.fastestLapTime), '%s') AS UNSIGNED) * 1000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', res.fastestLapTime), '%f') AS UNSIGNED) / 1000 \
                                AS UNSIGNED) AS RaceTime, \
                            CAST(CAST(TIME_FORMAT(CONCAT('0:', IFNULL(q.q3, '59')), '%i') AS UNSIGNED) * 60000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', IFNULL(q.q3, '59')), '%s') AS UNSIGNED) * 1000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', IFNULL(q.q3, '59')), '%f') AS UNSIGNED) / 1000 \
                                AS UNSIGNED) AS QualTime3, \
                            CAST(CAST(TIME_FORMAT(CONCAT('0:', IFNULL(q.q2, '59')), '%i') AS UNSIGNED) * 60000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', IFNULL(q.q2, '59')), '%s') AS UNSIGNED) * 1000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', IFNULL(q.q2, '59')), '%f') AS UNSIGNED) / 1000 \
                                AS UNSIGNED) AS QualTime2, \
                            CAST(CAST(TIME_FORMAT(CONCAT('0:', IFNULL(q.q1, '59')), '%i') AS UNSIGNED) * 60000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', IFNULL(q.q1, '59')), '%s') AS UNSIGNED) * 1000 + \
                                 CAST(TIME_FORMAT(CONCAT('0:', IFNULL(q.q1, '59')), '%f') AS UNSIGNED) / 1000 \
                                AS UNSIGNED) AS QualTime1 \
                        FROM f1db.races r \
                        INNER JOIN f1db.results res ON res.raceId = r.raceId AND res.rank = 1 \
                        INNER JOIN f1db.qualifying q ON q.raceId = r.raceId AND q.position = 1 \
                        WHERE r.circuitId = 6 \
                        ORDER BY r.year")
        report = cursor.fetchall()
    return report


def getTotalCareer():
    with connection.cursor() as cursor:
        cursor.execute('SELECT res.driverId, d.forename, d.surname, \
                            FLOOR(DATEDIFF(MAX(r.date), MIN(r.date))/365) AS Years, COUNT(res.raceId) AS Races \
                        FROM f1db.results res \
                        INNER JOIN f1db.races r ON r.raceId = res.raceId \
                        INNER JOIN f1db.drivers d ON d.driverId = res.driverId \
                        group by res.driverId, d.forename, d.surname \
                        ORDER BY 4 DESC \
                        LIMIT 20')
        report = cursor.fetchall()
    return report


def getPitstopTime(circuitid):
    with connection.cursor() as cursor:
        cursor.execute('SELECT r.year, MIN(p.milliseconds) AS MinTime, FLOOR(AVG(p.milliseconds)) AS AvgTime \
                        FROM f1db.pitStops p \
                        INNER JOIN f1db.races r ON r.raceId = p.raceId \
                        INNER JOIN f1db.circuits c ON c.circuitId = r.circuitId AND c.circuitId = %s \
                        GROUP BY r.year, c.circuitId, c.name \
                        ORDER BY r.year, c.circuitId, c.name', [str(int(circuitid))])
        report = cursor.fetchall()
    return report
