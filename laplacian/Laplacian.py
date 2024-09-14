import numpy as np
import cupy as cp
from cupyx.scipy.sparse import csr_matrix
from cupyx.scipy.sparse.linalg import eigsh
from scipy.spatial import Delaunay, cKDTree
import time
import json
import sys
import traceback
import matplotlib.pyplot as plt
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=RuntimeWarning)

def generate_mesh(N, boundary_type='smooth', dimension=3):
    """
    Generate a 3D mesh for the finite element method, with adaptive refinement near singularities.
    """
    try:
        print(f"Generating {dimension}D mesh with {N} points for {boundary_type} boundary.")
        points = np.random.rand(N, dimension).astype(np.float64)

        # Refine the mesh depending on the singularity type
        if boundary_type == 'edge':
            print("Applying edge refinement to the mesh (3D).")
            points[:, 0] *= 0.5  # Compress along x-axis near x=0
        elif boundary_type == 'cusp':
            print("Applying cusp refinement to the mesh (3D).")
            points[:, 2] = points[:, 2] ** 2  # Concentrate points near z=0
        elif boundary_type == 'conical':
            print("Applying conical refinement to the mesh (3D).")
            r = np.linalg.norm(points, axis=1)
            theta = np.arccos(points[:, 2] / r)
            phi = np.arctan2(points[:, 1], points[:, 0])
            r = r ** 0.5  # Adjust radial distance
            points[:, 0] = r * np.sin(theta) * np.cos(phi)
            points[:, 1] = r * np.sin(theta) * np.sin(phi)
            points[:, 2] = r * np.cos(theta)

        # Ensure points remain within the unit cube after transformation
        points = np.clip(points, 0.0, 1.0)

        # Remove duplicate or too-close points
        points = remove_close_points(points)

        # Create Delaunay triangulation in 3D
        tri = Delaunay(points)
        elements = tri.simplices  # Tetrahedra with 4 nodes

        # Compute and filter elements with small volumes
        volumes = compute_element_volumes(points, elements)
        min_volume_threshold = 1e-12  # Adjusted threshold for 3D
        valid_elements = elements[volumes > min_volume_threshold]
        elements = valid_elements

        print(f"Generated mesh with {len(points)} nodes and {len(elements)} elements.")
        return cp.asarray(points, dtype=cp.float64), cp.asarray(elements, dtype=cp.int32)
    except Exception as e:
        print(f"Error during mesh generation: {e}")
        traceback.print_exc()
        sys.exit(1)

def remove_close_points(points, min_distance=1e-5):
    """
    Remove points that are too close to each other to avoid degenerate elements.
    """
    try:
        print("Removing close points to prevent degenerate elements...")
        tree = cKDTree(points)
        pairs = tree.query_pairs(r=min_distance)
        points_to_remove = {i2 for i1, i2 in pairs}
        mask = np.ones(len(points), dtype=bool)
        mask[list(points_to_remove)] = False
        filtered_points = points[mask]
        print(f"Reduced from {len(points)} to {len(filtered_points)} points after removing close points.")
        return filtered_points
    except Exception as e:
        print(f"Error during removal of close points: {e}")
        traceback.print_exc()
        sys.exit(1)

def compute_element_volumes(points, elements):
    """
    Compute the volumes of tetrahedral elements.
    """
    try:
        coords = points[elements]
        # Vectors along the edges
        v0 = coords[:, 0, :]
        v1 = coords[:, 1, :]
        v2 = coords[:, 2, :]
        v3 = coords[:, 3, :]

        # Compute volume of tetrahedra
        vol = np.abs(np.einsum('ij,ij->i', np.cross(v1 - v0, v2 - v0), v3 - v0)) / 6.0
        return vol
    except Exception as e:
        print(f"Error during computation of element volumes: {e}")
        traceback.print_exc()
        sys.exit(1)

def compute_local_stiffness_matrix(nodes, element):
    """
    Calculate the local stiffness matrix for a tetrahedral element using linear shape functions.
    """
    try:
        # Extract node coordinates
        element_indices = element.get()
        coords = nodes.get()[element_indices, :]  # Shape: (4, 3)

        # Compute volume of the tetrahedron
        v0 = coords[0]
        v1 = coords[1]
        v2 = coords[2]
        v3 = coords[3]
        mat = np.array([
            [1, v0[0], v0[1], v0[2]],
            [1, v1[0], v1[1], v1[2]],
            [1, v2[0], v2[1], v2[2]],
            [1, v3[0], v3[1], v3[2]],
        ])
        volume = np.abs(np.linalg.det(mat)) / 6.0
        if volume <= 0:
            return np.zeros((4, 4))

        # Compute the gradients of the shape functions
        grads = np.zeros((4, 3))
        coeff_matrix = np.hstack((np.ones((4, 1)), coords))
        inv_coeff_matrix = np.linalg.inv(coeff_matrix)

        # The gradients of the shape functions are given by the last three rows of the inverse matrix
        for i in range(4):
            coeffs = inv_coeff_matrix[:, i]
            grads[i, :] = coeffs[1:]  # Gradient components

        # Compute the local stiffness matrix
        stiffness = np.zeros((4, 4))
        for i in range(4):
            for j in range(4):
                stiffness[i, j] = volume * np.dot(grads[i], grads[j])
        return stiffness
    except Exception as e:
        print(f"Error computing local stiffness matrix: {e}")
        traceback.print_exc()
        sys.exit(1)

