[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version fury.io](https://badge.fury.io/py/qgate-model.svg)](https://pypi.python.org/pypi/qgate-model/)
![coverage](https://github.com/george0st/qgate-model/blob/main/coverage.svg)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/george0st/qgate-model)
![GitHub release](https://img.shields.io/github/v/release/george0st/qgate-model) 

# QGate-Model
The machine learning meta-model with synthetic data (useful for MLOps/feature store), is independent of machine
learning solutions (definition in json, data in csv/parquet).

![Quality-Gate](./docs/assets/icons8-quality-100.png) 

## Usage
The meta-model is suitable for:
 - compare capabilities and functions of machine learning solutions (as part of RFP/X and 
[SWOT analysis](https://en.wikipedia.org/wiki/SWOT_analysis))
 - independent test new versions of machine learning solutions (with aim to keep quality in time)
 - unit, sanity, smoke, system, integration, regression, function, acceptance, 
performance, shadow, ... tests
 - external test coverage (in case, that internal test coverage is not available or weak)
 - etc.

Note: You can see real usage of this meta-model in e.g. project **[qgate-sln-mlrun](https://github.com/george0st/qgate-sln-mlrun)** 
for testing [MLRun](https://www.mlrun.org/)/[Iguazio](https://www.iguazio.com/) solution.

## Structure
The solution contains this simple structure:
 - **00-high-level**
   - The high-level [view](#meta-model) to the meta-model for better understanding
 - **01-model**
   - The definition contains 01-projects, 02-feature sets, 03-feature vectors, 
   04-pipelines, 05-ml models, etc.
 - **02-data**
   - The synthetic data for meta-model in CSV/GZ and parquet formats for party, account,
   transaction, event, communication, etc.
   - You can also generate your own dataset with requested size (see samples `./02-data/03-size-10k.sh`, 
   `./02-data/04-size-50k.sh`, etc. and description `python main.py generate --help`)
 - **03-test**
   - The information for test simplification e.g. feature vector vs on/off-line data, 
   test/data hints, etc.

Addition details, [see structure](./docs/structure.md) and [see rules](./docs/rules.md)

## Expected integrations
The supported sources/targets for realization (✅ done, ✔ in-progress, ❌ planned), see 
the definition `/spec/targets/` in projects (see specification in JSON files):
 - ✅ Redis, ✅ MySQL, ✅ Postgres, ✅ Kafka 
 - ✅ Pandas, ✅ Parquet, ✅ CSV

## Meta-Model

The object relations for key objects in meta-model, plus
splitting these objects in packages (01-model/01-project, 01-model/02-feature-set,
02-data, etc.).

![Object-relations](./00-high-level/object-relations.png)

The basic feature sets and relations between them.

![Basic-model](./00-high-level/basic-feature-sets.png)

The derived feature sets and relations between them.

![Derived-model](./00-high-level/derived-feature-sets.png)
