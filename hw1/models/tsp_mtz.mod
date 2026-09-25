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

#variável de decisão espcífica da implementação MTZ:
var visit_order{2..num_cities} integer >= 1 <= num_cities - 1;

#função objeto comum:
minimize Z: 
sum{
    i in 1..num_cities,
    j in 1..num_cities: i != j
    } dist_cities[i, j] * travel[i, j];

subject to c_in {j in 1..num_cities}:
    sum{i in 1..num_cities: i != j} travel[i,j] = 1;

subject to c_out {i in 1..num_cities}:
    sum{j in 1.. num_cities: i != j} travel[i,j] = 1;

#restrição da implementação MTZ:
subject to subtour_elimination {
    i in 2..num_cities, 
    j in 2..num_cities: i != j
    }: visit_order[i] - visit_order[j] + (num_cities - 1) * travel[i,j] <= num_cities - 2;