neo4j-import comes with the neo4j community version, instal the tar ball, you'll get it. 
```
/Users/kailiu/Downloads/neo4j-community-3.0.6/bin
```

Import CSV files to neo4j 
```
$ ./bin/neo4j-import --into /Users/kailiu/Documents/Neo4j/databases/graph.db 
--nodes /Users/kailiu/startup/springforward/graph/datafetch/data/investor.csv 
--nodes /Users/kailiu/startup/springforward/graph/datafetch/data/stock.csv 
--relationships /Users/kailiu/startup/springforward/graph/datafetch/data/activity.csv 
```
