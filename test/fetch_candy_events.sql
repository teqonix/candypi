SELECT 
        SUM(cc.candycount_nb) AS CANDY_COUNT
        , DATE(cc.logged_date) AS reporting_date
        , DATE_FORMAT(cc.logged_date,'%a %b %d') AS day_of_week
        , dd.weekend
        , COALESCE(HOUR(cc.logged_date),h.HOUR) AS logged_hour
FROM candydb.candycounts cc
        INNER JOIN candydb.date_dimension dd
                ON cc.candyconsumption_date_ik = dd.date_id
	RIGHT OUTER JOIN (
			SELECT DISTINCT HOUR FROM candydb.timedim
			) h
		ON HOUR(cc.logged_date) = h.HOUR
WHERE
    ( cc.candyconsumption_date_ik BETWEEN STR_TO_DATE('20180501','%Y%m%d') AND STR_TO_DATE('20180601','%Y%m%d')
      AND HOUR(cc.logged_date) BETWEEN 6 AND 18
    )
OR 
    ( 
	cc.candyconsumption_date_ik IS NULL
    )
GROUP BY dd.day_of_week
        , dd.weekend
        , DATE(cc.logged_date)
        , HOUR(cc.logged_date)
ORDER BY cc.logged_date ASC, logged_hour ASC
