# Rules for generated data

This is a basic look at several roles (not completed list) applied to generated data. 
You can see full detail in source code, see the folder `generator` in this GIT project.

## Name convention

 - Not to use '-' in feature/entity names (use '_' instead of that)
   - Note: it supports compatibility between Python and SQL
 - Not to use 
## 01. Basic-party

 - **party-establishment**: between generated data minus 15-100 years
 - **party-nchild**: interval 0-4
 - **party-type**: available values 'lead', 'prospect', 'client'
 - **party-peoplehousehold**: respect amnout of childrens

## 02. Basic-partycontact

 - **cardinality**: basic-party vs basic-partycontact (1:N)
 - ...

## 03. Basic-partyrelation
 
 - **cardinality**: basic-party vs basic-partyrelation (M:N)
 - ...

## 04. Basic-account

 - **cardinality**: basic-party vs basic-account (1:N) 
 - **party-type**: only type 'client' has accounts (amount of accounts from 1 to 4)

## 05. Basic-transaction

 - **cardinality**: basic-account vs basic-transaction (1:N) 
 - ...

## 06. Basic-event

 - **cardinality**: basic-party vs basic-event (1:N) 
 - ...

## 07. Basic-communication
 
 - **cardinality**: basic-party vs basic-event (1:N) 
 - ...