def assemble_fem_laplacian(nodes, elements):
    """
    Assemble the global stiffness matrix (Laplacian) using the finite element method.
    """
    try:
        print(f"Assembling Laplacian for {len(nodes)} nodes and {len(elements)} elements.")

        data = []
        rows = []
        cols = []

        for idx, element in enumerate(elements):
            local_stiffness = compute_local_stiffness_matrix(nodes, element)
            if local_stiffness is None or np.all(local_stiffness == 0):
                continue

            for i_local, i_global in enumerate(element):
                for j_local, j_global in enumerate(element):
                    rows.append(int(i_global.get()))
                    cols.append(int(j_global.get()))
                    data.append(local_stiffness[i_local, j_local])

        rows_cu = cp.array(rows, dtype=cp.int32)
        cols_cu = cp.array(cols, dtype=cp.int32)
        data_cu = cp.array(data, dtype=cp.float64)

        N = len(nodes)
        L_sparse = csr_matrix((data_cu, (rows_cu, cols_cu)), shape=(N, N))

        print(f"Laplacian matrix assembled in sparse format. Shape: {L_sparse.shape}")
        return L_sparse
    except Exception as e:
        print(f"Error during assembly of FEM Laplacian: {e}")
        traceback.print_exc()
        sys.exit(1)

def identify_boundary_nodes(nodes):
    """
    Identify boundary nodes for a 3D unit cube domain.
    """
    try:
        tol = 1e-5
        boundary_nodes = cp.where(
            (cp.abs(nodes[:, 0]) < tol) | (cp.abs(nodes[:, 0] - 1) < tol) |
            (cp.abs(nodes[:, 1]) < tol) | (cp.abs(nodes[:, 1] - 1) < tol) |
            (cp.abs(nodes[:, 2]) < tol) | (cp.abs(nodes[:, 2] - 1) < tol)
        )[0]
        return boundary_nodes
    except Exception as e:
        print(f"Error identifying boundary nodes: {e}")
        traceback.print_exc()
        sys.exit(1)

def apply_dirichlet_boundary_conditions(L_sparse, nodes):
    """
    Apply zero Dirichlet boundary conditions to the global stiffness matrix.
    """
    try:
        boundary_nodes = identify_boundary_nodes(nodes)
        print(f"Number of boundary nodes: {len(boundary_nodes)}")

        L_sparse_cpu = L_sparse.get().tolil()

        for node in boundary_nodes.get():
            L_sparse_cpu.rows[node] = [node]
            L_sparse_cpu.data[node] = [1.0]
            L_sparse_cpu[node, :] = 0
            L_sparse_cpu[:, node] = 0
            L_sparse_cpu[node, node] = 1.0

        L_sparse_cpu = L_sparse_cpu.tocsr()
        L_sparse_bc = csr_matrix(L_sparse_cpu)

        return L_sparse_bc
    except Exception as e:
        print(f"Error applying Dirichlet boundary conditions: {e}")
        traceback.print_exc()
        sys.exit(1)

def compute_eigenvalues(L_sparse, num_eigenvalues=100):
    """
    Compute the eigenvalues of the Laplacian using sparse eigsh solver on the GPU.
    """
    try:
        print(f"Computing {num_eigenvalues} smallest non-zero eigenvalues using sparse solver.")

        L_sparse = (L_sparse + L_sparse.T) / 2

        eigenvalues, _ = eigsh(L_sparse, k=num_eigenvalues + 10, which='SA', tol=1e-6, maxiter=5000)

        eigenvalues = cp.sort(eigenvalues)
        eigenvalues = eigenvalues[eigenvalues > 1e-8]
        eigenvalues = eigenvalues[:num_eigenvalues]

        print(f"Eigenvalue computation completed.")
        return eigenvalues
    except Exception as e:
        print(f"Error during eigenvalue computation: {e}")
        traceback.print_exc()
        sys.exit(1)

