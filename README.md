# QGate-FS-Model
The sample of feature store model for machine learning, part of quality gate concept. 
This model is independent (definition in json, data in csv/xlsx) on machine learning solution.

It can be used for different ML/MLOps solutions such as Iguazio/MLRun/MLRun-CE,
Tecton/FEAST, Hopsworks, Comet, Rasgo, Kaskada, Molecula, H2O, Databricks, 
Dataiku, Abacus, Sagemaker, Vertex, Zipline, Featureform, Featurebase, 
Continual, Metarank, Feathr, Michelangelo, Bigabid, Fblearner, Overton,
Doordash, etc.

## Usage
The model is suitable for:
 - independent testing new versions of machine learning solutions (with aim to keep quality in time)
 - compare capabilities of machine learning solutions (as part of RFI, RFP, RFX and SWOT analysis)
 - unit, function, acceptance, performance, shadow, ... tests
 - etc.

## Structure
The solution contains this simple structure:
 - **00-high-level**
   - The high-level view to the current model for better understanding
 - **01-model**
   - The definition of projects, feature sets, feature vectors, etc. in JSON format
 - **02-data**
   - The data for model in CSV and XML formats
