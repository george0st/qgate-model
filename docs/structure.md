# Structure details
 - **00-high-level**
   - [Basic-model](../00-high-level/basic-feature-sets.png), [Derived-model](../00-high-level/derived-feature-sets.png) are described as class model in UML
 - **01-model**
   - Name of objects such as entities, features, feature sets, etc. are chosen based on
   best practices (without view to limits some specific ML/MLOps solutions)
   - A few details: max_name=32 chars, code_page=ASCII
 - **02-data**
   - Data sets are in different amount of items based on amount of counterparties 
   (clients, prospects, leads). Default data sets are 100 items and 1K items.    
   - You can also generate your own dataset with requested size see 
   sample './02-data/03-size-10k.sh' or run command line 'python main.py generate --help'
   - The all data is synthetic and generated with the aim of maintaining referential integrity 
   and "closeness" to real dates (this also applies to sensitive data such as PII, SPII, etc. 
   see email, birthday, etc.)
 - **03-test**
   - The information for test simplification e.g. which feature vectors support on/off-line 
   features sets, set of data hints, hints for tests, etc. 


## Generated data
 - [Basic rules for generated data](./rules.md), cardinality, constrains, etc.
 - Data is in format CSV/GZ format (with expected future parquet support)
   - A few details: header=True, encoding="utf-8", sep=";", decimal=","



