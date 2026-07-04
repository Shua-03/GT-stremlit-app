import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import math
import copy
import io
import sys
import inspect

st.set_page_config(page_title="Graph Theory Lab", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&family=Source+Code+Pro:wght@400;600&display=swap');

/* Fixed header banner */
.fixed-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 9999;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    padding: 14px 36px;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 4px 24px rgba(0,0,0,0.5);
}
.fixed-header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(ellipse at center, rgba(108,92,231,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.fixed-header h1 {
    font-family: 'Cinzel', serif;
    font-size: 1.55rem;
    font-weight: 900;
    color: #fff;
    letter-spacing: 0.06em;
    margin: 0 0 2px 0;
    text-shadow: 0 0 30px rgba(108,92,231,0.8), 0 2px 4px rgba(0,0,0,0.5);
}
.fixed-header .sub {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.72rem;
    color: rgba(200,185,255,0.75);
    letter-spacing: 0.18em;
    text-transform: uppercase;
}

/* Fixed footer banner */
.fixed-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 9999;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    padding: 10px 36px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 -4px 20px rgba(0,0,0,0.4);
}
.roll {
    font-family: 'Cinzel', serif;
    font-size: 1rem;
    font-weight: 700;
    color: #a78bfa;
    letter-spacing: 0.12em;
}
.footer-name {
    font-family: 'Cinzel', serif;
    font-size: 1rem;
    font-weight: 700;
    color: #a78bfa;
    letter-spacing: 0.08em;
}
.footer-roll {
    font-family: 'Cinzel', serif;
    font-size: 1rem;
    font-weight: 700;
    color: #a78bfa;
    letter-spacing: 0.12em;
}
.fixed-footer .copy {
    font-family: 'Source Code Pro', monospace;
    font-size: 0.68rem;
    color: rgba(200,185,255,0.5);
    margin-top: 1px;
    letter-spacing: 0.1em;
}

/* Push content down so it doesn't hide behind fixed header */
.block-container {
    padding-top: 100px !important;
    padding-bottom: 80px !important;
}

/* Sidebar top padding */
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 90px !important;
}

.exp-aim-box {
    background: linear-gradient(135deg, rgba(108,92,231,0.10), rgba(36,36,62,0.6));
    border-left: 4px solid #7c3aed;
    border-radius: 0 8px 8px 0;
    padding: 12px 20px;
    margin: 8px 0 18px 0;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.88rem;
    color: #c4b5fd;
}
.exp-aim-box strong {
    color: #a78bfa;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    display: block;
    margin-bottom: 4px;
}

.exp-theory-box {
    background: linear-gradient(135deg, rgba(36,36,62,0.55), rgba(15,12,41,0.45));
    border-left: 4px solid #38bdf8;
    border-radius: 0 8px 8px 0;
    padding: 16px 22px;
    margin: 14px 0;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.85rem;
    line-height: 1.55;
    color: #dbeafe;
}
.exp-theory-box h4 {
    color: #7dd3fc;
    font-family: 'Cinzel', serif;
    font-size: 1rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0 0 10px 0;
}
.exp-conclusion-box {
    background: linear-gradient(135deg, rgba(60,36,90,0.55), rgba(15,12,41,0.45));
    border-left: 4px solid #34d399;
    border-radius: 0 8px 8px 0;
    padding: 14px 22px;
    margin: 6px 0 18px 0;
    font-family: 'Source Code Pro', monospace;
    font-size: 0.85rem;
    line-height: 1.5;
    color: #d1fae5;
}
.exp-conclusion-box h4 {
    color: #6ee7b7;
    font-family: 'Cinzel', serif;
    font-size: 1rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0 0 8px 0;
}
</style>

<!-- Fixed Header -->
<div class="fixed-header">
    <h1>CMP-226 Graph Theory and Combinatorics Lab</h1>
    <div class="roll">CMP-226 Graph Theory and Combinatorics Lab</div>
</div>

<!-- Fixed Footer -->
<div class="fixed-footer">
    <div class="footer-name">Dhanshri Sarkate</div>
    <div class="footer-roll">24B-CO-502</div>
</div>
""", unsafe_allow_html=True)

#   Sidebar   
experiment = st.sidebar.selectbox(
    "Choose Experiment",
    [
        "Exp 1 - Types of Graphs",
        "Exp 2 - Graph Isomorphism",
        "Exp 3 - Subgraphs",
        "Exp 4 - Havel-Hakimi (Degree Sequence)",
        "Exp 5 - Line Graph",
        "Exp 6 - Minimum Spanning Tree (Kruskal)",
        "Exp 7 - Dijkstra's Shortest Path",
        "Exp 8 - Walk / Trail / Path",
        "Exp 9 - Eulerian Circuit",
        "Exp 10 - Hamiltonian Circuit",
        "Exp 11 - Graph Coloring + Sudoku",
    ],
)

if experiment == "Exp 11 - Graph Coloring + Sudoku":
    mode = st.sidebar.radio(
        "Implementation",
        ["With Inbuilt Functions", "Manual Implementation", "Sudoku"],
    )
else:
    mode = st.sidebar.radio("Implementation", ["With Inbuilt Functions", "Manual Implementation"])

run_btn = st.sidebar.button("Run Experiment", use_container_width=True)

#   Aim mapping  ───────────────
AIMS = {
    "Exp 1 - Types of Graphs":
        "To implement basic graphs as null graph, complete graph, cycle graph, path graph, complete bipartite graph and wheel graph.",
    "Exp 2 - Graph Isomorphism":
        "To implement isomorphism verification in order to compare structural equivalence between two graphs.",
    "Exp 3 - Subgraphs":
        "To implement generation of various subgraphs such as induced, edge induced, and edge deleted subgraphs.",
    "Exp 4 - Havel-Hakimi (Degree Sequence)":
        "To implement a graph for a given degree sequence.",
    "Exp 5 - Line Graph":
        "Convert the original graph into its line graph, where each edge of the original graph becomes a vertex in the new graph, and adjacency is defined by shared endpoints in the original graph.",
    "Exp 6 - Minimum Spanning Tree (Kruskal)":
        "To implement finding the minimum spanning tree for a given graph using Kruskal's algorithm, ensuring all vertices are connected with the minimum possible total edge weight and without forming cycles.",
    "Exp 7 - Dijkstra's Shortest Path":
        "To implement shortest path algorithm in order to compute the shortest path from the source vertex to all the other vertices in a weighted graph.",
    "Exp 8 - Walk / Trail / Path":
        "To implement generation of closed walks, trails and paths in a connected graph.",
    "Exp 9 - Eulerian Circuit":
        "To implement an algorithm that checks existence for Eulerian circuit and construct a circuit that traverses every edge of the graph exactly once.",
    "Exp 10 - Hamiltonian Circuit":
        "To implement a method whether a graph contains a Hamiltonian circuit that is a cycle that visits every vertex exactly once.",
    "Exp 11 - Graph Coloring + Sudoku":
        "To implement greedy graph colouring algorithm that assigns colour to the vertices such that no two vertices share the same colour with minimal chromatic number.",
}

#   Theory mapping (shown for both "With Inbuilt Functions" and "Manual Implementation") ──
THEORY = {
    "Exp 1 - Types of Graphs": """
NetworkX is a Python library used for the creation, manipulation, and study of graphs and networks. It provides built-in data structures for representing different types of graphs such as undirected graphs, directed graphs, and multigraphs. In this experiment, NetworkX is used to implement basic graph types including null graphs, complete graphs, cycle graphs, path graphs, complete bipartite graphs, and wheel graphs.

The main advantage of NetworkX is that it provides predefined functions such as complete_graph(), cycle_graph(), path_graph(), complete_bipartite_graph(), and wheel_graph(), which allow direct construction of standard graph structures without manually defining all edges. It also provides layout algorithms such as spring_layout(), circular_layout(), shell_layout(), and bipartite_layout() to arrange vertices in meaningful positions for visualization.

Matplotlib is a widely used Python library for graphical representation and visualization. While NetworkX defines the structure of the graph (vertices and edges), Matplotlib is responsible for rendering the graphical output on the screen, allowing customization of node size, color, edge style, labels, and titles.

**Types of graphs:**

1) **Null Graph** — A graph consisting of a set of vertices with no edges connecting them, denoted Nn. Every vertex has degree zero. Implemented by adding nodes but providing no edge list.

2) **Complete Graph** — A simple undirected graph in which every pair of distinct vertices is connected by exactly one edge, denoted Kn. It has n(n-1)/2 edges and every vertex has degree n-1. Implemented using nx.complete_graph(n), or manually with a double loop ensuring every vertex is adjacent to every other vertex exactly once.

3) **Cycle Graph** — A connected graph in which each vertex has degree 2, forming a single closed loop, denoted Cn with n edges. Implemented using nx.cycle_graph(n), or manually using the modulo operator (%) to connect the last node back to the first, creating a closed loop.

4) **Path Graph** — Vertices arranged in a linear sequence; end vertices have degree 1, intermediate vertices have degree 2, denoted Pn with n-1 edges. Implemented using nx.path_graph(n), or manually by connecting consecutive vertices in sequence.

5) **Complete Bipartite Graph** — Vertices divided into two disjoint sets such that every vertex in one set is connected to every vertex in the other set, with no edges within the same set, denoted K(m,n) with m×n edges. Implemented using nx.complete_bipartite_graph(m, n), visualized with bipartite_layout().

6) **Wheel Graph** — Formed by connecting one central hub vertex to all vertices of a cycle graph, denoted Wn with 2(n-1) edges. Implemented using nx.wheel_graph(n), or manually by first creating a cycle (the "rim") and then connecting a separate "hub" node to every node on that rim.
""",
    "Exp 2 - Graph Isomorphism": """
Graph isomorphism determines if two graphs possess the same structural connection pattern, regardless of how their vertices are labeled or visually depicted. Two graphs G1 and G2 are isomorphic if there exist bijections between their vertex sets and edge sets that preserve the incidence relation — the graphs differ only in the names of their vertices and edges, but their underlying structures remain identical.

To verify isomorphism, several structural invariants are evaluated:
- **Degree sequence** — the sorted list of vertex degrees. If two graphs have different degree sequences, they cannot be isomorphic.
- **Cycle structure** — the number and lengths of independent cycles, given by the formula (edges − vertices + 1) for a connected graph.
- **Adjacency matrix** — a matrix where entry (i, j) denotes the number of edges joining vertices i and j; for isomorphic graphs, one adjacency matrix can be transformed into the other by permuting rows and columns according to the bijection.

**Manual implementation:** len(list) is used to compare vertex/edge counts. get_manual_degree_sequence() iterates through the vertex set to count incident edges for each node, returning a sorted list. get_manual_adj_matrix() constructs the connection matrix by checking every pair of vertices for an edge. verify_mapping() takes a manually defined bijection and checks whether every edge in G1 maps to a corresponding edge in G2, returning a Boolean.

