import numpy as np
from scipy.sparse import csc_matrix
import pymatching
import matplotlib.pyplot as plt

def step1_define_matrix():
    # 1. Define the parity check matrix (H)
    # This matrix describes the connections in our matching graph.
    # Each row corresponds to a detector (a node in the graph).
    # Each column corresponds to a potential error (an edge in the graph).
    # H[i, j] = 1 means that error 'j' flips detector 'i'.
    #
    # In this example, we have 4 detectors and 5 possible errors.
    # Error 0 connects detector 0 to the boundary.
    # Error 1 connects detector 0 and 1.
    # Error 2 connects detector 1 and 2.
    # Error 3 connects detector 2 and 3.
    # Error 4 connects detector 3 to the boundary.
    #
    # Visually, the graph looks like this:
    # (boundary) --4-- D0 --3-- D1 --2-- D2 --3-- D3 --4-- (boundary)
    # (The numbers are the weights defined below)
    H = csc_matrix([[1, 1, 0, 0, 0],
                    [0, 1, 1, 0, 0],
                    [0, 0, 1, 1, 0],
                    [0, 0, 0, 1, 1]])
    return H

def step2_define_weights():
    # 2. Define the weights for the errors (edges)
    # Each error has a "cost" or "weight". The decoder will try to find a
    # set of errors that explain the syndrome with the minimum total weight.
    # We have 5 errors, so we need 5 weights.
    weights = np.array([4, 3, 2, 3, 4])
    return weights

def step3_create_matching(H, weights):
    # 3. Create the Matching object
    # This takes our check matrix and weights and builds the internal
    # matching graph used by the decoder.
    matching = pymatching.Matching(H, weights=weights)
    return matching

def step4_define_syndrome():
    # 4. Define a syndrome to be decoded
    # A syndrome is a binary vector telling us which detectors have fired.
    # A '1' means the detector has fired.
    # In this case, detectors 1 and 3 have fired.
    syndrome = np.array([0, 1, 0, 1])
    return syndrome

def step5_decode(matching, syndrome):
    # 5. Decode the syndrome
    # The `decode` method finds a set of errors (a "prediction") that
    # results in the given syndrome and has the minimum possible total weight.
    # This is the Minimum Weight Perfect Matching solution.
    prediction = matching.decode(syndrome)
    prediction_with_weight, solution_weight = matching.decode(syndrome, return_weight=True)
    return prediction, prediction_with_weight, solution_weight

def draw_matching_graph(matching, filename, title=None, highlight_edges=None):
    # Draw the matching graph and save as SVG.
    # Optionally highlight certain edges (by index).
    import networkx as nx
    fig, ax = plt.subplots(figsize=(6, 3))
    plt.sca(ax)
    matching.draw()
    if highlight_edges is not None:
        # Highlight the selected edges in red
        G = matching.to_networkx()
        edge_list = list(G.edges)
        pos = nx.spring_layout(G, seed=42)
        for idx in highlight_edges:
            if idx < len(edge_list):
                u, v = edge_list[idx]
                nx.draw_networkx_edges(G, pos=pos, edgelist=[(u, v)], edge_color='red', width=3, ax=ax)
    if title:
        ax.set_title(title)
    plt.tight_layout()
    plt.savefig(filename, format='svg')
    plt.close(fig)

def main():
    # Step 1: Define matrix
    H = step1_define_matrix()
    # Step 2: Define weights
    weights = step2_define_weights()
    # Step 3: Create matching object
    matching = step3_create_matching(H, weights)
    # Step 4: Define syndrome
    syndrome = step4_define_syndrome()
    # Step 5: Decode
    prediction, prediction_with_weight, solution_weight = step5_decode(matching, syndrome)

    # Draw SVGs for each step
    draw_matching_graph(matching, "step3_matching_graph.svg", title="Step 3: Matching Graph")
    # Highlight the predicted errors in the graph for the decode step
    highlight_edges = [i for i, val in enumerate(prediction) if val]
    draw_matching_graph(matching, "step5_decoded_solution.svg", title="Step 5: Decoded Solution", highlight_edges=highlight_edges)

    print("--- PyMatching Example ---")
    print(f"Syndrome (detectors that fired): {syndrome}")
    print(f"Predicted errors (edges to flip): {prediction}")
    print(f"Total weight of the solution: {solution_weight}")
    print("\n--- Explanation ---")
    print("The syndrome [0, 1, 0, 1] means detectors 1 and 3 have fired.")
    print("The decoder found that the lowest-weight set of errors to cause this is to apply errors 2 and 3.")
    print("Error 2 connects detectors 1 and 2, and has weight 2.")
    print("Error 3 connects detectors 2 and 3, and has weight 3.")
    print("This 'path' of errors flips detectors 1 and 3, and the intermediate detector 2 is flipped twice, so its final state is 0.")
    print(f"The total weight is 2 + 3 = {solution_weight}.")
    print(f"The prediction vector {prediction} has 1s at indices 2 and 3, indicating which errors were chosen.")
    print("\nSVGs generated:")
    print(" - step3_matching_graph.svg: The matching graph after construction.")
    print(" - step5_decoded_solution.svg: The graph with the decoded solution highlighted.")

if __name__ == "__main__":
    main()
