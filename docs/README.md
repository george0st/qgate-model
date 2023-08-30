# Addition details

## Structure details
 - **01-model**
   - Name of objects such as entities, features, feature sets, etc. are chosen based on
   best practices (without view to limits some specific ML/MLOps solutions)
   - A few conventions 
     - max name: 32 chars
     - code page: ASCII
 - **02-data**
   - Data sets are in different sizes based on amount of counterparties (clients, ...), ~100 items, ~1K items, ~10K items
   - The data is synthetic and generated with the aim of maintaining referential integrity 
   and closeness to real dates (this also applies to sensitive data such as PII, SPII, etc. 
   see email, birthday, etc.)

## Generated data
 - [Basic rules for generated data](./rules.md), cardinality, constrains, etc.
 - etc.

## Model
 - [Class model](../00-high-level/qgate-fs-model.png), graphical visualization




