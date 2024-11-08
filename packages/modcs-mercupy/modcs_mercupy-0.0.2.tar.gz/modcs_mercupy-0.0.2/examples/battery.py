import itertools
import math
import os
import pandas as pd
import numpy as np
import time
from VSCode.battery_mercury_experiments.a002.mercupy.mercupy import *

# 6 5 1 0   2S2P
# 9 5 1 0   3S2P
# 72 5 6 1  20S7P

java_path = r'C:\Program Files\Java\jdk-1.8\bin\java.exe'
jar_mercury_path = r'X:\BK\UFPE\Mestrado\Mercury\trunk\dist\Mercury.jar'


def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


clear_terminal()

v_bat = 72
i_bat = 20
t_bat = 1
C_bat = i_bat * t_bat

cells = []
with open(r'X:\BK\Projetos\Projeto_Mestrado\VSCode\battery_mercury_experiments\lithium_cells.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(',')
        cells.append((parts[0], float(parts[1]), float(parts[2]), float(parts[3])))

    file.close()

df_cells = pd.DataFrame(cells, columns=['Battery Name', 'Nominal Voltage (V)', 'Continuous Discharge Current (A)', 'Capacity (mAh)'])
df_cells.index.name = 'Index'

print(df_cells)

selected_cell = df_cells.iloc[0]

print(f"Selected cell: {selected_cell['Battery Name']}")

print("-----------------------------------------------------------------------")
print("Results")
print("-----------------------------------------------------------------------")

print()

n_cells_series = math.ceil(v_bat / selected_cell['Nominal Voltage (V)'])
print(f"Number of cells in series: {n_cells_series}")

n_cells_parallel = math.ceil(C_bat / (selected_cell['Capacity (mAh)'] * 1e-3))
print(f"Number of cells in parallel: {n_cells_parallel}")

n_cells = n_cells_series * n_cells_parallel
print(f"Total number of cells: {n_cells}")

print()

print("Creating Mercury's Script...")

MNCD1PSOH_all = {
    "Group_1": (10.9032549732308, 3),
    "Group_2": (7.668014478961169, 3),
    "Group_3": (2.2271136238699802, 6),
    "Group_4": (2.135928112695071, 4),
    "Group_5": (1.2261594237806654, 5),
}

for group_name, (mean_delay, shape) in MNCD1PSOH_all.items():
    start_time = time.time()

    script = Mercury(
        java_path=java_path,
        mercury_jar_path=jar_mercury_path,
    )

    class INT_Vars(Enum):
        SOH_MIN = 0
        SOH_MAX = 20
        MNCD1PSOH_shape = round(shape)

    class REAL_Vars(Enum):
        MNCD1PSOH_mean_delay = mean_delay

    for var in INT_Vars:
        script.set_int_var(var.name, var.value)
    for var in REAL_Vars:
        script.set_real_var(var.name, var.value)

    cell_counter = itertools.count(start=0)
    transition_counter = itertools.count(start=0)

    battery_20S7P_SP = SPN.Model()

    place_cells_initial = [SPN.Place(name=f"P{next(cell_counter)}", tokens=INT_Vars.SOH_MAX.name) for _ in range(n_cells)]
    places_series_soh_deposit = [SPN.Place(name=f"P{next(cell_counter)}") for _ in range(n_cells)]
    places_series_ending = [SPN.Place(name=f"P{next(cell_counter)}") for _ in range(n_cells_parallel)]
    places_parallel_ending = [SPN.Place(name=f"P{next(cell_counter)}") for _ in range(n_cells_parallel)]
    place_battery_failure = SPN.Place(name=f"P{next(cell_counter)}")

    for place in [
            *place_cells_initial,
            *places_series_soh_deposit,
            *places_series_ending,
            *places_parallel_ending,
            place_battery_failure,
    ]:
        battery_20S7P_SP.add_place(place)

    immediate_transitions_series = [SPN.ImmediateTransition(
        name=f"TI{next(transition_counter)}",
        inputs=[(places_series_soh_deposit[i], f'{INT_Vars.SOH_MAX.name} - {INT_Vars.SOH_MIN.name}')],
        outputs=[(places_series_ending[i // n_cells_series], )],
    ) for i in range(n_cells)]

    immediate_transitions_parallel = [SPN.ImmediateTransition(
        name=f"TI{next(transition_counter)}",
        inputs=[(places_series_ending[i], )] + [(p, f'#{p.name}') for p in [*place_cells_initial[i * n_cells_series:i * n_cells_series + n_cells_series], *places_series_soh_deposit[i * n_cells_series:i * n_cells_series + n_cells_series]]],
        outputs=[(places_parallel_ending[i], )],
    ) for i in range(n_cells_parallel)]

    immediate_transition_failure = SPN.ImmediateTransition(
        name=f"TI{next(transition_counter)}",
        inputs=[(p, ) for p in places_parallel_ending],
        outputs=[(place_battery_failure, )],
    )

    timed_transition_soh_decay = [SPN.TimedTransition(
        name=f"TE{next(transition_counter)}",
        inputs=[(i, )],
        outputs=[(o, )],
        server_type=SPN.ServerType.SINGLE_SERVER,
        distribution='Erlang',
        distribution_params={
            "Mean_delay": REAL_Vars.MNCD1PSOH_mean_delay.name,
            "Shapes": INT_Vars.MNCD1PSOH_shape.name,
        },
    ) for i, o in zip(place_cells_initial, places_series_soh_deposit)]

    for transition in [
            *immediate_transitions_series,
            *immediate_transitions_parallel,
            immediate_transition_failure,
            *timed_transition_soh_decay,
    ]:
        battery_20S7P_SP.add_transition(transition)

    battery_20S7P_SP.set_metric(metric_name='UR', metric_expression=f'\"P{{#{place_battery_failure.name}>0}}\"')

    file_path = rf'X:/BK/Projetos/Projeto_Mestrado/VSCode/battery_mercury_experiments/a002/results/20S7P_sp_group_{group_name}'

    battery_20S7P_SP.add_solver(
        solver=SolverType.TRANSIENT_SIMULATION,
        metric_name='UR',
        parameters={
            "time": 1000,
            "confidenceLevel": .95,
            "maxRelativeError": .1,
            "samplingPoints": 100,
            "runs": 30,
            "replications": 50,
            "file": f'"{file_path}"',
        },
    )

    script.add_model(
        model_type=ModelType.SPN,
        model_name='battery',
        model_instance=battery_20S7P_SP,
    )

    script.run(script_path=f'{file_path}.txt')

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time Group {group_name}: {elapsed_time} seconds")
