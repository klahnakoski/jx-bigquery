# Typed json in BigQuery 

This document explains the quirks you will encounter in the data loaded by the `jx-bigquery` library.


## Problem

BigQuery table names have a limited character set so they can be put in URLs


## Solution: Escape with underscore (`_`)

`jx-bigquery` encodes all names so they conform to the limited character set. All non-conforming characters are encoded as the unicode hex value, surrounded by underscore (`_`).  For example

| character        | encoded    |
|------------------|------------|
| CR (`\n`)        |  `_a_`     |
| dash (`-`)       |  `_2d_`    |
| underscore (`_`) |  `__`      |
| happy (`😀`)     |  `_1f600_` |

Notice the underscore (`_`) is an exception; it is encoded as double-underscore (`__`).


## Problem 

BigQuery is strictly typed: Numbers, strings and objects can not share a column. 


## Solution: Typed encoding

All column names are given a suffix with the type information. This ensures one property name, with differnt datatypes in different documents, can all be stored in one table.
 

| name | type        | typed name | example json      | typed json           |
|------|-------------|------------|-------------------|----------------------|
| `a`  | `Boolean`   | `a._b_`    | `{"a": true}`     | `{"a": {"_b_": true}}` |
| `a`  | `integer`   | `a._i_`    | `{"a": 1}`        | `{"a": {"_i_": 1}}`    |
| `a`  | `number`    | `a._n_`    | `{"a": 1.0}`      | `{"a": {"_n_": 1.0}}`  |
| `a`  | `timestamp` | `a._t_`    | `{"a": 0}`        | `{"a": {"_t_": 0}}`    |
| `a`  | `string`    | `a._s_`    | `{"a": "1"}`      | `{"a": {"_s_": "1"}}`  |
| `a`  | `object`    | `a._e_`    | `{"a": {}}`       | `{"a": {"_e_": 1}}`    |
| `a`  | `array`     | `a._a_`    | `{"a": [1]}`      | `{"a": {"_a_": [{"_n_": 1}]}}` |

This format allows `jx-bigquery` to

* automatically expand the schema as the source data changes
* insert from multiple machines without need for coordination of schema
* ensure all primitive values are in own column so less data is scanned at query time 
* get around indexing limits found in other document stores
* defer business schema concerns to query time   

This format complicates the json, which can be mitigated with a view to provide better names. Views are also used to show only the latest record for an evolving entity and used to provide flatter perspectives on deeply nested json documents. 

## Problem 

You should only add data to BigQuery: Deleting/changing data is inefficient and does not save space.

## Solution: Keep everything

BigQuery efficiently removes data by dropping partitions, unfortunately a table is a single partition by default.  `jx-bigquery` allows you to specify a column (a timestamp) to use for partitioning; allowing old partitions to be dropped.  Furthermore, `jx-bigquery` lets you specify a cluster column (an id column to index/sort by) to use in all partitions; which that allows multiple records with the same id to be "close together". At a high level, you retain multiple snapshots of the same "entity" over time. To get the latest records, use the following subquery:

```sql
SELECT * EXCEPT (_rank) 
FROM (
  SELECT 
    *, 
    row_number() over (partition by my__id order by my__timestamp desc) as _rank 
  FROM  
    my__dataset.my__table
  ) a 
WHERE _rank=1    
```

