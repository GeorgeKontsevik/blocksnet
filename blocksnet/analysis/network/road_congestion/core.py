import pandas as pd
import networkx as nx
import numpy as np
from blocksnet.relations.accessibility import validate_accessibility_graph
from ..origin_destination import validate_od_matrix
from tqdm import tqdm
from blocksnet.config import log_config
from loguru import logger

CONGESTION_KEY = "congestion"

ONE_CAPACITY = 1000

LANES_COEF = {
    1: 1.0,
    2: 0.95,
    3: 0.90,
    4: 0.86,
    5: 0.84,
}


def _get_capacity_by_lanes(lanes):
    capacity = ONE_CAPACITY * LANES_COEF[lanes] * lanes

    return capacity

def _normalize_lanes(G: nx.Graph, default: int = 1) -> nx.Graph:
    for _, _, data in G.edges(data=True):
        raw = data.get("lanes", None)

        # list -> возьмём минимальное 
        if isinstance(raw, list):
            raw = min(raw) if raw else None

        # str -> попробуем вытащить число
        if isinstance(raw, str):
            s = raw.strip()
            for sep in [";", "|", ","]:
                if sep in s:
                    s = s.split(sep)[0].strip()
                    break
            raw = s

        try:
            lanes = int(float(raw))  
        except (TypeError, ValueError):
            lanes = default

        if lanes < 1:
            lanes = default

        data["lanes"] = lanes

    return G


def _add_intensity(G: nx.Graph, intensity_default: float = 0) -> nx.Graph:

    for _, _, data in G.edges(data=True):
        data["intensity"] = intensity_default

    return G


def _add_capacity(G: nx.Graph) -> nx.Graph:
    for _, _, data in G.edges(data=True):
        lanes = data.get("lanes", 1)
        data["capacity"] = _get_capacity_by_lanes(lanes)
    return G


def _peprocess_graph(G: nx.Graph) -> nx.Graph:
    H = G.copy()
    _normalize_lanes(H)
    _add_intensity(H)
    _add_capacity(H)
    return H


def road_congestion(od_mx: pd.DataFrame, G: nx.MultiDiGraph, weight_key: str = "time_min") -> nx.MultiDiGraph:
    
    validate_od_matrix(od_mx, G)
    validate_accessibility_graph(G, weight_key)

    logger.info("Preprocessing graph")
    H = _peprocess_graph(G)
    graph_congestion = H.copy()
    graph_routing = H.copy()

    for _, _, k, data in graph_congestion.edges(keys=True, data=True):
        data["intensity"] = 0.0

    logger.info("Calculating shortest paths")
    for i in tqdm(od_mx.index, disable=log_config.disable_tqdm):
        for j, demand in od_mx.loc[i].items():
            if i == j or demand <= 0:
                continue

            trips = int(round(float(demand)))

            for _ in range(trips):
                try:
                    route = nx.shortest_path(graph_routing, source=i, target=j, weight=weight_key, method="dijkstra")
                except (nx.NetworkXNoPath, nx.NodeNotFound):
                    break

                for u, v in zip(route[:-1], route[1:]):
                    k = min(graph_routing[u][v], key=lambda kk: graph_routing[u][v][kk].get(weight_key, np.inf))

                    graph_routing[u][v][k]["intensity"] += 1.0
                    graph_congestion[u][v][k]["intensity"] += 1.0

                    capacity = float(graph_routing[u][v][k]["capacity"])
                    load_level = graph_routing[u][v][k]["intensity"] / max(capacity, 1e-9)
                    if load_level > 1.0:
                        graph_routing.remove_edge(u, v, key=k)

    logger.info("Computing load level")
    for _, _, _, data in graph_congestion.edges(keys=True, data=True):
        data["load_level"] = data["intensity"] / max(data["capacity"], 1e-9)

    return graph_congestion