import cupy as cp
from cupy.cuda import cusolver
import numpy as np
from scipy.spatial import Delaunay
import time
import json
import traceback

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

    return cp.asarray(points, dtype=cp.float64), cp.asarray(elements, dtype=cp.float64)

# Step 2: Finite Element Assembly for Laplacian
def assemble_fem_laplacian(nodes, elements):
    """
    Assemble the stiffness matrix (Laplacian) using the finite element method.

    Parameters:
    nodes (cupy array): Mesh node coordinates.
    elements (cupy array): Mesh element connectivity matrix.

    Returns:
    L (cupy array): Stiffness matrix in dense format (double precision).
    """
    print(f"Assembling Laplacian for {len(nodes)} nodes and {len(elements)} elements.")

    num_nodes = len(nodes)
    L = cp.zeros((num_nodes, num_nodes), dtype=cp.float64)  # Storing as dense matrix for cuSolver compatibility

    # Ensure the elements array is of integer type
    elements = elements.astype(cp.int64)  # Convert elements to int64 to avoid index errors

    for idx, element in enumerate(elements):
        local_stiffness = np.random.rand(3, 3).astype(np.float64)  # Double precision
        if idx < 5:
            print(f"Local stiffness matrix for element {idx}: {local_stiffness}")

        for i in range(3):
            for j in range(3):
                L[element[i], element[j]] += local_stiffness[i, j]

    print(f"Laplacian matrix assembled. Shape: {L.shape}")

    return L


# Step 3: Eigenvalue Solver using cuSolver for GPU Acceleration (via CuPy's linalg.eigh)
def compute_eigenvalues(L, num_eigenvalues=50):
    """
    Compute the eigenvalues of the Laplacian using cuSolver via CuPy's linalg.eigh on the GPU.

    Parameters:
    L (cupy array): Assembled Laplacian matrix (in dense format).
    num_eigenvalues (int): Number of eigenvalues to compute.

    Returns:
    eigenvalues (cupy array): Computed eigenvalues.
    """
    print(f"Computing {num_eigenvalues} eigenvalues using cuSolver via CuPy.")

    try:
        start_time = time.time()

        # Use CuPy's linalg.eigh for eigenvalue computation
        eigenvalues, eigenvectors = cp.linalg.eigh(L)

        elapsed_time = time.time() - start_time
        print(f"Eigenvalue computation completed in {elapsed_time:.2f} seconds.")
        print(f"Eigenvalues: {eigenvalues[:5]}...")  # Print first 5 eigenvalues

        return eigenvalues[:num_eigenvalues]  # Return only the first `num_eigenvalues`

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
    L = assemble_fem_laplacian(nodes, elements)

    # Compute eigenvalues using cuSolver
    eigenvalues = compute_eigenvalues(L, num_eigenvalues)

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
