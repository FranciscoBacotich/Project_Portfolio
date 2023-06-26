---Schema and Database Creation in MYSqL
CREATE DATABASE mydb CHARACTER SET utf8 COLLATE utf8_bin;  
CREATE USER 'FB_UFC_odds' IDENTIFIED BY '12248650@SQLThatSenuaGuy'; 
GRANT ALL PRIVILEGES ON ufc_odds.* TO 'FB_UFC_odds'@'%';

CREATE TABLE ufc_data (
  R_fighter VARCHAR(255),
  B_fighter VARCHAR(255),
  R_odds INT,
  B_odds INT,
  date DATE,
  location VARCHAR(255),
  country VARCHAR(255),
  Winner VARCHAR(255),
  title_bout BOOLEAN,
  weight_class VARCHAR(255),
  gender VARCHAR(255)
);
DESCRIBE ufc_data;

---Import Csv file with the database information.SHOW VARIABLES LIKE "secure_file_priv"; to find the path to the authorize folder.Run in root
LOAD DATA LOCAL INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Data - UFC.csv'
INTO TABLE ufc_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;                                                                                                                                                                                                   
