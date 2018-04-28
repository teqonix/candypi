CREATE DATABASE candydb;
CREATE USER 'cobicandy'@'localhost' identified by 'cobi';
grant all on candydb.* to 'cobicandy' identified by 'cobi';

USE candydb;

CREATE TABLE candydb.candycounts(
candycount_ik INT NOT NULL AUTO_INCREMENT PRIMARY KEY
,candyconsumption_date_ik BIGINT NOT NULL
,candylog_type_ik INT DEFAULT 1
,candycount_nb INT DEFAULT 1
,logged_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE candydb.candytype(
candylog_type_ik INT NOT NULL AUTO_INCREMENT PRIMARY KEY
,candytype_name VARCHAR(128) NOT NULL
,added_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO candydb.candytype(candytype_name) VALUES ('Single Piece of Candy'); 

ALTER TABLE candydb.candycounts ADD CONSTRAINT FOREIGN KEY (candylog_type_ik) REFERENCES candydb.candytype (candylog_type_ik);

COMMIT;

###### small-numbers table
DROP TABLE IF EXISTS numbers_small;
CREATE TABLE numbers_small (number INT);
INSERT INTO numbers_small VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8),(9);

###### main numbers table
DROP TABLE IF EXISTS numbers;
CREATE TABLE numbers (number BIGINT);
INSERT INTO numbers
SELECT thousands.number * 1000 + hundreds.number * 100 + tens.number * 10 + ones.number
  FROM numbers_small thousands, numbers_small hundreds, numbers_small tens, numbers_small ones
LIMIT 1000000;

###### date table
DROP TABLE IF EXISTS dates;
CREATE TABLE date_dimension (
  date_id          BIGINT PRIMARY KEY, 
  date             DATE NOT NULL,
  timestamp        BIGINT NOT NULL, 
  weekend          CHAR(10) NOT NULL DEFAULT "Weekday",
  day_of_week      CHAR(10) NOT NULL,
  month            CHAR(10) NOT NULL,
  month_day        INT NOT NULL, 
  year             INT NOT NULL,
  week_starting_monday CHAR(2) NOT NULL,
  UNIQUE KEY `date` (`date`),
  KEY `year_week` (`year`,`week_starting_monday`)
);

###### populate it with days
INSERT INTO date_dimension (date_id, date)
SELECT date_format(DATE_ADD( '2018-01-01', INTERVAL number DAY ), "%Y%m%d"), DATE_ADD( '2018-01-01', INTERVAL number DAY )
  FROM numbers
  WHERE DATE_ADD( '2018-01-01', INTERVAL number DAY ) BETWEEN '2018-01-01' AND '2035-01-01'
  ORDER BY number;

###### fill in other rows
UPDATE date_dimension SET
  timestamp =   UNIX_TIMESTAMP(date),
  day_of_week = DATE_FORMAT( date, "%W" ),
  weekend =     IF( DATE_FORMAT( date, "%W" ) IN ('Saturday','Sunday'), 'Weekend', 'Weekday'),
  month =       DATE_FORMAT( date, "%M"),
  year =        DATE_FORMAT( date, "%Y" ),
  month_day =   DATE_FORMAT( date, "%d" );

UPDATE date_dimension SET week_starting_monday = DATE_FORMAT(date,'%v');

COMMIT;

ALTER TABLE candydb.candycounts ADD CONSTRAINT FOREIGN KEY (candyconsumption_date_ik) REFERENCES candydb.date_dimension (date_id);

CREATE VIEW candydb.candyconsumptiondate AS (
SELECT 
	date_id AS candyconsumption_date_ik
	,date AS candyconsumption_date_dt
	,year AS candyconsumption_year_nb
	,month AS candyconsumption_month_nm
	,month_day AS candyconsumption_day_nb
	,week_starting_monday AS candyconsumption_ISO_week_nb
	,weekend AS candyconsumption_weekend_nm
	,day_of_week AS candyconsumption_week_day_nm
from candydb.date_dimension
);

/*
+----------+------------+------------+---------+-------------+---------+-----------+------+----------------------+
| date_id  | date       | timestamp  | weekend | day_of_week | month   | month_day | year | week_starting_monday |
+----------+------------+------------+---------+-------------+---------+-----------+------+----------------------+
| 20180101 | 2018-01-01 | 1514764800 | Weekday | Monday      | January |         1 | 2018 | 01                   |

*/ 
