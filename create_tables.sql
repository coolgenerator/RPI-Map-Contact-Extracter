CREATE DATABASE IF NOT EXISTS MapContactExtracter;

CREATE TABLE IF NOT EXISTS COMPANY (
    CompanyID int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    CompanyName varchar(255) NOT NULL,
    Address varchar(255),
    State varchar(50),
    ZipCode varchar(10),
    Category varchar(50),
    Description varchar(255),
    DirectLink varchar(255),
    Status tinyint(1),
    Keyword varchar(50),
    Rating varchar(5),
    RateNum varchar(10)
    );
    
CREATE TABLE IF NOT EXISTS WEBSITE (
    WebsiteID int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    CompanyID int NOT NULL REFERENCES COMPANY(CompanyID),
    Website varchar(255) NOT NULL,
    Status tinyint(1),
    Category varchar(30)
    );
    
CREATE TABLE IF NOT EXISTS EMAIL (
    EmailID int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    CompanyID int NOT NULL REFERENCES COMPANY(CompanyID),
    WebsiteID int,
    Email varchar(255) NOT NULL,
    Contactor varchar(30),
    Status tinyint(1)
    );
    
CREATE TABLE IF NOT EXISTS PHONE (
    PhoneID int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    CompanyID int NOT NULL REFERENCES COMPANY(CompanyID),
    Phone varchar(255) NOT NULL,
    Contactor varchar(30),
    Status tinyint(1)
    );
    
CREATE TABLE IF NOT EXISTS CONTACTHISTORY (
    EmailID int NOT NULL REFERENCES EMAIL(EmailID),
    CompanyID int NOT NULL REFERENCES COMPANY(CompanyID),
    Times int NOT NULL,
    FromEmail int,
    Date DATE,
    Comment varchar(255),
    Status tinyint(1),
    CONSTRAINT PK_EMAIL PRIMARY KEY (EmailID, Times)
    );
    
CREATE TABLE IF NOT EXISTS FROMEMAIL (
    FromEmailID int NOT NULL PRIMARY KEY PRIMARY KEY AUTO_INCREMENT,
    Email varchar(255) NOT NULL
    );
    
CREATE TABLE IF NOT EXISTS LOGGER (
    TimesID int NOT NULL,
    Keyword varchar(255) NOT NULL,
    County varchar(50) NOT NULL,
    Time Datetime
    );