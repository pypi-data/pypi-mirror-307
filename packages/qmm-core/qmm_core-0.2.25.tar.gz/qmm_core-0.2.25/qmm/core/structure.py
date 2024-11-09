import json
from typing import Union, List, Dict, Tuple
import networkx as nx
import sympy as sp
from .helper import get_nodes

def import_digraph(data, file_path=True) -> nx.DiGraph:
    if file_path:
        with open(data, "r") as file:
            data = json.load(file)
    G = nx.DiGraph()
    for node in data["nodes"]:
        att = {k: v for k, v in node.items() if k != "id"}
        G.add_node(str(node["id"]), **att)
    for edge in data["edges"]:
        source, target = str(edge["from"]), str(edge["to"])
        att = {k: v for k, v in edge.items() if k not in ["from", "to", "arrows"]}
        arr = edge.get("arrows", {}).get("to", {})
        if isinstance(arr, dict):
            arr_type = arr.get("type")
            if arr_type == "triangle":
                att["sign"] = 1
            elif arr_type == "circle":
                att["sign"] = -1
        G.add_edge(source, target, **att)
    nx.set_node_attributes(G, "state", "category")
    return G

def create_matrix(G, form="symbolic", matrix_type="A") -> sp.Matrix:
    if not isinstance(G, nx.DiGraph):
        raise TypeError("Input must be a networkx.DiGraph.")
    if form not in ["symbolic", "signed", "binary"]:
        raise ValueError("Invalid form. Choose 'symbolic', 'signed', or 'binary'.")
    if matrix_type not in ["A", "B", "C", "D"]:
        raise ValueError("Invalid matrix_type. Choose 'A', 'B', 'C', or 'D'.")
    def sym(source: str, target: str, prefix: str) -> sp.Symbol:
        return sp.Symbol(f"{prefix}_{target},{source}")
    def sign(source: str, target: str, prefix: str) -> Union[sp.Symbol, int]:
        if form == "symbolic":
            return sym(source, target, prefix) * G[source][target].get("sign", 1)
        elif form == "signed":
            return G[source][target].get("sign", 1)
        else:  # form == 'binary'
            return int(G.has_edge(source, target))
    def product(path: List[str]) -> Union[sp.Symbol, int]:
        effect = 1
        for i in range(len(path) - 1):
            effect *= sign(path[i], path[i + 1], prefix)
        return effect
    state_n = get_nodes(G, "state")
    input_n = get_nodes(G, "input")
    output_n = get_nodes(G, "output")
    matrix_configs: Dict[str, Tuple[List[str], List[str], str, str]] = {
        "A": (state_n, state_n, "a", "state"),
        "B": (state_n, input_n, "b", "input"),
        "C": (output_n, state_n, "c", "output"),
        "D": (output_n, input_n, "d", "input"),
    }
    rows, cols, prefix, category = matrix_configs[matrix_type]
    matrix = sp.zeros(len(rows), len(cols))
    for i, target in enumerate(rows):
        for j, source in enumerate(cols):
            if matrix_type == "A":
                if G.has_edge(source, target):
                    matrix[i, j] = sign(source, target, prefix)
            else:
                paths = nx.all_simple_paths(G, source, target)
                valid = [p for p in paths if all(G.nodes[n]["category"] == category for n in p[1:-1])]
                matrix[i, j] = sum(product(path) for path in valid)
    return matrix

def create_equations(G, form="state") -> sp.Matrix:
    if not isinstance(G, nx.DiGraph):
        raise TypeError("Input must be a networkx.DiGraph.")
    if form not in ["state", "output"]:
        raise ValueError("Invalid form. Choose 'state' or 'output'.")
    A = create_matrix(G, form="symbolic", matrix_type="A")
    B = create_matrix(G, form="symbolic", matrix_type="B")
    C = create_matrix(G, form="symbolic", matrix_type="C")
    D = create_matrix(G, form="symbolic", matrix_type="D")
    state_nodes = get_nodes(G, "state")
    input_nodes = get_nodes(G, "input")
    output_nodes = get_nodes(G, "output")
    x = sp.Matrix([sp.Symbol(f"x_{i}") for i in state_nodes])
    u = sp.Matrix([sp.Symbol(f"u_{i}") for i in input_nodes]) if input_nodes else None
    if form == "state":
        equations = A * x
        if B.shape[1] > 0 and u is not None:
            equations += B * u
        return equations
    if not output_nodes:
        raise ValueError("No output nodes found in graph")
    equations = C * x
    if D.shape[1] > 0 and u is not None:
        equations += D * u
    return equations
