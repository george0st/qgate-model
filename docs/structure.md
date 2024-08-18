# Structure details
 - **00-high-level**
   - [Object-relations](../00-high-level/object-relations.png), [Basic-model](../00-high-level/basic-feature-sets.png), [Derived-model](../00-high-level/derived-feature-sets.png) are described as class model in UML
 - **01-model**
   - The objects such as projects, feature sets, feature vectors, pipelines, ml models, etc.
   are chosen based on best practices (without view to limits some specific 
   ML/MLOps solutions)
 - **02-data**
   - Data sets are in different amount of items based on amount of counterparties 
   (clients, prospects, leads). Default data sets are 100 items and 1K items.    
   - You can also generate your own dataset with requested size see 
   sample './02-data/03-size-10k.sh' or run command line 'python main.py generate --help'
   - The all data is synthetic and generated with the aim of maintaining referential integrity 
   and "closeness" to real dates (this also applies to sensitive data such as PII, SPII, etc. 
   see email, birthday, etc.)
 - **03-test**
   - The information for test simplification e.g.
     - which feature vectors support on/off-line features sets
     - hints for tests (how can you check valid output from feature vectors)
     - etc. 


## Generated data
 - [Basic rules for generated data](./rules.md), cardinality, constrains, etc.
 - Data is in CSV/GZ and parquet formats
   - A few details: 
     - header=True, encoding="utf-8", sep=",", decimal="." 
     - NOTE: setting of 'sep' and 'decimal' see the json file '01-model/model.json'



