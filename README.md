# Synthetic-Healthcare-Data---Semantic-View
Data materialization script and semantic view YAML file for the Synthetic Healthcare Data available on the Snowflake Marketplace.

This is for the following data product on the Snowflake Marketplace - https://app.snowflake.com/marketplace/listing/GZSTZL7M0Q6/snowflake-virtual-hands-on-labs-synthetic-healthcare-data-clinical-and-claims

There are three files here:

1. Script to materialize the shared data product into your own account.  I did this just in case the data product changes in the future, I wouldn't want it to unexpectedly break the semantic view being created.
2. YAML file for Semantic View creation.
3. SiS app code for a Cortex Analyst app.  The app is branded for Aetna.  After editing any code to make it work in your Snowflake account, you can cut and paste the whole code into Cursor and leverage Cursor to re-brand it however you want.


