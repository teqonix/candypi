USE candydb;

CREATE TABLE IF NOT EXISTS timedim  (
    time_id INT NOT NULL auto_increment,
    fulltime time,
    hour int,
    minute int,
    second int,
    ampm varchar(2),
    PRIMARY KEY(time_id)
) ENGINE=InnoDB AUTO_INCREMENT=1000;


delimiter //

DROP PROCEDURE IF EXISTS timedimbuild;
CREATE PROCEDURE timedimbuild ()
BEGIN
    DECLARE v_full_date DATETIME;

    DELETE FROM timedim;

    SET v_full_date = '2009-03-01 00:00:00';
    WHILE v_full_date < '2009-03-02 00:00:00' DO

        INSERT INTO timedim (
            fulltime ,
            hour ,
            minute ,
            second ,
            ampm
        ) VALUES (
            TIME(v_full_date),
            DATE(v_full_date,%H),
            DATE(v_full_date,%i),
            SECOND(v_full_date),
            DATE_FORMAT(v_full_date,'%p')
        );

        SET v_full_date = DATE_ADD(v_full_date, INTERVAL 1 SECOND);
    END WHILE;
END;

//
delimiter ;

call timedimbuild();

// delimiter;

CREATE TABLE candydb.time_dimension AS ( SELECT DISTINCT CAST(CONCAT(hour,minute) AS INT) AS time_ik, hour, minute, ampm FROM timedim);