def main_simulation(N=100000, num_eigenvalues=100, boundary_type='smooth'):
    """
    Run the FEM-based simulation for the Laplacian, including statistical output.
    """
    try:
        print(f"\nStarting simulation for {boundary_type} boundary with N = {N}.")
        dimension = 3
        start_time = time.time()
        nodes, elements = generate_mesh(N, boundary_type, dimension)
        L_sparse = assemble_fem_laplacian(nodes, elements)

        L_sparse = apply_dirichlet_boundary_conditions(L_sparse, nodes)

        eigenvalues = compute_eigenvalues(L_sparse, num_eigenvalues)
        if eigenvalues is None or len(eigenvalues) == 0:
            print("Eigenvalue computation failed or returned no valid eigenvalues.")
            sys.exit(1)

        elapsed_time = time.time() - start_time
        print(f"Simulation completed in {elapsed_time:.2f} seconds.")

        # Compute summary statistics
        eigenvalues_cpu = eigenvalues.get()
        min_eigenvalue = np.min(eigenvalues_cpu)
        max_eigenvalue = np.max(eigenvalues_cpu)
        mean_eigenvalue = np.mean(eigenvalues_cpu)
        median_eigenvalue = np.median(eigenvalues_cpu)
        std_eigenvalue = np.std(eigenvalues_cpu)
        first_ten_eigenvalues = eigenvalues_cpu[:10]
        eigenvalue_gaps = np.diff(eigenvalues_cpu[:10])

        print(f"\nSummary Statistics:")
        print(f"Number of eigenvalues computed: {len(eigenvalues_cpu)}")
        print(f"Minimum eigenvalue: {min_eigenvalue}")
        print(f"Maximum eigenvalue: {max_eigenvalue}")
        print(f"Mean eigenvalue: {mean_eigenvalue}")
        print(f"Median eigenvalue: {median_eigenvalue}")
        print(f"Standard deviation: {std_eigenvalue}")
        print(f"First 10 eigenvalues: {first_ten_eigenvalues}")
        print(f"Eigenvalue gaps (first 10): {eigenvalue_gaps}")

        # Save eigenvalues to file
        filename = f"eigenvalues_{boundary_type}_n{N}_d{dimension}.npy"
        np.save(filename, eigenvalues_cpu)
        print(f"Eigenvalues saved to {filename}")

        # Optional: Plot eigenvalue distribution
        plt.figure(figsize=(10, 6))
        plt.plot(eigenvalues_cpu, np.arange(1, len(eigenvalues_cpu)+1), drawstyle='steps-post')
        plt.xlabel('Eigenvalue λ')
        plt.ylabel('Eigenvalue Count N(λ)')
        plt.title(f'Eigenvalue Distribution for {boundary_type.capitalize()} Boundary (N={N}, Dimension={dimension})')
        plt.grid(True)
        plot_filename = f'eigenvalues_distribution_{boundary_type}.png'
        plt.savefig(plot_filename)
        print(f"Eigenvalue distribution plot saved as {plot_filename}")

        result = {
            "boundary_type": boundary_type,
            "dimension": dimension,
            "mesh_size": N,
            "num_eigenvalues": num_eigenvalues,
            "elapsed_time": elapsed_time,
            "summary_statistics": {
                "min_eigenvalue": min_eigenvalue,
                "max_eigenvalue": max_eigenvalue,
                "mean_eigenvalue": mean_eigenvalue,
                "median_eigenvalue": median_eigenvalue,
                "std_eigenvalue": std_eigenvalue,
                "first_ten_eigenvalues": first_ten_eigenvalues.tolist(),
                "eigenvalue_gaps": eigenvalue_gaps.tolist()
            }
        }
        return result
    except Exception as e:
        print(f"Error during main simulation: {e}")
        traceback.print_exc()
        sys.exit(1)

def run_simulations():
    """
    Run simulations for multiple boundary types and mesh sizes.
    """
    try:
        boundary_types = ['smooth', 'edge', 'cusp', 'conical']
        N = 100000  # Mesh size
        num_eigenvalues = 100  # Adjust as needed based on computational resources
        results = []

        for boundary in boundary_types:
            result = main_simulation(N=N, num_eigenvalues=num_eigenvalues, boundary_type=boundary)
            results.append(result)
            print(f"\nSimulation completed for {boundary} boundary. Results:")
            print(json.dumps(result["summary_statistics"], indent=4))

        # Save all results to a JSON file
        with open('simulation_results.json', 'w') as f:
            json.dump(results, f, indent=4)
        print("\nAll simulations completed and results saved to 'simulation_results.json'.")
    except Exception as e:
        print(f"Error during simulations: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_simulations()
