# QGate-FS-Model
The sample of feature store model for machine learning, part of quality gate concept. 
This model is independent (definition in json, data in csv) of machine learning solutions.

It can be used with various of ML/MLOps solutions with or without FeatureStore concept.

## Usage
The model is suitable for:
 - compare capabilities and functions of machine learning solutions (as part of RFP/X and SWOT analysis)
 - independent test new versions of machine learning solutions (with aim to keep quality in time)
 - unit, sanity, smoke, system, reqression, function, acceptance, performance, shadow, ... tests
 - external test coverage (in case, that internal test coverage is not available or weak)
 - etc.

## Structure
The solution contains this simple structure:
 - **00-high-level**
   - The high-level view to the current model for better understanding of logical relations
   - see [schema](./00-high-level/qgate-fs-model.png)
 - **01-model**
   - The definition of 01-projects, 02-feature sets, 03-feature vectors, etc. in JSON format
 - **02-data**
   - The data for model in CSV format (data sets are in a few sizes)


## Structure details
 - **01-model**
   - Name of objects such as entities, features, feature sets, etc. are chosen based on
   best practices (without view to limits some specific ML/MLOps solutions)
 - **02-data**
   - Data sets are in different sizes ~100 items, ~1K items, ~10K items
   - The data is synthetic and generated with the aim of maintaining referential integrity 
   and closeness to real dates (this also applies to sensitive data such as PII, SPII, etc. 
   see email, birthday, etc.)