**Inbuilt implementation:** nx.circular_layout() and nx.bipartite_layout() return node position dictionaries for visualization. G.number_of_nodes() and G.number_of_edges() give global counts. G.degree() returns a DegreeView, sorted with sorted(). nx.to_numpy_array() returns the adjacency matrix as a NumPy array. nx.isomorphism.GraphMatcher() searches for a bijection; GM.is_isomorphic() returns a Boolean, and if True, GM.mapping returns the node-to-node bijection.
""",
    "Exp 3 - Subgraphs": """
A graph is formally defined as an ordered triple consisting of a non-empty set of vertices, a set of edges, and an incidence function that associates each edge with a pair of vertices. A subgraph is formed by selecting a subset of the original vertices and edges such that the original incidence relation is preserved.

- A **spanning subgraph** has a vertex set exactly equal to that of the original graph, containing every original vertex even if some edges are removed.
- A **vertex-induced subgraph** is defined by a chosen subset of vertices and must contain every edge from the original graph that joins two vertices within that subset.
- An **edge-induced subgraph** is determined by a selected subset of edges, and its vertex set is restricted solely to the vertices that serve as endpoints for those edges.

**Inbuilt implementation:** nx.Graph() initializes the graph container. G.subgraph() returns a vertex-induced subgraph, automatically including all corresponding edges. G.edge_subgraph() returns an edge-induced subgraph containing strictly the specified edges and their incident vertices. G.copy() combined with G.remove_edges_from() is used to build a spanning subgraph that keeps the vertex set identical while removing specific edges.

**Manual implementation:** For a spanning subgraph, every vertex is added with add_node() and then a chosen subset of edges is added. For a vertex-induced subgraph, only selected vertices are added, then the entire original edge set is iterated to add a link only if both endpoints are members of the chosen subset. For an edge-induced subgraph, a chosen list of edges is added directly; add_edge() automatically includes the incident endpoints. plt.subplot() and nx.draw() are used to visualize the results side by side.
""",
    "Exp 4 - Havel-Hakimi (Degree Sequence)": """
A graph is an ordered triple (V, E, ψ) consisting of vertices, edges, and an incidence function mapping each edge to an unordered pair of vertices. The degree of a vertex is the number of edges incident with it, and the sum of all vertex degrees must equal exactly twice the number of edges. A degree sequence is the list of vertex degrees arranged in non-increasing order, and a sequence is termed **graphic** if there exists a simple graph that possesses that exact sequence of degrees.

The **Havel-Hakimi Theorem** provides the recursive algorithm to determine if a sequence is graphic and to construct a representative simple graph: a non-increasing sequence is graphic if and only if the reduced sequence — formed by deleting the largest element and subtracting one from each of the next elements — is also graphic. This reduction simulates connecting the vertex with the highest degree to the vertices with the next highest degrees. If the process results in all zeros, the sequence is graphic; if it produces negative numbers or requires more neighbors than available vertices, it is not graphical.

**Inbuilt implementation:** nx.havel_hakimi_graph() takes a degree sequence and returns a Graph object realized through the theorem's logic, visualized with nx.circular_layout() or nx.spring_layout() and nx.draw().

**Manual implementation:** len(list) determines the number of vertices; nx.Graph() creates an empty graph. A while loop continuously sorts the vertex-degree pairs in non-increasing order using list.sort(reverse=True). The vertex with maximum degree is removed, and G.add_edge(u, v) is called to join it to the next-highest-degree vertices, decrementing their required degree by one each time — mimicking the mathematical subtraction of the theorem step-by-step.
""",
    "Exp 5 - Line Graph": """
Given a graph G = (V, E), its line graph L(G) is a graph in which each vertex represents an edge of G, so the vertex set V(L(G)) is in one-to-one correspondence with the edge set E(G). Two distinct vertices in L(G) are adjacent if and only if their corresponding edges in G are incident to a common vertex — this transformation converts the property of edge incidence in G into the property of vertex adjacency in L(G).

**Inbuilt implementation:** The original graph G is defined through its edge set and vertex set. nx.line_graph(G) automates the mapping E(G) → V(L(G)) by inspecting the endpoints of each edge pair in G, creating a link in L(G) whenever two edges share a common vertex.

**Manual implementation:** The edges of G are represented as a set of tuples E = {e1, e2, …, em}. A new adjacency matrix A′ of dimension m × m is initialized, and the algorithm iterates through every pair of edges, comparing their endpoints — if the intersection of their vertex sets is non-empty, the corresponding entry in A′ is set to 1.

In weighted applications, an edge in L(G) can be assigned a weight equal to the sum of the weights of its two incident edges in G.
""",
    "Exp 6 - Minimum Spanning Tree (Kruskal)": """
A spanning tree of a connected, undirected graph G = (V, E) is a subgraph T that is a tree and includes all the vertices of V. When each edge is assigned a real-valued weight, the graph is a weighted graph, and the weight of a spanning tree is the sum of the weights of its edges. A **Minimum Spanning Tree (MST)** is a spanning tree whose total weight is less than or equal to that of every other spanning tree in G — representing the most efficient way to connect a set of locations with minimum total cost.

**Kruskal's Algorithm** is a greedy strategy based on edge-addition. It begins with an empty edge set and treats every vertex as a separate component (a forest). Edges are processed in non-decreasing order of weight; for each edge {u, v}, if u and v belong to different components the edge is added (since it cannot form a cycle) and the components are merged. This continues until n−1 edges have been added, forming a spanning tree. Sorting ensures the smallest-weight edges are considered first, while component tracking (e.g. a Disjoint Set Union structure) guarantees no cycles are formed.

**Inbuilt implementation** uses nx.minimum_spanning_edges(), which abstracts the manual handling of components while applying an efficient implementation of Kruskal's or Prim's algorithm internally.
""",
    "Exp 7 - Dijkstra's Shortest Path": """
The Shortest Path Problem seeks a path between two vertices such that the sum of the weights of its edges is minimized. Given a weighted graph G where each edge has a non-negative weight, the distance between two vertices is the minimum weight among all possible connecting paths. A **Shortest Path Tree** is a spanning tree rooted at a source vertex containing the shortest paths to all other reachable vertices.

**Dijkstra's Algorithm** is a label-setting, greedy algorithm for the single-source shortest path problem. Vertices are partitioned into a "reached" set (finalized shortest distance) and an "unreached" set. The source is assigned distance 0, all others infinity. In each iteration, the unreached vertex with the smallest distance label is moved to the reached set and its outgoing edges are "relaxed": if d(u) + w(u, v) < d(v), the label d(v) is updated. This greedy selection guarantees that once a vertex is reached, no shorter path to it can exist.

**Inbuilt implementation** uses nx.single_source_dijkstra(), which uses a Min-Priority Queue / Fibonacci Heap internally, changing the time complexity from quadratic to near-linear in the number of edges, and abstracting the manual relaxation steps.

**Manual implementation** explicitly maintains a distance dictionary and predecessor dictionary, repeatedly selecting the unvisited vertex with the minimum distance label and relaxing its neighboring edges, mirroring the textbook algorithm step-by-step.
""",
    "Exp 8 - Walk / Trail / Path": """
A **walk** in a graph G is a finite sequence of alternating vertices and edges; a closed walk starts and ends at the same vertex, and both vertices and edges may repeat. A **trail** is a walk in which all edges are distinct (vertices may repeat); a closed trail is also called a circuit. A **path** is a walk in which all vertices (and hence all edges) are distinct; a closed path is called a cycle.

**Manual implementation:** For a closed walk, a sequence of incident edges that returns to the origin is chosen, intentionally repeating an edge to demonstrate that edge repetition is permissible. For a closed trail, a sequence is chosen where every edge is unique even if a vertex is revisited. For a closed path, the sequence is restricted so no internal vertex repeats, forming a simple cycle. nx.draw_networkx_edges() highlights the chosen sequence in red against the original graph.

**Inbuilt implementation:** nx.find_cycle(G) uses a DFS-based algorithm to locate a closed path where every vertex has degree exactly two within the found edge set. nx.eulerian_circuit() (applied to a known-Eulerian subgraph) uses Hierholzer's Algorithm to find a closed trail. nx.shortest_path() combined with reversing the path is used to programmatically construct a closed walk that repeats edges.
""",
    "Exp 9 - Eulerian Circuit": """
An **Eulerian circuit** is a closed trail that traverses every edge of a graph exactly once. A connected graph contains an Eulerian circuit if and only if every vertex has even degree — because a circuit must enter and leave each vertex it passes through, and an odd-degree vertex would break this entry/exit balance.

**Fleury's Algorithm** provides a constructive procedure: starting from an arbitrary vertex, at each step choose an edge incident to the current vertex that is not a cut edge (bridge) of the remaining graph, unless there is no alternative; stop when no edge can be chosen. This produces a valid Eulerian trail.

**Manual implementation:** The algorithm checks connectivity and verifies even degree for all vertices. To identify bridges, a candidate edge is temporarily removed and the number of connected components is compared before and after; if the count increases, the edge is a bridge. The algorithm iterates through the neighbors of the current vertex, preferring a non-bridge edge whenever possible, continuing until the edge set is empty.

**Inbuilt implementation** uses nx.is_eulerian() to check the existence condition and nx.eulerian_circuit() to compute the circuit directly.
""",
    "Exp 10 - Hamiltonian Circuit": """
A cycle that includes every vertex of G is a **Hamilton cycle** (Hamiltonian circuit); a graph containing at least one is called Hamiltonian. Unlike Eulerian circuits, which are characterized by vertex-degree parity, determining whether a general graph is Hamiltonian is NP-complete — there is no known simple necessary-and-sufficient condition.

Sufficient conditions rely on vertex degrees. **Dirac's Theorem** (1952): if G is simple with n ≥ 3 vertices and every vertex has degree ≥ n/2, then G is Hamiltonian. **Ore's Theorem** (1960) generalizes this: if for every pair of non-adjacent vertices u, v, d(u) + d(v) ≥ n, then G is Hamiltonian.

The **Bondy–Chvátal Closure**: if non-adjacent vertices u, v satisfy d(u) + d(v) ≥ n, then G is Hamiltonian if and only if G + uv is Hamiltonian. Repeatedly applying this builds the closure c(G); the Bondy–Chvátal Theorem states G is Hamiltonian if and only if c(G) is Hamiltonian, and if c(G) is complete, G is guaranteed Hamiltonian.

**Implementation:** the manual algorithm verifies the existence of the circuit by identifying a sequence of edges forming a closed trail that visits every vertex exactly once (no separate inbuilt NetworkX function exists for Hamiltonian circuits).
""",
    "Exp 11 - Graph Coloring + Sudoku": """
A **k-vertex colouring** of a graph G is an assignment of k colours to the vertices such that no two adjacent vertices receive the same colour, partitioning V(G) into k independent sets called colour classes. The minimum number of colours required is the **chromatic number**, χ(G). The greedy colouring algorithm guarantees any graph can be coloured using at most Δ(G) + 1 colours, where Δ(G) is the maximum vertex degree.

This implementation follows the **Saturation Largest First (DSATUR)** heuristic, a variant of greedy colouring that dynamically prioritizes the "most constrained" vertices first. The saturation degree of an uncoloured vertex is the number of distinct colours already assigned to its adjacent neighbours. In each iteration, the algorithm selects the vertex with maximum saturation degree (using vertex degree or alphabetical order as a tie-breaker) and assigns it the smallest available colour from a predefined sequence (Red, Green, Blue, Yellow).

