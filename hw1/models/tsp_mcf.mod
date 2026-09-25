#parametros comums:
param num_cities;
param dist_cities{
    1..num_cities, 
    1..num_cities
    }; 

#variável de decisão comum:
var travel{
    1..num_cities,
    1..num_cities
    } binary;

#variável de decisão espcífica da implementação MCF:
var commodity_flow{
    i in 1..num_cities, 
    j in 1..num_cities, 
    k in 2..num_cities: i != j 
    } >= 0;

#funcao objetivo comum:
minimize Z: 
sum{    
    i in 1..num_cities, 
    j in 1..num_cities: 
    i != j
    } dist_cities[i, j] * travel[i, j];

#restricoes communs
subject to c_in {j in 1..num_cities}:
    sum{i in 1..num_cities: i != j} travel[i, j] = 1;

subject to c_out {i in 1..num_cities}:
    sum{j in 1.. num_cities: i != j} travel[i, j] = 1;

#restricoes da implementacao MCF:
subject to origin {k in 2..num_cities}:
    sum{j in 1..num_cities: j != 1} commodity_flow[1, j, k] - sum{j in 1..num_cities: j != 1} commodity_flow[j, 1, k] = 1;

subject to destination {k in 2..num_cities}:
    sum{j in 1..num_cities: j != k} commodity_flow[k, j, k] - sum{j in 1..num_cities: j != k} commodity_flow[j, k, k] = -1;

subject to others {i in 2..num_cities, k in 2..num_cities: i != k}:
    sum{j in 1..num_cities: j != i} commodity_flow[i, j, k] - sum{j in 1..num_cities: j != i} commodity_flow[j, i, k] = 0;

subject to flow_coupling{
    i in 1..num_cities, 
    j in 1..num_cities, 
    k in 2..num_cities: i != j
    }: commodity_flow[i, j ,k] <= travel[i, j];