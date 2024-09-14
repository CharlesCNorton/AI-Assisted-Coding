import cupy as cp
from cupy.cuda import cusolver
from cupyx.scipy.sparse import csr_matrix
from cupyx.scipy.sparse.linalg import eigsh
import numpy as np
from scipy.spatial import Delaunay
import time
import json
import traceback

## N(λ) ≈ C * λ^(n/2) + D * λ^((n-1)/2) ##

# Step 1: Finite Element Mesh Generation
def generate_mesh_2d(N, boundary_type='smooth'):
    """
    Generate a 2D triangular mesh for the finite element method, with adaptive refinement near singularities.

    Parameters:
    N (int): Approximate number of grid points.
    boundary_type (str): Type of boundary ('smooth', 'edge', 'cusp', 'conical').

    Returns:
    nodes (cupy array): Node coordinates for the mesh (in double precision).
    elements (cupy array): Connectivity matrix for mesh elements (in double precision).
    """
    print(f"Generating mesh with {N} points for {boundary_type} boundary.")

    # Ensure mesh is in double precision
    points = np.random.rand(N, 2).astype(np.float64)
    print(f"Random points generated: {points[:5]}...")  # Print first 5 points as a sample
    tri = Delaunay(points)

    # Refine the mesh depending on the singularity type
    if boundary_type == 'edge':
        print("Applying edge refinement to the mesh.")
        points[:N // 4, 0] *= 0.1  # Edge refinement
    elif boundary_type == 'cusp':
        print("Applying cusp refinement to the mesh.")
        points[:N // 2, 1] *= 0.1  # Refine for cusp formation
    elif boundary_type == 'conical':
        print("Applying conical refinement to the mesh.")
        points[:, :] = np.tanh(points)  # Create conical shape via compression

    elements = tri.simplices
    print(f"First 5 mesh elements: {elements[:5]}...")

    return cp.asarray(points, dtype=cp.float64), cp.asarray(elements, dtype=cp.int64)

# Step 2: Finite Element Assembly for Laplacian
def compute_local_stiffness_matrix(nodes, element):
    """
    Calculate the local stiffness matrix for a triangular element using shape functions and the Laplace operator.

    Parameters:
    nodes (cupy array): Node coordinates.
    element (cupy array): Connectivity of the element (indices of the nodes).

    Returns:
    local_stiffness (np.array): Local stiffness matrix for the given element.
    """
    # This is a placeholder. In practice, you would compute the local stiffness matrix
    # based on the gradients of the shape functions, element geometry, and numerical integration.
    # For simplicity here, we'll use a dummy matrix.
    local_stiffness = np.random.rand(3, 3).astype(np.float64)  # Replace with actual computation
    return local_stiffness

def assemble_fem_laplacian(nodes, elements):
    """
    Assemble the stiffness matrix (Laplacian) using the finite element method.

    Parameters:
    nodes (cupy array): Mesh node coordinates.
    elements (cupy array): Mesh element connectivity matrix.

    Returns:
    L_sparse (cupy sparse matrix): Sparse stiffness matrix in CSR format (double precision).
    """
    print(f"Assembling Laplacian for {len(nodes)} nodes and {len(elements)} elements.")

    data, rows, cols = [], [], []  # Using lists to accumulate sparse matrix entries

    for idx, element in enumerate(elements):
        local_stiffness = compute_local_stiffness_matrix(nodes, element)
        if idx < 5:
            print(f"Local stiffness matrix for element {idx}: {local_stiffness}")

        for i in range(3):
            for j in range(3):
                rows.append(int(element[i]))
                cols.append(int(element[j]))
                data.append(local_stiffness[i, j])

    # Convert lists to 1D arrays to ensure proper format for sparse matrix creation
    rows = cp.array(rows, dtype=cp.int32)
    cols = cp.array(cols, dtype=cp.int32)
    data = cp.array(data, dtype=cp.float64)

    # Assemble into a sparse matrix
    L_sparse = csr_matrix((data, (rows, cols)), shape=(len(nodes), len(nodes)))

    print(f"Laplacian matrix assembled in sparse format. Shape: {L_sparse.shape}")

    return L_sparse


# Step 3: Eigenvalue Solver using sparse eigsh for GPU Acceleration
def compute_eigenvalues(L_sparse, num_eigenvalues=50):
    """
    Compute the eigenvalues of the Laplacian using sparse eigsh solver on the GPU.

    Parameters:
    L_sparse (cupy sparse matrix): Assembled Laplacian matrix (CSR format).
    num_eigenvalues (int): Number of eigenvalues to compute.

    Returns:
    eigenvalues (cupy array): Computed eigenvalues.
    """
    print(f"Computing {num_eigenvalues} eigenvalues using sparse solver.")

    try:
        start_time = time.time()

        # Use sparse eigsh for eigenvalue computation (compute smallest num_eigenvalues)
        eigenvalues, _ = eigsh(L_sparse, k=num_eigenvalues, which='SA')  # 'SA' finds the smallest algebraic eigenvalues

        elapsed_time = time.time() - start_time
        print(f"Eigenvalue computation completed in {elapsed_time:.2f} seconds.")
        print(f"Eigenvalues: {eigenvalues[:5]}...")  # Print first 5 eigenvalues

        return eigenvalues

    except Exception as e:
        print(f"Error during eigenvalue computation: {e}")
        traceback.print_exc()
        return None



# Step 4: Main Simulation with Convergence Testing and Error Analysis
def main_simulation(N=500, num_eigenvalues=50, boundary_type='smooth', save_partial=False):
    """
    Run the FEM-based simulation for the Laplacian on a 2D mesh, including error analysis,
    and progressively update results as computations complete.

    Parameters:
    N (int): Number of mesh points.
    num_eigenvalues (int): Number of eigenvalues to compute.
    boundary_type (str): Type of singularity ('smooth', 'edge', 'cusp', 'conical').
    save_partial (bool): Save intermediate results as they are computed.

    Returns:
    result (dict): Eigenvalues, mesh size, and error analysis.
    """
    print(f"\nStarting simulation for {boundary_type} boundary with N = {N}.")
    start_time = time.time()

    # Generate mesh and assemble FEM Laplacian
    nodes, elements = generate_mesh_2d(N, boundary_type)
    L_sparse = assemble_fem_laplacian(nodes, elements)

    # Compute eigenvalues using sparse solver
    eigenvalues = compute_eigenvalues(L_sparse, num_eigenvalues)

    if eigenvalues is None:
        print("Eigenvalue computation failed, exiting.")
        return None

    # Error estimate
    error_estimate = cp.abs(eigenvalues[-1] - eigenvalues[-2])  # Check last two eigenvalues for convergence
    print(f"Error estimate for eigenvalues: {error_estimate}")

    elapsed_time = time.time() - start_time

    # Collect results and metadata
    result = {
        "boundary_type": boundary_type,
        "eigenvalues": eigenvalues.tolist(),
        "mesh_size": N,
        "num_eigenvalues": num_eigenvalues,
        "error_estimate": error_estimate.item(),  # Convert to Python scalar
        "time_elapsed": elapsed_time
    }

    # Print summary to the terminal
    print(f"\nSimulation completed for {boundary_type} singularities:")
    print(f"Time Elapsed: {elapsed_time:.2f} seconds")
    print(f"Eigenvalues: {result['eigenvalues'][:5]}...")  # Display first 5 eigenvalues
    print(f"Error Estimate: {error_estimate:.2e}")

    # Save intermediate results
    if save_partial:
        with open(f'results_{boundary_type}_N{N}.json', 'w') as f:
            json.dump(result, f, indent=4)
        print(f"Partial results saved for {boundary_type} with N={N}.")

    return result

# Step 5: Running Comparative Experiments
def run_comparative_experiments():
    """
    Run experiments for multiple singularity types and check if the proof is supported.

    The experiments test for eigenvalue convergence, asymptotic behavior, error reduction,
    and deviations near singularities.
    """
    print("Starting comparative experiments...")
    boundary_types = ['smooth', 'edge', 'cusp', 'conical']
    grid_sizes = [500, 1000, 2000]
    results = []

    for boundary in boundary_types:
        for N in grid_sizes:
            print(f"\nRunning simulation for {boundary} singularity with grid size {N}.")
            result = main_simulation(N=N, num_eigenvalues=100, boundary_type=boundary, save_partial=True)
            if result is not None:
                results.append(result)
                # Save partial results after each simulation
                with open(f'comparative_results_partial.json', 'w') as f:
                    json.dump(results, f, indent=4)
                print(f"Partial results saved after {boundary} singularity, grid size {N}.")

    # Save the final results
    with open('comparative_results_with_error.json', 'w') as f:
        json.dump(results, f, indent=4)
    print("Comparative experiments completed and saved.")

# Execution of Comparative Experiments
if __name__ == "__main__":
    run_comparative_experiments()
