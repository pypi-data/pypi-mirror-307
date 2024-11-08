from enum import Enum
import subprocess


class SolverType(Enum):
    TRANSIENT_ANALYSIS = "transientAnalysis"
    TRANSIENT_SIMULATION = "transientSimulation"
    STATIONARY_ANALYSIS = "stationaryAnalysis"
    STATIONARY_SIMULATION = "stationarySimulation"


class ModelType(Enum):
    RBD = "RBD"
    SPN = "SPN"
    CTMC = "CTMC"
    DTMC = "DTMC"
    ET = "ET"
    FT = "FT"


class SPN:

    class ServerType(Enum):
        SINGLE_SERVER = "ExclusiveServer"
        INFINITE_SERVER = "InfiniteServer"

    class TransitionType(Enum):
        IMMEDIATE_TRANSITION = "immediateTransition"
        TIMED_TRANSITION = "timedTransition"

    class Place:

        def __init__(self, name, tokens=None):
            self.name = name
            self.tokens = tokens

    class __Transition:

        def __init__(self, name, inputs=None, outputs=None, priority=None, guard=None):
            self.name = name
            self.inputs = inputs if inputs is not None else []
            self.outputs = outputs if outputs is not None else []
            self.priority = priority
            self.guard = guard

    class ImmediateTransition(__Transition):

        def __init__(self, name, inputs=None, outputs=None, weight=1, priority=None, guard=None):
            super().__init__(name, inputs, outputs, priority, guard)
            self.weight = weight

    class TimedTransition(__Transition):

        def __init__(
            self,
            name,
            inputs=None,
            outputs=None,
            priority=None,
            guard=None,
            server_type: 'SPN.ServerType' = None,
            distribution=None,
            distribution_params=None,
        ):
            super().__init__(name, inputs, outputs, priority, guard)
            self.server_type = server_type
            self.distribution = distribution
            self.distribution_params = distribution_params

    class Model:

        def __init__(self):
            self.places = []
            self.transitions = []
            self.metrics = []
            self.solvers = []

        def add_place(self, place: 'SPN.Place'):
            self.places.append(place)

        def add_transition(self, transition: 'SPN.__Transition'):
            self.transitions.append(transition)

        def add_solver(self, solver: SolverType, metric_name, parameters=None):
            self.solvers.append((solver.value, metric_name, parameters))

        def set_metric(self, metric_name, metric_expression):
            self.metrics.append((metric_name, metric_expression))


class Mercury:

    def __init__(self, java_path=None, mercury_jar_path=None):
        self.int_vars = {}
        self.real_vars = {}
        self.models = {model_type.value: [] for model_type in ModelType}
        self.solvers = []
        self.java_path = java_path
        self.mercury_jar_path = mercury_jar_path

    def set_int_var(self, name, value):
        self.int_vars[name] = value

    def set_real_var(self, name, value):
        self.real_vars[name] = value

    def add_model(self, model_type: ModelType, model_instance, model_name):
        self.models[model_type.value].append((model_name, model_instance))

    def __generate_script(self):
        script_parts = []

        for name, value in self.real_vars.items():
            script_parts.append(f"{name} = {value};")
        for name, value in self.int_vars.items():
            script_parts.append(f"{name} = {value};")

        for model_type_str, models in self.models.items():
            for model_name, model in models:
                model_script = [f"\n{model_type_str} {model_name}{{"]
                if model_type_str == ModelType.SPN.value:
                    for place in model.places:
                        if place.tokens is not None:
                            model_script.append(f"\tplace {place.name}( tokens = {place.tokens} );")
                        else:
                            model_script.append(f"\tplace {place.name};")
                    for transition in model.transitions:
                        if isinstance(transition, SPN.ImmediateTransition):
                            transition_type = SPN.TransitionType.IMMEDIATE_TRANSITION.value
                        elif isinstance(transition, SPN.TimedTransition):
                            transition_type = SPN.TransitionType.TIMED_TRANSITION.value
                        else:
                            transition_type = "transition"
                        trans_script = [f"\t{transition_type} {transition.name}("]
                        params = []
                        if transition.inputs:
                            inputs = ', '.join([f"{input_tuple[0].name}({input_tuple[1]})" if len(input_tuple) > 1 and input_tuple[1] is not None else f"{input_tuple[0].name}" for input_tuple in transition.inputs])
                            params.append(f"inputs = [{inputs}]")
                        if transition.outputs:
                            outputs = ', '.join([f"{output_tuple[0].name}({output_tuple[1]})" if len(output_tuple) > 1 and output_tuple[1] is not None else f"{output_tuple[0].name}" for output_tuple in transition.outputs])
                            params.append(f"outputs = [{outputs}]")
                        if transition.priority is not None:
                            params.append(f"priority = {transition.priority}")
                        if transition.guard is not None:
                            params.append(f"guard = {transition.guard}")
                        if isinstance(transition, SPN.TimedTransition):
                            if transition.distribution is not None and transition.distribution_params is not None:
                                params_str = ', '.join(f"{k} = {v}" for k, v in transition.distribution_params.items())
                                delay_script = f"delay = ( type = \"{transition.distribution}\", parameters = ({params_str}) )"
                                params.append(delay_script)
                            if transition.server_type is not None:
                                server_type = transition.server_type.value
                                params.append(f"serverType = \"{server_type}\"")
                        if isinstance(transition, SPN.ImmediateTransition):
                            if transition.weight != 1:
                                params.append(f"weight = {transition.weight}")
                        trans_script.append('\t\t' + ',\n\t\t'.join(params))
                        trans_script.append("\t);")
                        model_script.extend(trans_script)
                    for solver, metric_name, parameters in model.solvers:
                        metric_expression = next((metric for metric in model.metrics if metric[0] == metric_name), None)
                        if metric_expression and parameters:
                            params_str = ',\n\t\t\t'.join(f"{k} = {v}" for k, v in parameters.items())
                            model_script.append(f"\n\tmetric {metric_name} = {solver}(\n\t\texpression = {metric_expression[1]},\n\t\tparameters = (\n\t\t\t{params_str}\n\t\t)\n\t);")
                    model_script.append("}\n")
                    script_parts.append('\n'.join(model_script))
                else:
                    pass

        main_script = ["main{"]
        if self.int_vars:
            keys = [f'\"{key}\"' for key in self.int_vars.keys()]
            main_script.append(f"\tsetIntegerParameters({', '.join(keys)});")
        for model_type_str, models in self.models.items():
            for model_name, model in models:
                if model.solvers:
                    for solver, metric_name, parameters in model.solvers:
                        main_script.append(f"\t{metric_name} = solve({model_name}, {metric_name});")
                        main_script.append(f"\tprintln({metric_name});")
        main_script.append("}")
        script_parts.append('\n'.join(main_script))

        return '\n'.join(script_parts)

    def run(self, script_path):
        print("Writing Mercury's script...")
        script = self.__generate_script()
        # print("start----------------------------------------------------------------")
        # print(script)
        # print("end----------------------------------------------------------------")
        print("The script has been written!")
        print("Saving script file...")
        with open(script_path, "w") as f:
            f.write(script)
        print("The script file has been saved!")
        command = [self.java_path, '-jar', self.mercury_jar_path, '-cli', script_path]
        print("Running Mercury's script...")
        try:
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error:\n{e.stderr}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
