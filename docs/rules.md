# Rules for generated data

This is a basic look at several roles (not completed list) applied to generated data. 
You can see full detail in source code see the folder [generator](./generator/)

## 1. Basic-party

 - **party-establishment**: between generated data minus 15-100 years
 - **party-nchild**: interval 0-4
 - **party-type**: available values 'lead', 'prospect', 'client'
 - **party-peoplehousehold**: respect amnout of childrens

## 2. Basic-account

 - **cardinality**: basic-party vs basic-account (1:N) 
 - **party-type**: only type 'client' has accounts (amount of accounts from 1 to 4)

## 3. Basic-transaction

 - **cardinality**: basic-account vs basic-transaction (1:N) 
 - ...

