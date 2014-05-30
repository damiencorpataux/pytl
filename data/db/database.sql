-- SET GLOBAL sql_mode = "TRADITIONAL";
SET SESSION sql_mode = "TRADITIONAL";

DROP DATABASE IF EXISTS tl;
CREATE DATABASE tl DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE tl;

DROP TABLE IF EXISTS line;
CREATE TABLE  line (
    id INT NOT NULL AUTO_INCREMENT
    COMMENT "Line identifier (the tl numeric id from http://www.t-l.ch/horaires-par-arrets.html)",
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    COMMENT "Row creation timestamp",
    name VARCHAR(255) UNIQUE NOT NULL
    COMMENT "Human name of the line",
    PRIMARY KEY (id)
) ENGINE=InnoDB
COMMENT "Lines catalog";

DROP TABLE IF EXISTS station;
CREATE TABLE station (
    name VARCHAR(255) NOT NULL
    COMMENT "Human name of the station",
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    COMMENT "Row creation timestamp",
    root VARCHAR(255) NOT NULL
    COMMENT "Station text identifier",
    PRIMARY KEY (name)
) ENGINE=InnoDB
COMMENT "Stations catalog";

DROP TABLE IF EXISTS stop;
CREATE TABLE stop (
    id INT NOT NULL AUTO_INCREMENT
    COMMENT "Internal stop identifier",
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    COMMENT "Row creation timestamp",
    orientation CHAR(1) NOT NULL
    COMMENT "Station are split into stops (typically one stop per direction)",
    direction CHAR(1) NOT NULL
    COMMENT "Direction of the line (can be 'a' or 'r')",
    line_id INT NOT NULL
    COMMENT "Line identifier",
    station_name VARCHAR(255) NOT NULL
    COMMENT "Station identifier",
    PRIMARY KEY (id),
    FOREIGN KEY (line_id) REFERENCES line(id),
    FOREIGN KEY (station_name) REFERENCES station(name)
) ENGINE=InnoDB
COMMENT "A stop lays where a line crosses a station";
