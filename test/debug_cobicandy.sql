SELECT 
        SUM(cc.candycount_nb) AS CANDY_COUNT
        , DATE(cc.logged_date) AS reporting_date
        , DATE_FORMAT(cc.logged_date,'%a %b %d') AS day_of_week
        , dd.weekend
        , HOUR(cc.logged_date) AS logged_hour
FROM candydb.candycounts cc
        INNER JOIN candydb.date_dimension dd
                ON cc.candyconsumption_date_ik = dd.date_id
WHERE 1=1
    AND cc.candyconsumption_date_ik BETWEEN STR_TO_DATE('20180622','%Y%m%d') AND STR_TO_DATE('20180622','%Y%m%d')
    AND HOUR(cc.logged_date) BETWEEN 6 AND 18
GROUP BY dd.day_of_week
        , dd.weekend
        , DATE(cc.logged_date)
        , HOUR(cc.logged_date)
ORDER BY HOUR(cc.logged_date), cc.logged_date ASC
;

CREATE TABLE derp AS (
SELECT 
	*
FROM candydb.candycounts cc
WHERE 1=1
    AND cc.candyconsumption_date_ik BETWEEN STR_TO_DATE('20180501','%Y%m%d') AND STR_TO_DATE('20180531','%Y%m%d')
ORDER BY cc.logged_date ASC
)
;

SELECT *
FROM candydb.candycounts cc
WHERE DATE_FORMAT(cc.logged_date,'%a %b %d') = 'Wed May 09'
;



SELECT COUNT(0)
FROM time_dimension
;

SELECT DISTINCT *
FROM derp d
	INNER JOIN (
		SELECT DISTINCT HOUR FROM time_dimension td
        ) td
		 ON HOUR(d.logged_date) = td.HOUR
        
;


SELECT 
	SUM(cc.candycount_nb) AS candyconsumed_nb
    ,CONCAT(dd.year, ' - Wk ', dd.week_starting_monday) AS week
FROM candydb.candycounts cc
	INNER JOIN candydb.date_dimension dd
		ON cc.candyconsumption_date_ik = dd.date_id
WHERE 1=1
	AND cc.logged_date BETWEEN DATE_ADD(CURRENT_DATE, INTERVAL -4 WEEK) AND CURRENT_DATE
GROUP BY CONCAT(dd.year, ' ', dd.week_starting_monday)
ORDER BY cc.logged_date ASC
;


SELECT 
    SUM(candycount_nb) AS currentDayCandyCount
    ,CURRENT_DATE AS startOfCurrentDay
    ,CURRENT_TIMESTAMP AS queryCurrentTime
FROM candydb.candycounts cc
WHERE 1=1
	AND cc.logged_date BETWEEN CURRENT_DATE AND CURRENT_TIMESTAMP
ORDER BY logged_date DESC
;

SELECT 
    SUM(candycount_nb) AS previousDayCandyCount
    ,ADDDATE(CURRENT_DATE, INTERVAL -1 DAY) AS startOfPreviousDay
    ,CURRENT_DATE AS endOfPreviousDay
FROM candydb.candycounts cc
WHERE 1=1
	AND cc.logged_date BETWEEN ADDDATE(CURRENT_DATE, INTERVAL -1 DAY) AND CURRENT_DATE
ORDER BY logged_date DESC
;

SELECT 
	STR_TO_DATE(CONCAT(CAST(CURRENT_DATE AS CHAR(12)),' ',CAST(HOUR(CURRENT_TIME) AS CHAR),':00:00'),'%Y-%m-%d %T') AS CURRENT_HOUR
	,CURRENT_TIME
	,TIME_FORMAT(CURRENT_TIME, '%H')
    ,ADDTIME(STR_TO_DATE(CONCAT(CAST(CURRENT_DATE AS CHAR(12)),' ',CAST(HOUR(CURRENT_TIME) AS CHAR),':00:00'),'%Y-%m-%d %T'),'-01:00:00') AS TIME_ADD
    ,STR_TO_DATE(CONCAT(CAST(CURRENT_DATE AS CHAR(12)),' ',CAST(HOUR(CURRENT_TIME) AS CHAR),':00:00'),'%Y-%m-%d %T') AS LAG_TIME_END
,CURRENT_TIMESTAMP
;

SELECT CURRENT_DATE;
-- || CAST(HOUR(CURRENT_TIME) AS VARCHAR(2));

SELECT *
FROM mysql.time_zone_name
;


SELECT 
	STR_TO_DATE(CONCAT(CAST(CURRENT_DATE AS CHAR(12)),' ',CAST(HOUR(CURRENT_TIME) AS CHAR),':00:00'),'%Y-%m-%d %T') AS CURRENT_DATE_HOUR
	,CONCAT(CAST(CURRENT_DATE AS CHAR(12)),' ',CAST(HOUR(CURRENT_TIME) AS CHAR),':00:00') AS CURRENT_DATE_HOUR_TX
;

SELECT *
FROM candycounts
;


INSERT INTO `candydb`.`candycounts`
(
`candyconsumption_date_ik`,
`candylog_type_ik`,
`candycount_nb`,
`logged_date`)
VALUES
(
20180428,
1,
3,
CURRENT_TIMESTAMP);

COMMIT;