**Inbuilt implementation** uses nx.coloring.greedy_color(G, strategy='DSATUR'), which internally manages adjacency relationships and saturation degrees, returning a dictionary mapping each vertex to a colour-class index.

**Manual implementation** builds the DSATUR logic from scratch: it computes the saturation degree of each uncoloured vertex by counting distinct neighbour colours, selects the most saturated vertex (breaking ties alphabetically), and assigns it the smallest colour not used by its coloured neighbours, repeating until all vertices are coloured.

For the **Sudoku** mode, the 4×4 puzzle is modeled as a graph via nx.sudoku_graph(2) (equivalent to a proper 4-colouring problem), and solved with a backtracking constraint-satisfaction search that checks row, column, and sub-grid constraints (is_safe()) before assigning each digit.
""",
}

CONCLUSIONS = {
    "Exp 1 - Types of Graphs":
        "Successfully implemented basic graphs as null graph, complete graph, cycle graph, path graph, complete bipartite graph and wheel graph using NetworkX.",
    "Exp 2 - Graph Isomorphism":
        "Isomorphism verification in order to compare structural equivalence between two graphs was successfully implemented.",
    "Exp 3 - Subgraphs":
        "Generation of various subgraphs such as induced, edge induced, and edge deleted subgraphs was successfully implemented.",
    "Exp 4 - Havel-Hakimi (Degree Sequence)":
        "A graph for a given degree sequence was successfully implemented using NetworkX.",
    "Exp 5 - Line Graph":
        "Conversion of the original graph into its line graph was successfully implemented.",
    "Exp 6 - Minimum Spanning Tree (Kruskal)":
        "The Minimum Spanning Tree for the given graph was successfully implemented using Kruskal's algorithm.",
    "Exp 7 - Dijkstra's Shortest Path":
        "The implementation of the shortest path algorithm using Dijkstra's algorithm was successfully completed.",
    "Exp 8 - Walk / Trail / Path":
        "Closed walks, trails and paths were successfully generated in a connected graph.",
    "Exp 9 - Eulerian Circuit":
        "An algorithm to check the existence of an Eulerian circuit was successfully implemented.",
    "Exp 10 - Hamiltonian Circuit":
        "A method to determine whether a graph contains a Hamiltonian circuit was implemented successfully.",
    "Exp 11 - Graph Coloring + Sudoku":
        "The greedy graph colouring algorithm was implemented successfully.",
}

#   Code strings for display  
CODE_EXP11_INBUILT = '''\
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
edges = [
    ('A', 'B'), ('A', 'G'), ('A', 'E'), ('A', 'F'),
    ('B', 'D'), ('B', 'C'),
    ('C', 'D'), ('C', 'G'),
    ('D', 'E'),
    ('E', 'F'), ('E', 'G'),
    ('F', 'G')
]
G.add_edges_from(edges)
pos = {
    'A': (1, 3),   'B': (2, 3),
    'F': (0.5, 2), 'G': (1.5, 2), 'C': (2.5, 2),
    'E': (1, 1),   'D': (2, 1)
}

coloring_indices = nx.coloring.greedy_color(G, strategy='DSATUR')
chromatic_num = max(coloring_indices.values()) + 1
color_seq = ['Red', 'Green', 'Blue', 'Yellow']
final_coloring = {node: color_seq[index] for node, index in coloring_indices.items()}

print(f"{'Node':<10} | {'Assigned Color'}")
print("-" * 25)
for node in sorted(final_coloring.keys()):
    print(f"{node:<10} | {final_coloring[node]}")
print("-" * 25)
print(f"Chromatic Number (X(G)): {chromatic_num}")

plt.figure(figsize=(15, 7))
plt.subplot(1, 2, 1)
nx.draw(G, pos, with_labels=True, node_color='lightgray',
        node_size=1500, font_size=12, font_weight='bold', edge_color='black')
plt.title("Original Uncolored Graph", fontsize=14, fontweight='bold')
plt.subplot(1, 2, 2)
node_colors = [final_coloring[node] for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=node_colors,
        node_size=1500, font_size=12, font_weight='bold', edge_color='black')
plt.title(f"Colored Graph (X(G) = {chromatic_num})", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
'''

CODE_EXP11_MANUAL = '''\
import networkx as nx
import matplotlib.pyplot as plt

def dsatur_coloring(G, color_sequence, start_node):
    coloring = {node: None for node in G.nodes()}
    coloring[start_node] = color_sequence[0]
    nodes_to_color = set(G.nodes())
    nodes_to_color.remove(start_node)
    while nodes_to_color:
        saturation_data = []
        for node in nodes_to_color:
            neighbor_colors = {coloring[n] for n in G.neighbors(node) if coloring[n] is not None}
            sat_degree = len(neighbor_colors)
            saturation_data.append((node, sat_degree))
        saturation_data.sort(key=lambda x: (-x[1], x[0]))
        best_node = saturation_data[0][0]
        forbidden_colors = {coloring[n] for n in G.neighbors(best_node) if coloring[n] is not None}
        for color in color_sequence:
            if color not in forbidden_colors:
                coloring[best_node] = color
                break
        nodes_to_color.remove(best_node)
    return coloring

G = nx.Graph()
edges = [
    ('A', 'B'), ('A', 'G'), ('A', 'E'), ('A', 'F'),
    ('B', 'D'), ('B', 'C'),
    ('C', 'D'), ('C', 'G'),
    ('D', 'E'),
    ('E', 'F'), ('E', 'G'),
    ('F', 'G')
]
G.add_edges_from(edges)
pos = {
    'A': (1, 3),   'B': (2, 3),
    'F': (0.5, 2), 'G': (1.5, 2), 'C': (2.5, 2),
    'E': (1, 1),   'D': (2, 1)
}
color_seq = ['Red', 'Green', 'Blue', 'Yellow']
final_coloring = dsatur_coloring(G, color_seq, 'A')
unique_colors_used = set(final_coloring.values())
chromatic_num = len(unique_colors_used)

print(f"{'Node':<10} | {'Assigned Color'}")
print("-" * 25)
for node in sorted(final_coloring.keys()):
    print(f"{node:<10} | {final_coloring[node]}")
print("-" * 25)
print(f"Chromatic Number (X(G)): {chromatic_num}")

plt.figure(figsize=(15, 7))
plt.subplot(1, 2, 1)
nx.draw(G, pos, with_labels=True, node_color='lightgray',
        node_size=1500, font_size=12, font_weight='bold', edge_color='black')
plt.title("Original Graph", fontsize=14, fontweight='bold')
plt.subplot(1, 2, 2)
node_colors = [final_coloring[node] for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=node_colors,
        node_size=1500, font_size=12, font_weight='bold', edge_color='black')
plt.title(f"Colored Graph (X(G) = {chromatic_num})", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
'''

CODE_EXP11_SUDOKU = '''\
import networkx as nx
import matplotlib.pyplot as plt
import copy

sudoku = [
    [0, 4, 0, 0],
    [0, 0, 0, 4],
    [0, 0, 0, 0],
    [0, 2, 0, 0]
]
initial_sudoku = copy.deepcopy(sudoku)
SIZE = 4
SUBGRID = 2
G = nx.sudoku_graph(2)
steps = []

def is_safe(board, row, col, num):
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row = (row // SUBGRID) * SUBGRID
    start_col = (col // SUBGRID) * SUBGRID
    for r in range(start_row, start_row + SUBGRID):
        for c in range(start_col, start_col + SUBGRID):
            if board[r][c] == num:
                return False
    return True

def solve(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == 0:
                for num in range(1, SIZE + 1):
                    if is_safe(board, row, col, num):
                        steps.append(f"Pick cell ({row+1},{col+1}) -> Assign {num}")
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                        steps.append(f"Backtrack cell ({row+1},{col+1})")
                return False
    return True

# PROCESS SOLUTION
print("\\nInitial Sudoku:\\n")
for row in sudoku:
    print(row)
solve(sudoku)
print("\\nSolved Sudoku:\\n")
for row in sudoku:
    print(row)

colors = ["red", "green", "skyblue", "yellow"]
pos = {}
initial_colors = []
initial_labels = {}
final_colors = []
final_labels = {}
for i in range(SIZE):
    for j in range(SIZE):
        node = i * SIZE + j
        pos[node] = (j, -i)
        val_init = initial_sudoku[i][j]
        initial_labels[node] = val_init if val_init != 0 else ""
        if val_init == 0:
            initial_colors.append("lightgray")
        else:
            initial_colors.append(colors[val_init - 1])
        val_final = sudoku[i][j]
        final_labels[node] = val_final
        if val_final == 0:
            final_colors.append("lightgray")
        else:
            final_colors.append(colors[val_final - 1])

def draw_curved_edges(G, pos, ax, edge_color=\'black\', alpha=1, linewidth=1.2):

    rad_options = [0.08, -0.08, 0.16, -0.16, 0.24, -0.24, 0.32, -0.32]
    for i, (u, v) in enumerate(G.edges()):
        rad = rad_options[i % len(rad_options)]
        ax.annotate(
            "",
            xy=pos[v], xycoords=\'data\',
            xytext=pos[u], textcoords=\'data\',
            arrowprops=dict(
                arrowstyle="-",
                color=edge_color,
                alpha=alpha,
                linewidth=linewidth,
                connectionstyle=f"arc3,rad={rad}",
                shrinkA=18, shrinkB=18,
            ),
        )

fig = plt.figure(figsize=(16, 8))
# Original Graph
ax1 = plt.subplot(1, 2, 1)
draw_curved_edges(G, pos, ax1)
nx.draw_networkx_nodes(G, pos, node_color=initial_colors, node_size=1800, edgecolors=\'black\', linewidths=2, ax=ax1)
nx.draw_networkx_labels(G, pos, labels=initial_labels, font_size=16, font_weight=\'bold\', ax=ax1)
plt.title("Original Graph", fontsize=14, fontweight=\'bold\')
plt.axis(\'off\')
# Colored Graph
ax2 = plt.subplot(1, 2, 2)
draw_curved_edges(G, pos, ax2)
nx.draw_networkx_nodes(G, pos, node_color=final_colors, node_size=1800, edgecolors=\'black\', linewidths=2, ax=ax2)
nx.draw_networkx_labels(G, pos, labels=final_labels, font_size=16, font_weight=\'bold\', ax=ax2)
plt.title("Solved Sudoku Graph", fontsize=14, fontweight=\'bold\')
plt.axis(\'off\')
plt.tight_layout()
plt.show()
'''

CODE_EXP4_MANUAL = '''\
import networkx as nx
import matplotlib.pyplot as plt
import math

degree_sequence = [6, 5, 5, 4, 3, 3, 2, 2, 1, 1]
G = nx.Graph()
n = len(degree_sequence)
for i in range(n):
    G.add_node(i)

pos = nx.circular_layout(G)
degree_list = [[i, degree_sequence[i]] for i in range(n)]
steps = []

while True:
    degree_list.sort(key=lambda x: x[1], reverse=True)
    if degree_list[0][1] == 0:
        steps.append((G.copy(), f"Final Graph\\nRemaining: {degree_list}"))
        break
    node, deg = degree_list[0]
    degree_list = degree_list[1:]
    if deg > len(degree_list):
        print("Sequence is NOT graphical")
        break
    for i in range(deg):
        neighbor_node = degree_list[i][0]
        G.add_edge(node, neighbor_node)
        degree_list[i][1] -= 1
    steps.append((G.copy(), f"Connected Node {node}\\nRemaining: {list(degree_list)}"))

num_steps = len(steps)
cols = 3
rows = math.ceil(num_steps / cols)
fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 4 * rows))
axes = axes.flatten()

for idx, (graph_snapshot, title) in enumerate(steps):
    ax = axes[idx]
    nx.draw(graph_snapshot, pos, ax=ax, with_labels=True,
            node_color="plum", node_size=600, font_size=10)
    ax.set_title(title, fontsize=10, fontweight=\'bold\')

for idx in range(num_steps, len(axes)):
    fig.delaxes(axes[idx])

plt.tight_layout()
plt.show()
'''


CODE_EXP9_INBUILT = '''\
import networkx as nx
import matplotlib.pyplot as plt

G1 = nx.Graph()
G1.add_edges_from([('A','B'), ('A','E'), ('B','E'), ('B','C'), ('B','D'), ('C','D')])
pos1 = {'A': (0, 2), 'C': (2, 2), 'B': (1, 1), 'E': (0, 0), 'D': (2, 0)}

def show_inbuilt_results(G, pos, title):
    plt.figure(figsize=(10, 5))

    ax1 = plt.subplot(1, 2, 1)
    ax1.set_title(f"{title}: Original")
    nx.draw(G, pos, ax=ax1, with_labels=True, node_color='lightgreen',
            node_size=1000, font_weight='bold', arrows=False)

    ax2 = plt.subplot(1, 2, 2)
    if nx.is_eulerian(G):
        circuit_edges = list(nx.eulerian_circuit(G))
        path_nodes = [u for u, v in circuit_edges] + [circuit_edges[-1][1]]
        path_str = " -> ".join(path_nodes)
        print(f"{title} Eulerian Circuit found: {path_str}")
        ax2.set_title(f"{title} (Eulerian Trail: {path_str})")
        NullG = G.copy()
        NullG.clear_edges()
        nx.draw(NullG, pos, ax=ax2, with_labels=True, node_color='plum',
                node_size=1000, font_weight='bold', arrows=False)
    else:
        ax2.set_title(f"{title}: No Eulerian Circuit exists")
        print(f"{title}: No Eulerian Circuit exists.")

show_inbuilt_results(G1, pos1, "Graph G")
plt.tight_layout()
plt.show()
'''

#   Helpers   ─
def capture_prints(func, *args, **kwargs):
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    result = func(*args, **kwargs)
    sys.stdout = old
    return result, buf.getvalue()

def show_fig():
    st.pyplot(plt.gcf())
    plt.close("all")

#   EXP 1   ───
def exp1_inbuilt():
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    fig.suptitle("Types of Graphs", fontsize=20, fontweight="bold", color="purple")
    G1 = nx.Graph(); G1.add_nodes_from([1,2,3,4,5])
    G1 = nx.relabel_nodes(G1,{1:"I",2:"II",3:"III",4:"IV",5:"V"})
    nx.draw(G1,nx.circular_layout(G1),with_labels=True,ax=axes[0,0],node_color="cyan",edge_color="brown",node_size=1100)
    axes[0,0].set_title("(N5) Null Graph",color="brown")
    G2=nx.complete_graph(6)
    nx.draw(G2,nx.circular_layout(G2),with_labels=True,ax=axes[0,1],node_color="yellow",edge_color="blue",node_size=1100)
    axes[0,1].set_title("(K6) Complete Graph",color="blue")
    G3=nx.path_graph(5); G3=nx.relabel_nodes(G3,{0:"A",1:"B",2:"C",3:"D",4:"E"})
    nx.draw(G3,nx.spring_layout(G3),with_labels=True,ax=axes[0,2],node_color="orange",edge_color="brown",node_size=1100)
    axes[0,2].set_title("(P5) Path Graph",color="brown")
    G4=nx.complete_bipartite_graph(3,4)
    pos4={i:(i,1) for i in [0,1,2]}; pos4.update({i:(i-3,0) for i in [3,4,5,6]})
    nx.draw(G4,pos4,with_labels=True,ax=axes[1,0],node_color="lightgreen",edge_color="brown",node_size=1100)
    axes[1,0].set_title("(K3,4) Bipartite Graph",color="brown")
    G5=nx.cycle_graph(8)
    nx.draw(G5,nx.circular_layout(G5),with_labels=True,ax=axes[1,1],node_color="lightpink",edge_color="blue",node_size=1100)
    axes[1,1].set_title("(C8) Cycle Graph",color="blue")
    G6=nx.wheel_graph(6)
    nx.draw(G6,nx.shell_layout(G6,nlist=[[0],[1,2,3,4,5]]),with_labels=True,ax=axes[1,2],node_color="violet",edge_color="brown",node_size=1100)
    axes[1,2].set_title("(W6) Wheel Graph",color="brown")
    plt.tight_layout(); return ""

def exp1_manual():
    fig,axes=plt.subplots(2,3,figsize=(14,8))
    fig.suptitle("Types of Graphs",fontsize=20,fontweight="bold",color="purple")
    G1=nx.Graph(); G1.add_nodes_from(["I","II","III","IV","V"])
    nx.draw(G1,nx.circular_layout(G1),ax=axes[0,0],with_labels=True,node_color="cyan",node_size=900)
    axes[0,0].set_title("(N5) Null Graph",color="brown")
    G2=nx.Graph(); nodes2=range(1,7)
    for i in nodes2:
        for j in nodes2:
            if i<j: G2.add_edge(i,j)
    nx.draw(G2,nx.circular_layout(G2),ax=axes[0,1],with_labels=True,node_color="yellow",edge_color="blue",node_size=900)
    axes[0,1].set_title("(K6) Complete Graph",color="blue")
    G3=nx.Graph(); nodes3=["A","B","C","D","E"]
    for i in range(len(nodes3)-1): G3.add_edge(nodes3[i],nodes3[i+1])
    nx.draw(G3,ax=axes[0,2],with_labels=True,node_color="orange",edge_color="brown",node_size=900)
    axes[0,2].set_title("(P5) Path Graph",color="brown")
    G4=nx.Graph(); X,Y=[1,2,3],[4,5,6,7]
    for x in X:
        for y in Y: G4.add_edge(x,y)
    pos4={i:(i-1,1) for i in X}; pos4.update({i:(i-4,0) for i in Y})
    nx.draw(G4,pos4,ax=axes[1,0],with_labels=True,node_color="lightgreen",edge_color="brown",node_size=900)
    axes[1,0].set_title("(K3,4) Bipartite Graph",color="brown")
    G5=nx.Graph()
    for i in range(8): G5.add_edge(i,(i+1)%8)
    nx.draw(G5,nx.circular_layout(G5),ax=axes[1,1],with_labels=True,node_color="lightpink",edge_color="blue",node_size=900)
    axes[1,1].set_title("(C8) Cycle Graph",color="blue")
    G6=nx.Graph(); hub,rim=0,[1,2,3,4,5]
    for i in range(len(rim)): G6.add_edge(rim[i],rim[(i+1)%len(rim)])
    for node in rim: G6.add_edge(hub,node)
    nx.draw(G6,nx.shell_layout(G6,nlist=[[hub],rim]),ax=axes[1,2],with_labels=True,node_color="violet",edge_color="brown",node_size=900)
    axes[1,2].set_title("(W6) Wheel Graph",color="brown")
    plt.tight_layout(); return ""

#   EXP 2   ───
def exp2_inbuilt():
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    G1=nx.Graph(); G1.add_nodes_from(range(1,7))
    G1.add_edges_from([(1,2),(2,3),(3,4),(4,5),(5,6),(6,1),(1,4),(2,5),(3,6)])
    nx.draw(G1,nx.circular_layout(G1),with_labels=True,ax=axes[0],node_color="lightgreen",node_size=1500)
    axes[0].set_title("Graph G1")
    G2=nx.Graph()
    G2.add_nodes_from(["a","b","c"],bipartite=0); G2.add_nodes_from(["d","e","f"],bipartite=1)
    G2.add_edges_from([("a","d"),("a","e"),("a","f"),("b","d"),("b","e"),("b","f"),("c","d"),("c","e"),("c","f")])
    pos2=nx.bipartite_layout(G2,["a","b","c"],align="horizontal")
    nx.draw(G2,pos2,with_labels=True,ax=axes[1],node_color="lightpink",node_size=1500)
    axes[1].set_title("Graph G2"); plt.tight_layout()
    GM=nx.isomorphism.GraphMatcher(G1,G2)
    if GM.is_isomorphic(): return f"Graphs are ISOMORPHIC\nMapping (G1 → G2): {GM.mapping}"
    return "Graphs are NOT isomorphic"

def exp2_manual():
    nodes1=[1,2,3,4,5,6]; edges1=[(1,2),(2,3),(3,4),(4,5),(5,6),(6,1),(1,4),(2,5),(3,6)]
    nodes2=["a","b","c","d","e","f"]
    edges2=[("a","d"),("a","e"),("a","f"),("b","d"),("b","e"),("b","f"),("c","d"),("c","e"),("c","f")]
    G1_nx=nx.Graph(); G1_nx.add_edges_from(edges1)
    G2_nx=nx.Graph(); G2_nx.add_edges_from(edges2)
    v1,v2=len(nodes1),len(nodes2); e1,e2=len(edges1),len(edges2)
    def deg_seq(nodes,edges):
        return sorted([sum(1 for e in edges if n in e) for n in nodes])
    deg1=deg_seq(nodes1,edges1); deg2=deg_seq(nodes2,edges2)
    num_cycles1=e1-v1+1; num_cycles2=e2-v2+1
    mapping={1:"a",3:"b",5:"c",2:"d",4:"e",6:"f"}
    def verify(e1,e2,m):
        for u,v in e1:
            if (m[u],m[v]) not in e2 and (m[v],m[u]) not in e2: return False
        return True
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    pos1={1:(0,1),2:(1,0.5),3:(1,-0.5),4:(0,-1),5:(-1,-0.5),6:(-1,0.5)}
    nx.draw(G1_nx,pos1,ax=axes[0],with_labels=True,node_color="lightgreen",node_size=1200)
    axes[0].set_title("Graph G1")
    pos2={"a":(-1,-1),"b":(0,-1),"c":(1,-1),"d":(-1,1),"e":(0,1),"f":(1,1)}
    nx.draw(G2_nx,pos2,ax=axes[1],with_labels=True,node_color="lightpink",node_size=1200)
    axes[1].set_title("Graph G2"); plt.tight_layout()
    out=(f"Vertices: G1={v1}, G2={v2}\nEdges: G1={e1}, G2={e2}\n"
         f"Degree seq G1: {deg1}\nDegree seq G2: {deg2}\n"
         f"Cycles: G1={num_cycles1}, G2={num_cycles2}\nMapping: {mapping}\n")
    if v1==v2 and e1==e2 and deg1==deg2 and num_cycles1==num_cycles2 and verify(edges1,edges2,mapping):
        out+="RESULT: Graphs are ISOMORPHIC"
    else:
        out+="RESULT: Graphs are NOT isomorphic"
    return out

#   EXP 3   ───
def exp3_inbuilt():
    nodes=list(range(1,8))
    edges=[(1,5),(1,4),(2,6),(2,5),(3,7),(3,6),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,1),(4,7)]
    G=nx.Graph(); G.add_nodes_from(nodes); G.add_edges_from(edges)
    pos=nx.circular_layout(G); fig,axs=plt.subplots(2,2,figsize=(12,10))
    nx.draw(G,pos,with_labels=True,node_color="cyan",ax=axs[0,0]); axs[0,0].set_title("Original Graph")
    span=G.edge_subgraph([(1,2),(2,3),(3,4),(4,5),(5,6),(6,7)])
    nx.draw(span,pos,with_labels=True,node_color="lightgreen",ax=axs[0,1]); axs[0,1].set_title("Spanning Subgraph")
    ind=G.subgraph([3,4,5,6])
    nx.draw(ind,pos,with_labels=True,node_color="lightpink",ax=axs[1,0]); axs[1,0].set_title("Vertex-Induced Subgraph")
    ei=G.edge_subgraph([(1,5),(2,6),(3,7),(4,1)])
    nx.draw(ei,pos,with_labels=True,node_color="yellow",ax=axs[1,1]); axs[1,1].set_title("Edge-Induced Subgraph")
    plt.tight_layout(); return ""

def exp3_manual():
    nodes=list(range(1,8))
    edges=[(1,5),(1,4),(2,6),(2,5),(3,7),(3,6),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,1),(4,7)]
    G_orig=nx.Graph(); [G_orig.add_node(n) for n in nodes]; [G_orig.add_edge(u,v) for u,v in edges]
    pos=nx.circular_layout(G_orig); fig,axs=plt.subplots(2,2,figsize=(12,10))
    nx.draw(G_orig,pos,with_labels=True,node_color="cyan",node_size=800,ax=axs[0,0]); axs[0,0].set_title("Original Graph")
    G_span=nx.Graph(); [G_span.add_node(n) for n in nodes]
    for u,v in [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7)]: G_span.add_edge(u,v)
    nx.draw(G_span,pos,with_labels=True,node_color="lightgreen",node_size=800,ax=axs[0,1]); axs[0,1].set_title("Spanning Subgraph")
    G_ind=nx.Graph(); V_sel=[3,4,5,6]; [G_ind.add_node(n) for n in V_sel]
    for u,v in edges:
        if u in V_sel and v in V_sel: G_ind.add_edge(u,v)
    nx.draw(G_ind,pos,with_labels=True,node_color="lightpink",node_size=800,ax=axs[1,0]); axs[1,0].set_title("Vertex-Induced Subgraph")
    G_ei=nx.Graph()
    for u,v in [(1,5),(2,6),(3,7),(4,1)]: G_ei.add_edge(u,v)
    nx.draw(G_ei,pos,with_labels=True,node_color="yellow",node_size=800,ax=axs[1,1]); axs[1,1].set_title("Edge-Induced Subgraph")
    plt.tight_layout(); return ""

#   EXP 4   ───
def exp4_inbuilt():
    ds=[6,5,5,4,3,3,2,2,1,1]
    G=nx.havel_hakimi_graph(ds)
    plt.figure(figsize=(10,8))
    nx.draw(G,nx.circular_layout(G),with_labels=True,node_color="plum",node_size=900)
    plt.title("Havel-Hakimi Graph"); return f"Degree sequence: {ds}"

def exp4_manual():
    """Updated Havel-Hakimi manual — step-by-step subplot version."""
    degree_sequence=[6,5,5,4,3,3,2,2,1,1]
    G=nx.Graph(); n=len(degree_sequence)
    for i in range(n): G.add_node(i)
    pos=nx.circular_layout(G)
    degree_list=[[i,degree_sequence[i]] for i in range(n)]
    steps=[]
    while True:
        degree_list.sort(key=lambda x:x[1],reverse=True)
        if degree_list[0][1]==0:
            steps.append((G.copy(),f"Final Graph\nRemaining: {degree_list}")); break
        node,deg=degree_list[0]; degree_list=degree_list[1:]
        if deg>len(degree_list):
            return "Sequence is NOT graphical"
        for i in range(deg):
            neighbor_node=degree_list[i][0]
            G.add_edge(node,neighbor_node); degree_list[i][1]-=1
        steps.append((G.copy(),f"Connected Node {node}\nRemaining: {list(degree_list)}"))
    num_steps=len(steps); cols=3; rows=math.ceil(num_steps/cols)
    fig,axes=plt.subplots(rows,cols,figsize=(5*cols,4*rows)); axes=axes.flatten()
    for idx,(graph_snapshot,title) in enumerate(steps):
        ax=axes[idx]
        nx.draw(graph_snapshot,pos,ax=ax,with_labels=True,node_color="plum",node_size=600,font_size=10)
        ax.set_title(title,fontsize=10,fontweight="bold")
    for idx in range(num_steps,len(axes)): fig.delaxes(axes[idx])
    plt.tight_layout()
    return f"Graph constructed for degree sequence: {degree_sequence}"

#   EXP 5   ───
def exp5_inbuilt():
    edges_data=[(1,2,"e1",10),(1,3,"e2",20),(1,5,"e3",30),(2,4,"e4",40),(2,8,"e5",50),
                (3,5,"e6",60),(3,4,"e7",70),(3,6,"e8",80),(4,6,"e9",90),(4,7,"e10",10),
                (4,8,"e11",20),(5,6,"e12",30),(6,7,"e13",40),(7,8,"e14",50)]
    G=nx.Graph()
    for u,v,label,weight in edges_data: G.add_edge(u,v,label=label,weight=weight)
    pos_G={1:(-0.7,2.8),2:(0.3,2.8),3:(-0.3,1),4:(0.3,1),5:(-0.9,-0.6),6:(-0.3,-0.6),7:(0.3,-0.6),8:(1,1)}
    L_full=nx.line_graph(G); steps=[]; current_L=nx.Graph()
    for i in range(len(edges_data)):
        u1,v1,label1,w1=edges_data[i]; node1=(u1,v1)
        current_L.add_node(node1,label=label1); new_edges=[]
        for en in list(current_L.nodes()):
            if en==node1: continue
            if L_full.has_edge(node1,en):
                u2,v2=en; w2=G[u2][v2]["weight"]
                current_L.add_edge(node1,en,weight=w1+w2); new_edges.append((node1,en))
        steps.append((current_L.copy(),new_edges))
    def circ(nodes,r=2):
        pos={}; nl=list(nodes); n=len(nl)
        for i,nd in enumerate(nl):
            a=2*math.pi*i/n if n>0 else 0; pos[nd]=(r*math.cos(a),r*math.sin(a))
        return pos
    cols=5; rows=math.ceil((len(steps)+1)/cols)
    plt.figure(figsize=(22,rows*4.5))
    plt.subplot(rows,cols,1)
    nx.draw(G,pos_G,with_labels=True,node_size=500,node_color="violet")
    el={(u,v):f"w={d['weight']}" for u,v,d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G,pos_G,edge_labels=el,font_size=8)
    plt.title("Original Graph",fontsize=10)
    for i,(tL,newest) in enumerate(steps):
        plt.subplot(rows,cols,i+2)
        pL=circ(tL.nodes())
        labels={n:G.edges[n]["label"] for n in tL.nodes()}
        nx.draw(tL,pL,labels=labels,with_labels=True,node_size=400,node_color="cyan",font_size=8)
        nx.draw_networkx_edges(tL,pL,edgelist=newest,edge_color="red",width=2)
        lw={(u,v):d["weight"] for u,v,d in tL.edges(data=True)}
        nx.draw_networkx_edge_labels(tL,pL,edge_labels=lw,font_size=6)
        plt.title(f"Step {i+1}",fontsize=9)
    plt.tight_layout(); return ""

def exp5_manual():
    edges_data=[(1,2,"e1",10),(1,3,"e2",20),(1,5,"e3",30),(2,4,"e4",40),(2,8,"e5",50),
                (3,5,"e6",60),(3,4,"e7",70),(3,6,"e8",80),(4,6,"e9",90),(4,7,"e10",10),
                (4,8,"e11",20),(5,6,"e12",30),(6,7,"e13",40),(7,8,"e14",50)]
    G=nx.Graph()
    for u,v,label,weight in edges_data: G.add_edge(u,v,label=label,weight=weight)
    pos_G={1:(-0.7,2.8),2:(0.3,2.8),3:(-0.3,1),4:(0.3,1),5:(-0.9,-0.6),6:(-0.3,-0.6),7:(0.3,-0.6),8:(1,1)}
    L_nodes=[]; L_edges=[]; steps=[]
    for i in range(len(edges_data)):
        u1,v1,label1,w1=edges_data[i]; L_nodes.append(label1); new_conn=[]
        for j in range(i):
            u2,v2,label2,w2=edges_data[j]
            if u1==u2 or u1==v2 or v1==u2 or v1==v2:
                cw=w1+w2; L_edges.append((label1,label2,cw)); new_conn.append((label1,label2,cw))
        steps.append((list(L_nodes),list(L_edges),new_conn))
    def circ(nodes,r=2):
        pos={}; n=len(nodes)
        for i,nd in enumerate(nodes):
            a=2*math.pi*i/n if n>0 else 0; pos[nd]=(r*math.cos(a),r*math.sin(a))
        return pos
    cols=5; rows=math.ceil((len(steps)+1)/cols)
    plt.figure(figsize=(10,rows*4))
    plt.subplot(rows,cols,1)
    nx.draw(G,pos_G,with_labels=True,node_size=500,node_color="violet",font_weight="bold")
    el={(u,v):f"{d['label']}\n(w={d['weight']})" for u,v,d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G,pos_G,edge_labels=el,font_size=7)
    plt.title("Original Graph (G)",fontsize=12)
    for i,(nodes,all_edges,newest_edges) in enumerate(steps):
        plt.subplot(rows,cols,i+2)
        tL=nx.Graph(); tL.add_nodes_from(nodes)
        for u,v,w in all_edges: tL.add_edge(u,v,weight=w)
        pL=circ(nodes)
        nx.draw(tL,pL,with_labels=True,node_size=300,node_color="cyan",edge_color="gray",alpha=0.6,font_size=8)
        nx.draw_networkx_edges(tL,pL,edgelist=[(u,v) for u,v,w in newest_edges],edge_color="red",width=1.5)
        if tL.edges():
            lw={(u,v):f"{d['weight']}" for u,v,d in tL.edges(data=True)}
            nx.draw_networkx_edge_labels(tL,pL,edge_labels=lw,font_size=6)
        plt.title(f"Step {i+1}: Added {nodes[-1]}",fontsize=10)
    plt.subplots_adjust(hspace=0.4,wspace=0.3); return ""

#   EXP 6   ───
MATRIX=[
    [None,14,5,2,None,None,None,None,None],
    [14,None,9,8,15,None,None,None,None],
    [5,9,None,None,13,8,None,None,None],
    [2,8,None,None,10,None,None,11,None],
    [None,15,13,10,None,1,7,5,None],
    [None,None,8,None,1,None,10,None,11],
    [None,None,None,None,7,10,None,0,12],
    [None,None,None,11,5,None,0,None,6],
    [None,None,None,None,None,11,12,6,None]
]
NODES6=["1","2","3","4","5","6","7","8","9"]
LAYOUT6={"1":(0,0),"2":(1,0),"5":(2,0),"7":(3,0),"9":(4,0),"3":(1,1),"6":(3,1),"4":(1,-1),"8":(3,-1)}

def exp6_inbuilt():
    G_full=nx.Graph()
    for i in range(9):
        for j in range(i+1,9):
            if MATRIX[i][j] is not None: G_full.add_edge(NODES6[i],NODES6[j],weight=MATRIX[i][j])
    gen=nx.minimum_spanning_edges(G_full,algorithm="kruskal",data=True)
    mst_steps=[]; curr=[]; cost=0; costs=[]
    for u,v,d in gen:
        curr.append((u,v,d["weight"])); cost+=d["weight"]
        mst_steps.append(list(curr)); costs.append(cost)
    total=1+len(mst_steps); cols=3; rows=math.ceil(total/cols)
    fig,axes=plt.subplots(rows,cols,figsize=(18,5*rows)); axes=axes.flatten()
    nx.draw(G_full,LAYOUT6,ax=axes[0],with_labels=True,node_color="orange",node_size=800,font_weight="bold")
    nx.draw_networkx_edge_labels(G_full,LAYOUT6,edge_labels=nx.get_edge_attributes(G_full,"weight"),ax=axes[0],font_size=8)
    axes[0].set_title("Original Graph",fontweight="bold")
    for i,step in enumerate(mst_steps):
        ax=axes[i+1]; Gs=nx.Graph(); Gs.add_nodes_from(NODES6); Gs.add_weighted_edges_from(step)
        nx.draw(Gs,LAYOUT6,ax=ax,with_labels=True,node_color="cyan",node_size=800,font_weight="bold")
        nx.draw_networkx_edge_labels(Gs,LAYOUT6,edge_labels=nx.get_edge_attributes(Gs,"weight"),ax=ax,font_size=8)
        u_l,v_l,w_l=step[-1]; ax.set_title(f"Step {i+1}: Added {u_l}-{v_l}\nCost: {costs[i]}",fontsize=10)
    for j in range(total,len(axes)): axes[j].axis("off")
    plt.tight_layout(); return f"Final MST Weight: {cost}"

def exp6_manual():
    edges=[]
    for i in range(9):
        for j in range(i+1,9):
            if MATRIX[i][j] is not None: edges.append((MATRIX[i][j],NODES6[i],NODES6[j]))
    edges.sort(); comps=[{n} for n in NODES6]; mst_steps=[]; curr=[]; cost=0; costs=[]
    for w,u,v in edges:
        cu=next(c for c in comps if u in c); cv=next(c for c in comps if v in c)
        if cu!=cv:
            curr.append((u,v,w)); cost+=w; comps.remove(cu); comps.remove(cv); comps.append(cu|cv)
            mst_steps.append(list(curr)); costs.append(cost)
    total=1+len(mst_steps); cols=3; rows=math.ceil(total/cols)
    fig,axes=plt.subplots(rows,cols,figsize=(18,5*rows)); axes=axes.flatten()
    G_full=nx.Graph()
    for w,u,v in edges: G_full.add_edge(u,v,weight=w)
    nx.draw(G_full,LAYOUT6,ax=axes[0],with_labels=True,node_color="orange",node_size=800,font_weight="bold")
    nx.draw_networkx_edge_labels(G_full,LAYOUT6,edge_labels=nx.get_edge_attributes(G_full,"weight"),ax=axes[0],font_size=8)
    axes[0].set_title("Original Graph",fontweight="bold")
    for i,step in enumerate(mst_steps):
        ax=axes[i+1]; Gs=nx.Graph(); Gs.add_nodes_from(NODES6); Gs.add_weighted_edges_from(step)
        nx.draw(Gs,LAYOUT6,ax=ax,with_labels=True,node_color="cyan",node_size=800,font_weight="bold")
        nx.draw_networkx_edge_labels(Gs,LAYOUT6,edge_labels=nx.get_edge_attributes(Gs,"weight"),ax=ax,font_size=8)
        le=step[-1]; ax.set_title(f"Step {i+1}: Added {le[0]}-{le[1]}\nCost: {costs[i]}",fontsize=10)
    for j in range(total,len(axes)): axes[j].axis("off")
    plt.tight_layout(); return f"Final MST Weight: {cost}"

#   EXP 7   ───
EDGES7=[(1,2,15),(1,3,14),(1,5,3),(2,4,2),(2,8,17),(3,5,9),(3,4,6),(3,6,8),
        (4,6,9),(4,7,3),(4,8,9),(5,6,15),(6,7,8),(7,8,2)]
POS7={1:(-0.7,2.8),2:(0.3,2.8),3:(-0.3,1),4:(0.3,1),5:(-0.9,-0.6),6:(-0.3,-0.6),7:(0.3,-0.6),8:(1,1)}

def exp7_inbuilt():
    G=nx.Graph()
    for u,v,w in EDGES7: G.add_edge(u,v,weight=w)
    src=1; fd,fp=nx.single_source_dijkstra(G,src)
    tree=[]
    for node,path in fp.items():
        for i in range(len(path)-1):
            u,v=path[i],path[i+1]
            if (u,v) not in tree and (v,u) not in tree: tree.append((u,v))
    non_tree=[e for e in G.edges() if (e[0],e[1]) not in tree and (e[1],e[0]) not in tree]
    el=nx.get_edge_attributes(G,"weight")
    fig,axes=plt.subplots(1,2,figsize=(16,7.5))
    ax1=axes[0]; ax1.set_axis_off()
    nx.draw_networkx_edges(G,POS7,ax=ax1,edge_color="black",width=1.5)
    nx.draw_networkx_nodes(G,POS7,ax=ax1,node_color="lightgray",node_size=900,edgecolors="black")
    nx.draw_networkx_labels(G,POS7,ax=ax1,font_size=11,font_weight="bold")
    nx.draw_networkx_edge_labels(G,POS7,edge_labels=el,ax=ax1,font_size=10)
    ax1.set_title("Original Graph",fontsize=14,fontweight="bold")
    ax2=axes[1]; ax2.set_axis_off()
    nx.draw_networkx_edges(G,POS7,ax=ax2,edgelist=non_tree,edge_color="gainsboro",width=1.2,style="dashed")
    nx.draw_networkx_edges(G,POS7,ax=ax2,edgelist=tree,edge_color="red",width=3.5)
    nx.draw_networkx_nodes(G,POS7,ax=ax2,node_color="violet",node_size=1000,edgecolors="black")
    rl={n:f"{n}\n(d={fd[n]})" for n in G.nodes()}
    nx.draw_networkx_labels(G,POS7,rl,ax=ax2,font_size=9,font_weight="bold")
    nx.draw_networkx_edge_labels(G,POS7,edge_labels=el,ax=ax2,font_size=10)
    ax2.set_title(f"Shortest Path from Node {src}",fontsize=14,fontweight="bold")
    plt.tight_layout()
    lines=["Shortest Paths from Source Node 1:","─"*50]
    for node in sorted(fd):
        lines.append(f"Node {node:2} | Cost={fd[node]:2} | Path: {' → '.join(map(str,fp[node]))}")
    return "\n".join(lines)

def exp7_manual():
    G=nx.Graph()
    for u,v,w in EDGES7: G.add_edge(u,v,weight=w)
    src=1; dist={n:float("inf") for n in G.nodes()}; pred={n:None for n in G.nodes()}
    dist[src]=0; visited=set(); steps=[]; all_nodes=sorted(G.nodes())
    while len(visited)<len(G.nodes()):
        unvis={n:dist[n] for n in G.nodes() if n not in visited}
        if not unvis: break
        u=min(unvis,key=unvis.get); red=[]
        for v in G.neighbors(u):
            if v not in visited:
                w=G[u][v]["weight"]; red.append((u,v))
                if dist[u]+w<dist[v]: dist[v]=dist[u]+w; pred[v]=u
        visited.add(u); steps.append({"cur":u,"dist":dict(dist),"vis":set(visited),"red":red})
    cols=3; rows=math.ceil(len(steps)/cols)
    fig,axes=plt.subplots(rows,cols,figsize=(15,rows*5)); axes=axes.flatten()
    for i,step in enumerate(steps):
        ax=axes[i]; ax.set_axis_off()
        nx.draw_networkx_edges(G,POS7,ax=ax,edge_color="black",alpha=1.0,width=1)
        nx.draw_networkx_edges(G,POS7,ax=ax,edgelist=step["red"],edge_color="red",width=3)
        nx.draw_networkx_nodes(G,POS7,ax=ax,node_color="lightgray",node_size=500)
        nx.draw_networkx_nodes(G,POS7,ax=ax,nodelist=list(step["vis"]),node_color="violet",node_size=600)
        nx.draw_networkx_nodes(G,POS7,ax=ax,nodelist=[step["cur"]],node_color="orange",node_size=700)
        lbl={n:f"{n}\n(d={step['dist'][n] if step['dist'][n]!=float('inf') else '∞'})" for n in G.nodes()}
        nx.draw_networkx_labels(G,POS7,lbl,ax=ax,font_size=8,font_weight="bold")
        ax.set_title(f"Step {i+1}: Node {step['cur']} explored",fontsize=10,fontweight="bold")
    for j in range(i+1,len(axes)): axes[j].axis("off")
    plt.tight_layout()
    def get_path(t):
        p=[]; c=t
        while c: p.append(c); c=pred[c]
        p.reverse(); return p if p and p[0]==src else []
    lines=["Shortest Paths:","─"*40]
    for n in all_nodes:
        if n!=src: lines.append(f"To {n}: {get_path(n)}  Cost={dist[n]}")
    return "\n".join(lines)

#   EXP 8   ───
def exp8_inbuilt():
    G1=nx.Graph(); G1.add_edges_from([("A","B"),("A","E"),("B","E"),("B","C"),("B","D"),("C","D")])
    pos1={"A":(0,2),"C":(2,2),"B":(1,1),"E":(0,0),"D":(2,0)}
    G2=nx.Graph(); G2.add_edges_from([("A","F"),("A","B"),("A","I"),("E","B"),("E","D"),("C","D"),
                                       ("E","H"),("E","F"),("B","C"),("D","I"),("H","G"),("H","I"),("F","G")])
    pos2={"A":(0,2),"B":(1,2),"C":(2,2),"F":(0,0.8),"E":(1,0.8),"D":(2,0.8),"G":(0,0),"H":(1,0),"I":(2,0)}
    def get_seqs(G,small):
        pe=nx.find_cycle(G)
        sub=["B","C","D"] if small else ["E","F","G","H"]
        te=list(nx.eulerian_circuit(G.subgraph(sub)))
        nodes=list(G.nodes()); p1=nx.shortest_path(G,nodes[0],nodes[1])
        wn=p1+p1[-2::-1]; we=[(wn[i],wn[i+1]) for i in range(len(wn)-1)]
        return we,te,pe
    def plot(G,pos,title,he,ax):
        nx.draw(G,pos,with_labels=True,node_color="plum",edge_color="gray",node_size=600,font_weight="bold",ax=ax)
        if he: nx.draw_networkx_edges(G,pos,edgelist=[(u,v) for u,v in he],edge_color="red",width=3,ax=ax)
        ax.set_title(title,fontsize=10)
    w1,t1,p1=get_seqs(G1,True); w2,t2,p2=get_seqs(G2,False)
    fig,axes=plt.subplots(2,4,figsize=(20,10))
    plot(G1,pos1,"G1: Original",None,axes[0,0])
    plot(G1,pos1,"G1: Closed Walk",w1,axes[0,1])
    plot(G1,pos1,"G1: Closed Trail",t1,axes[0,2])
    plot(G1,pos1,"G1: Closed Path",p1,axes[0,3])
    plot(G2,pos2,"G2: Original",None,axes[1,0])
    plot(G2,pos2,"G2: Closed Walk",w2,axes[1,1])
    plot(G2,pos2,"G2: Closed Trail",t2,axes[1,2])
    plot(G2,pos2,"G2: Closed Path",p2,axes[1,3])
    plt.tight_layout()
    return (f"G1 Walk: {w1}\nG1 Trail: {t1}\nG1 Path: {p1}\n"
            f"G2 Walk: {w2}\nG2 Trail: {t2}\nG2 Path: {p2}")

def exp8_manual():
    G1=nx.Graph(); G1.add_edges_from([("A","B"),("A","E"),("B","E"),("B","C"),("B","D"),("C","D")])
    pos1={"A":(0,2),"C":(2,2),"B":(1,1),"E":(0,0),"D":(2,0)}
    G2=nx.Graph(); G2.add_edges_from([("A","F"),("A","B"),("A","I"),("E","B"),("E","D"),("C","D"),
                                       ("E","H"),("E","F"),("B","C"),("D","I"),("H","G"),("H","I"),("F","G")])
    pos2={"A":(0,2),"B":(1,2),"C":(2,2),"F":(0,0.8),"E":(1,0.8),"D":(2,0.8),"G":(0,0),"H":(1,0),"I":(2,0)}
    w1=[("A","B"),("B","E"),("E","B"),("B","A")]
    t1=[("A","B"),("B","C"),("C","D"),("D","B"),("B","E"),("E","A")]
    p1=[("A","B"),("B","E"),("E","A")]
    w2=[("A","F"),("F","G"),("G","H"),("H","G"),("G","F"),("F","A")]
    t2=[("A","B"),("B","C"),("C","D"),("D","E"),("E","H"),("H","I"),("I","A")]
    p2=[("E","F"),("F","G"),("G","H"),("H","E")]
    def plot(G,pos,title,he,ax):
        nx.draw(G,pos,with_labels=True,node_color="lightblue",edge_color="gray",node_size=600,font_weight="bold",ax=ax)
        if he:
            valid=[(u,v) for u,v in he if G.has_edge(u,v)]
            nx.draw_networkx_edges(G,pos,edgelist=valid,edge_color="red",width=3,ax=ax)
        ax.set_title(title,fontsize=12,pad=10)
    fig,axes=plt.subplots(2,4,figsize=(22,10))
    plot(G1,pos1,"G1: Original",None,axes[0,0])
    plot(G1,pos1,"G1: Closed Walk\n(A-B-E-B-A)",w1,axes[0,1])
    plot(G1,pos1,"G1: Closed Trail\n(A-B-C-D-B-E-A)",t1,axes[0,2])
    plot(G1,pos1,"G1: Closed Path\n(A-B-E-A)",p1,axes[0,3])
    plot(G2,pos2,"G2: Original",None,axes[1,0])
    plot(G2,pos2,"G2: Closed Walk\n(A-F-G-H-G-F-A)",w2,axes[1,1])
    plot(G2,pos2,"G2: Closed Trail\n(A-B-C-D-E-H-I-A)",t2,axes[1,2])
    plot(G2,pos2,"G2: Closed Path\n(E-F-G-H-E)",p2,axes[1,3])
    plt.tight_layout(); return ""

#   EXP 9   ───
def exp9_inbuilt():
    G1=nx.Graph()
    G1.add_edges_from([("A","B"),("A","E"),("B","E"),("B","C"),("B","D"),("C","D")])
    pos1={"A":(0,2),"C":(2,2),"B":(1,1),"E":(0,0),"D":(2,0)}

    def show_inbuilt_results(G,pos,title):
        plt.figure(figsize=(10,5))
        ax1=plt.subplot(1,2,1)
        ax1.set_title(f"{title}: Original")
        nx.draw(G,pos,ax=ax1,with_labels=True,node_color="lightgreen",
                node_size=1000,font_weight="bold",arrows=False)
        ax2=plt.subplot(1,2,2)
        if nx.is_eulerian(G):
            circuit_edges=list(nx.eulerian_circuit(G))
            path_nodes=[u for u,v in circuit_edges]+[circuit_edges[-1][1]]
            path_str=" -> ".join(path_nodes)
            print(f"{title} Eulerian Circuit found: {path_str}")
            ax2.set_title(f"{title} (Eulerian Trail: {path_str})")
            NullG=G.copy(); NullG.clear_edges()
            nx.draw(NullG,pos,ax=ax2,with_labels=True,node_color="plum",
                    node_size=1000,font_weight="bold",arrows=False)
        else:
            ax2.set_title(f"{title}: No Eulerian Circuit exists")
            print(f"{title}: No Eulerian Circuit exists.")

    show_inbuilt_results(G1,pos1,"Graph G")
    plt.tight_layout()
    return ""

def exp9_manual():
    def is_bridge(G,u,v):
        if G.degree(u)==1: return False
        orig=nx.number_connected_components(G); G.remove_edge(u,v)
        new=nx.number_connected_components(G); G.add_edge(u,v); return new>orig
    def fleury(G_orig):
        is_conn=nx.is_connected(G_orig)
        odd=[v for v,d in G_orig.degree() if d%2!=0]
        if is_conn and len(odd)==0:
            out="Eulerian Circuit EXISTS.\n"
        else:
            return None,[],"Eulerian Circuit does NOT exist."
        G=G_orig.copy(); curr=sorted(G.nodes())[0]; path=[curr]; steps=[]
        steps.append((G.copy(),list(path),None))
        while G.number_of_edges()>0:
            nbrs=list(G.neighbors(curr)); chosen=None
            if len(nbrs)==1: chosen=nbrs[0]
            else:
                for n in nbrs:
                    if not is_bridge(G,curr,n): chosen=n; break
                if chosen is None: chosen=nbrs[0]
            edge=(curr,chosen); G.remove_edge(curr,chosen); curr=chosen; path.append(curr)
            steps.append((G.copy(),list(path),edge))
        return path,steps,out+"Final: "+" → ".join(path)
    G1=nx.Graph(); G1.add_edges_from([("A","B"),("A","E"),("B","E"),("B","C"),("B","D"),("C","D")])
    pos1={"A":(0,2),"C":(2,2),"B":(1,1),"E":(0,0),"D":(2,0)}
    path,steps,msg=fleury(G1)
    if steps:
        n_steps=len(steps); cols=3; rows=(n_steps+cols-1)//cols
        plt.figure(figsize=(15,4*rows))
        for i,(gs,cp,edge) in enumerate(steps):
            ax=plt.subplot(rows,cols,i+1)
            nx.draw_networkx_nodes(G1,pos1,node_color="lightblue",node_size=500,ax=ax)
            nx.draw_networkx_labels(G1,pos1,ax=ax)
            nx.draw_networkx_edges(gs,pos1,edge_color="black",width=2,ax=ax)
            we=[(cp[j],cp[j+1]) for j in range(len(cp)-1)]
            nx.draw_networkx_edges(G1,pos1,edgelist=we,edge_color="red",width=3,ax=ax)
            ttl=f"Step {i}: Start at {cp[0]}" if i==0 else f"Step {i}: {edge[0]} → {edge[1]}"
            ax.set_title(ttl); ax.axis("off")
        plt.tight_layout()
    return msg

#   EXP 10   ──
def exp10_manual():
    G=nx.Graph()
    edges=[("A","F"),("A","B"),("A","I"),("E","B"),("E","D"),("C","D"),
           ("E","H"),("E","F"),("B","C"),("D","I"),("H","G"),("H","I"),("F","G")]
    G.add_edges_from(edges)
    pos={"A":(0,2),"B":(1,2),"C":(2,2),"F":(0,0.8),"E":(1,0.8),"D":(2,0.8),"G":(0,0),"H":(1,0),"I":(2,0)}
    circuit=["A","F","G","H","E","B","C","D","I","A"]
    c_edges=[(circuit[i],circuit[i+1]) for i in range(len(circuit)-1)]
    total=len(c_edges); cols=5; rows=math.ceil((total+1)/cols)
    plt.figure(figsize=(20,rows*4))
    plt.subplot(rows,cols,1)
    nx.draw(G,pos,with_labels=True,node_color="lightgreen",edge_color="black",node_size=600,font_weight="bold")
    plt.title("Original Graph",fontsize=12)
    for i in range(total):
        plt.subplot(rows,cols,i+2)
        nx.draw(G,pos,with_labels=True,node_color="lightgreen",edge_color="black",node_size=600,font_weight="bold")
        nx.draw_networkx_edges(G,pos,edgelist=c_edges[:i+1],edge_color="red",width=3)
        nx.draw_networkx_nodes(G,pos,nodelist=[circuit[i+1]],node_color="plum",node_size=700)
        plt.title(f"Step {i+1}: {circuit[i]} → {circuit[i+1]}",fontsize=10)
    plt.tight_layout()
    return f"Hamiltonian Circuit: {' → '.join(circuit)}"

#   EXP 11   ──
EDGES11=[("A","B"),("A","G"),("A","E"),("A","F"),("B","D"),("B","C"),("C","D"),
         ("C","G"),("D","E"),("E","F"),("E","G"),("F","G")]
POS11={"A":(1,3),"B":(2,3),"F":(0.5,2),"G":(1.5,2),"C":(2.5,2),"E":(1,1),"D":(2,1)}
CSEQ=["Red","Green","Blue","Yellow"]

def exp11_inbuilt():
    G=nx.Graph(); G.add_edges_from(EDGES11)
    coloring_indices=nx.coloring.greedy_color(G,strategy="DSATUR")
    chromatic_num=max(coloring_indices.values())+1
    final_coloring={node:CSEQ[index] for node,index in coloring_indices.items()}
    fig,axes=plt.subplots(1,2,figsize=(15,7))
    nx.draw(G,POS11,ax=axes[0],with_labels=True,node_color="lightgray",node_size=1500,font_size=12,font_weight="bold")
    axes[0].set_title("Original Uncolored Graph",fontsize=14,fontweight="bold")
    nc=[final_coloring[n] for n in G.nodes()]
    nx.draw(G,POS11,ax=axes[1],with_labels=True,node_color=nc,node_size=1500,font_size=12,font_weight="bold")
    axes[1].set_title(f"Colored Graph (X(G)={chromatic_num})",fontsize=14,fontweight="bold")
    plt.tight_layout()
    lines=[f"{'Node':<10} | {'Assigned Color'}","-"*25]
    for n in sorted(final_coloring): lines.append(f"{n:<10} | {final_coloring[n]}")
    lines.extend(["-"*25, f"Chromatic Number (X(G)): {chromatic_num}"])
    return "\n".join(lines)

def exp11_manual():
    def dsatur_coloring(G,color_sequence,start_node):
        coloring={node:None for node in G.nodes()}; coloring[start_node]=color_sequence[0]
        nodes_to_color=set(G.nodes()); nodes_to_color.remove(start_node)
        while nodes_to_color:
            saturation_data=[]
            for node in nodes_to_color:
                neighbor_colors={coloring[n] for n in G.neighbors(node) if coloring[n] is not None}
                saturation_data.append((node,len(neighbor_colors)))
            saturation_data.sort(key=lambda x:(-x[1],x[0]))
            best_node=saturation_data[0][0]
            forbidden={coloring[n] for n in G.neighbors(best_node) if coloring[n] is not None}
            for c in color_sequence:
                if c not in forbidden: coloring[best_node]=c; break
            nodes_to_color.remove(best_node)
        return coloring
    G=nx.Graph(); G.add_edges_from(EDGES11)
    final_coloring=dsatur_coloring(G,CSEQ,"A")
    chromatic_num=len(set(final_coloring.values()))
    fig,axes=plt.subplots(1,2,figsize=(15,7))
    nx.draw(G,POS11,ax=axes[0],with_labels=True,node_color="lightgray",node_size=1500,font_size=12,font_weight="bold")
    axes[0].set_title("Original Graph",fontsize=14,fontweight="bold")
    nc=[final_coloring[n] for n in G.nodes()]
    nx.draw(G,POS11,ax=axes[1],with_labels=True,node_color=nc,node_size=1500,font_size=12,font_weight="bold")
    axes[1].set_title(f"Colored Graph (X(G)={chromatic_num})",fontsize=14,fontweight="bold")
    plt.tight_layout()
    lines=[f"{'Node':<10} | {'Assigned Color'}","-"*25]
    for n in sorted(final_coloring): lines.append(f"{n:<10} | {final_coloring[n]}")
    lines.extend(["-"*25, f"Chromatic Number (X(G)): {chromatic_num}"])
    return "\n".join(lines)

def exp11_sudoku():
    """Standalone Sudoku experiment (curved-edge sudoku-graph visualization)."""
    sudoku=[[0,4,0,0],[0,0,0,4],[0,0,0,0],[0,2,0,0]]
    initial_sudoku=copy.deepcopy(sudoku)
    SIZE=4; SUBGRID=2; G=nx.sudoku_graph(2); steps=[]

    def is_safe(board,row,col,num):
        for x in range(SIZE):
            if board[row][x]==num or board[x][col]==num: return False
        sr,sc=(row//SUBGRID)*SUBGRID,(col//SUBGRID)*SUBGRID
        for r in range(sr,sr+SUBGRID):
            for c in range(sc,sc+SUBGRID):
                if board[r][c]==num: return False
        return True

    def solve(board):
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col]==0:
                    for num in range(1,SIZE+1):
                        if is_safe(board,row,col,num):
                            steps.append(f"Pick cell ({row+1},{col+1}) -> Assign {num}")
                            board[row][col]=num
                            if solve(board): return True
                            board[row][col]=0
                            steps.append(f"Backtrack cell ({row+1},{col+1})")
                    return False
        return True

    # PROCESS SOLUTION
    print("\nInitial Sudoku:\n")
    for row in sudoku: print(row)
    solve(sudoku)
    print("\nSolved Sudoku:\n")
    for row in sudoku: print(row)

    colors=["red","green","skyblue","yellow"]
    pos={}; initial_colors=[]; initial_labels={}; final_colors=[]; final_labels={}
    for i in range(SIZE):
        for j in range(SIZE):
            node=i*SIZE+j; pos[node]=(j,-i)
            val_init=initial_sudoku[i][j]
            initial_labels[node]=val_init if val_init!=0 else ""
            if val_init==0:
                initial_colors.append("lightgray")
            else:
                initial_colors.append(colors[val_init-1])
            val_final=sudoku[i][j]
            final_labels[node]=val_final
            if val_final==0:
                final_colors.append("lightgray")
            else:
                final_colors.append(colors[val_final-1])

    def draw_curved_edges(G,pos,ax,edge_color='black',alpha=1,linewidth=1.2):
        rad_options=[0.08,-0.08,0.16,-0.16,0.24,-0.24,0.32,-0.32]
        for i,(u,v) in enumerate(G.edges()):
            rad=rad_options[i % len(rad_options)]
            ax.annotate(
                "",
                xy=pos[v], xycoords='data',
                xytext=pos[u], textcoords='data',
                arrowprops=dict(
                    arrowstyle="-",
                    color=edge_color,
                    alpha=alpha,
                    linewidth=linewidth,
                    connectionstyle=f"arc3,rad={rad}",
                    shrinkA=18, shrinkB=18,
                ),
            )

    fig=plt.figure(figsize=(16,8))
    # Original Graph
    ax1=plt.subplot(1,2,1)
    draw_curved_edges(G,pos,ax1)
    nx.draw_networkx_nodes(G,pos,node_color=initial_colors,node_size=1800,edgecolors='black',linewidths=2,ax=ax1)
    nx.draw_networkx_labels(G,pos,labels=initial_labels,font_size=16,font_weight='bold',ax=ax1)
    plt.title("Original Graph",fontsize=14,fontweight='bold')
    plt.axis('off')
    # Colored Graph
    ax2=plt.subplot(1,2,2)
    draw_curved_edges(G,pos,ax2)
    nx.draw_networkx_nodes(G,pos,node_color=final_colors,node_size=1800,edgecolors='black',linewidths=2,ax=ax2)
    nx.draw_networkx_labels(G,pos,labels=final_labels,font_size=16,font_weight='bold',ax=ax2)
    plt.title("Solved Sudoku Graph",fontsize=14,fontweight='bold')
    plt.axis('off')
    plt.tight_layout()

#   Dispatch table  ────────────
EXPERIMENTS = {
    "Exp 1 - Types of Graphs":               (exp1_inbuilt,  exp1_manual,  None),
    "Exp 2 - Graph Isomorphism":             (exp2_inbuilt,  exp2_manual,  None),
    "Exp 3 - Subgraphs":                     (exp3_inbuilt,  exp3_manual,  None),
    "Exp 4 - Havel-Hakimi (Degree Sequence)":(exp4_inbuilt,  exp4_manual,  None),
    "Exp 5 - Line Graph":                    (exp5_inbuilt,  exp5_manual,  None),
    "Exp 6 - Minimum Spanning Tree (Kruskal)":(exp6_inbuilt, exp6_manual,  None),
    "Exp 7 - Dijkstra's Shortest Path":      (exp7_inbuilt,  exp7_manual,  None),
    "Exp 8 - Walk / Trail / Path":           (exp8_inbuilt,  exp8_manual,  None),
    "Exp 9 - Eulerian Circuit":              (exp9_inbuilt,  exp9_manual,  None),
    "Exp 10 - Hamiltonian Circuit":          (None,          exp10_manual, None),
    "Exp 11 - Graph Coloring + Sudoku":      (exp11_inbuilt, exp11_manual, exp11_sudoku),
}

#   Override code strings for Exp 11 & Exp 4 manual (user-supplied canonical code) ──
# For all other experiments, inspect.getsource() is used automatically.
OVERRIDE_CODE = {
    ("Exp 11 - Graph Coloring + Sudoku", "With Inbuilt Functions"):  CODE_EXP11_INBUILT,
    ("Exp 11 - Graph Coloring + Sudoku", "Manual Implementation"):   CODE_EXP11_MANUAL,
    ("Exp 11 - Graph Coloring + Sudoku", "Sudoku"):                  CODE_EXP11_SUDOKU,
    ("Exp 4 - Havel-Hakimi (Degree Sequence)", "Manual Implementation"): CODE_EXP4_MANUAL,
    ("Exp 9 - Eulerian Circuit", "With Inbuilt Functions"):              CODE_EXP9_INBUILT,
}

def get_source_code(fn, exp_name, mode_name):
    """Return source code: override string if available, else inspect the function."""
    key = (exp_name, mode_name)
    if key in OVERRIDE_CODE:
        return OVERRIDE_CODE[key]
    if fn is None:
        return ""
    try:
        raw = inspect.getsource(fn)
        # Dedent so the 'def' line starts at column 0
        lines = raw.splitlines()
        if lines:
            indent = len(lines[0]) - len(lines[0].lstrip())
            lines = [l[indent:] if len(l) >= indent else l for l in lines]
        return "\n".join(lines)
    except Exception:
        return ""

#   Main UI   ─
st.markdown(f"### {experiment}")

if experiment in AIMS:
    st.markdown(
        f'<div class="exp-aim-box"><strong>Aim</strong>{AIMS[experiment]}</div>',
        unsafe_allow_html=True,
    )

fn_inbuilt, fn_manual, fn_sudoku = EXPERIMENTS[experiment]

if experiment == "Exp 10 - Hamiltonian Circuit":
    st.info("Experiment 10 only has a Manual implementation (no inbuilt NetworkX function for Hamiltonian circuits).")

if run_btn:
    if mode == "With Inbuilt Functions":
        fn = fn_inbuilt
    elif mode == "Manual Implementation":
        fn = fn_manual
    else:  # Sudoku (Exp 11 only)
        fn = fn_sudoku

    if fn is None:
        fn = fn_manual
        st.warning("No inbuilt version available. Running manual implementation.")

    with st.spinner("Running experiment..."):
        try:
            console_out, printed = capture_prints(fn)
            show_fig()

            # Always show source code
            src = get_source_code(fn, experiment, mode)
            if src.strip():
                st.subheader("Source Code")
                st.code(src, language="python")

            all_output = "\n".join(filter(None, [printed, str(console_out) if console_out else ""]))
            if all_output.strip():
                st.subheader("Console Output")
                st.code(all_output, language="text")

            # Theory & Conclusion — shown after the source code, for both
            # "With Inbuilt Functions" and "Manual Implementation" modes.
            if mode in ("With Inbuilt Functions", "Manual Implementation", "Sudoku"):
                if experiment in THEORY:
                    st.markdown(
                        f'<div class="exp-theory-box"><h4>Theory</h4>{THEORY[experiment]}</div>',
                        unsafe_allow_html=True,
                    )
                if experiment in CONCLUSIONS:
                    st.markdown(
                        f'<div class="exp-conclusion-box"><h4>Conclusion</h4>{CONCLUSIONS[experiment]}</div>',
                        unsafe_allow_html=True,
                    )
        except Exception as e:
            plt.close("all")
            st.error(f"Error: {e}")
