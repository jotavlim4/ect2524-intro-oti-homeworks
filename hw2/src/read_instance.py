import math

def read_instance(tsp_file):
    """
        input: tsp_file, um arquivo .tsp que contém a dimensao e as coordenadas das 
        cidades visitadas.

        output: retorna o inteiro num_cities que indica o número de cidades (n), e um
        dicionário dist_cities que contem a distnacia da cidade i para j.
    """
    num_cities = None
    coordinates = dict()
    reading_coordinates = False

    with open(tsp_file) as file:
        for line in file:
            line = line.strip()

            if line.startswith("DIMENSION"):
                num_cities = int(line.split(":")[1].strip())

            elif line == "NODE_COORD_SECTION":
                reading_coordinates = True

            elif line == "EOF":
                break

            elif reading_coordinates:
                city, x, y = line.split()
                coordinates[int(city)] = (float(x), float(y))


    dist_cities = dict()

    for i in range(1, num_cities + 1):
        xi, yi = coordinates[i]
        
        for j in range(1, num_cities + 1):
            xj, yj = coordinates[j]
            distance = math.hypot(xi - xj, yi - yj)
            dist_cities[i, j] = int(distance + 0.5)

    return num_cities, dist_cities

            


