use role ACCOUNTADMIN;
--CREATE WAREHOUSE
CREATE OR REPLACE WAREHOUSE DATAENGINE WAREHOUSE_SIZE = XSMALL, AUTO_SUSPEND = 300, AUTO_RESUME= TRUE;

--USE WAREHOUSE
USE WAREHOUSE DATAENGINE;

 -- CREATE DATABASE
CREATE OR REPLACE DATABASE CUSTOMER_DATABASE;

--DROP PUBLIC SCHEMA
DROP SCHEMA CUSTOMER_DATABASE.PUBLIC;
-- CREATE RAW_NEWSARTICLES
CREATE OR REPLACE SCHEMA  CUSTOMER_DATABASE.RAW_CUSTOMER;



--- create storage intergration

CREATE or replace STORAGE INTEGRATION customer_data_int
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::076482969119:role/snowflake_ecommarce_role'
  STORAGE_ALLOWED_LOCATIONS = ('s3://landing-zone-customers-bucket/');
 
 --- Retrieve the AWS IAM User for your Snowflake Account

 DESC INTEGRATION customer_data_int;

--- just granting privilege for the schema to my self noting special
GRANT CREATE STAGE ON SCHEMA CUSTOMER_DATABASE.RAW_CUSTOMER TO ROLE ACCOUNTADMIN;

GRANT USAGE ON INTEGRATION customer_data_int TO ROLE ACCOUNTADMIN;

--- Create an External Stage 


CREATE or replace STAGE raw_customer_stage
  STORAGE_INTEGRATION = ecommarce_data_int
  URL = 's3://landing-zone-customers-bucket/';
 

-- testing stage to retrive data
list @raw_customer_stage;




---- create product details
CREATE OR REPLACE TABLE CUSTOMER.RAW_CUSTOMER.CUSTOMER_TABLE (
    product VARCHAR,
    customer_name VARCHAR,
    customer_email VARCHAR,
    phone_number INT,
    address VARCHAR,
    city VARCHAR,
    shipping_address VARCHAR,
    order_date DATE,
    quantity INT,
    price FLOAT,
    country VARCHAR,
    payment_method VARCHAR,
    status VARCHAR   
);



