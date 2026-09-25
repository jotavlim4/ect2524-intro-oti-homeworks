def nearst_neighbor(dist_cities, origin=1):
    """
        in: dist_cities é um dicionários cujas chaves tuplas de inteiros que representam as cidades e o valor é a distância entre essas cidades.
        out: menor rota encontrada, o custo e o tempo de execução
    """
    cities = len(list(dist_cities))
    visited = [0] * 
    smallest_dist = (0, 0, 0) # actual_city, dest_city, dist

    for i in range(origin, len(dist_cities) + 1):
        actual_city = origin
        for j in range(2, len())

    