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
    AND cc.candyconsumption_date_ik BETWEEN STR_TO_DATE('20180501','%Y%m%d') AND STR_TO_DATE('20180531','%Y%m%d')
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


