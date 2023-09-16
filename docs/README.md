# Addition details

## Structure details
 - **00-high-level**
   - [Basic-model](../00-high-level/basic-feature-sets.png), [Derived-model](../00-high-level/derived-feature-sets.png) are described as class model in UML
 - **01-model**
   - Name of objects such as entities, features, feature sets, etc. are chosen based on
   best practices (without view to limits some specific ML/MLOps solutions)
   - A few details: max_name=32 chars, code_page=ASCII
 - **02-data**
   - Data sets are in different sizes based on amount of counterparties (clients, prospects, leads), ~100 items, ~1K items, ~10K items
   - The data is synthetic and generated with the aim of maintaining referential integrity 
   and closeness to real dates (this also applies to sensitive data such as PII, SPII, etc. 
   see email, birthday, etc.)

## Generated data
 - [Basic rules for generated data](./rules.md), cardinality, constrains, etc.
 - Data is in format CSV (or compressed CSV)
   - A few details: header=True, encoding="utf-8", sep=";", decimal=","



