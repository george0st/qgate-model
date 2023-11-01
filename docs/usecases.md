# Use cases for key-value model

The list of expected use cases for key-value model (for MLOps with/without feature store):

 - **UC001: Get list of parties** 
   - with details e.g. income, etc.
 - **UC002: Get list of accounts for relevent party**
   - with details e.g. account type, etc.
 - **UC003: Get list of transactions for relevant account**
   - with detail e.g. transaction amount, date, etc.
 - **UC004: Get list of party contacts for relevant party**
   - with detail e.g. email address, etc.
 - **UC005: Get list of party relation for relevant party**
   - with detail e.g. relation to other party, type of relation, etc.
 - **UC006: Get list of events for relevant party**
   - with detail e.g. event action - login, show contract detail, change contact information, etc.

Note: The feature store concept is based on feature sets (tables with key-value structure)
which can be joined via feature vectors (views).