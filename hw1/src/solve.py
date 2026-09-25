from pathlib import Path
from amplpy import AMPL
from read_instance import read_instance
import time
import math

base = Path(__file__).resolve().parent.parent

SOLVER = "highs"
INSTANCES = ["berlin52.tsp", "ch150.tsp", "kroA100.tsp", "kroA200.tsp"]
MODELS = ["tsp_mtz.mod"] # tirei o outro modelo para poder executar as demais instânicas

#secolher uma única instância
print("choice a instância:")

for number, name in enumerate(INSTANCES, start=1):
    print(f"{number} - {name}")

while True:
    choice = input("Digite um número de 1 a 4: ").strip()

    if choice in ["1", "2", "3", "4"]:
        instance = INSTANCES[int(choice) - 1]
        break

    print("Opção inválida. Tente novamente.")

#aplicar a instancia escolhida aos dois modelos
for model in MODELS:
    print("\n--------------------")
    print("Modelo:", model)
    print("Instância:", instance)

    ampl = None
    start = time.perf_counter()

    try:
        path_instances = base / "data" / instance
        num_cities, dist_cities = read_instance(path_instances)

        ampl = AMPL()
        path_models = base / "models" / model
        ampl.read(str(path_models))

        ampl.param["num_cities"] = num_cities
        ampl.param["dist_cities"] = dist_cities

        ampl.option["solver"] = SOLVER
        ampl.option[f"{SOLVER}_options"] = (
            "threads=1 timelim=1800 "
            "bestbound=1 return_mipgap=3"
        )

        ampl.eval("""
            suffix bestbound OUT;
            suffix relmipgap OUT;
        """)

        ampl.solve()
        status = ampl.get_value("solve_result")

        print("Solver:", SOLVER)
        print("Status:", status)
        print("Mensagem:", ampl.get_value("solve_message"))

        if status in ["solved", "limit"]:
            lb = ampl.get_value("Z.bestbound")
            gap = ampl.get_value("Z.relmipgap")

            print("LB:", lb)

            if math.isfinite(gap):
                ub = ampl.get_objective("Z").value()
                print("UB:", ub)
                print("GAP (%):", 100 * gap)
            else:
                print("UB: sem solução inteira viável")
                print("GAP: infinito")

    except MemoryError:
        print("Impraticável: faltou memória.")

    except Exception as erro:
        print("Erro na execução:", erro)

    finally:
        total_time = time.perf_counter() - start
        print("Tempo total (segundos):", round(total_time, 2))

        if ampl is not None:
            ampl.close()