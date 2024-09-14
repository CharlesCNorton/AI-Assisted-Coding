import numpy as np
import cupy as cp
from cupyx.scipy.sparse import csr_matrix
from cupyx.scipy.sparse.linalg import eigsh
from scipy.spatial import Delaunay, cKDTree
import time
import json
import sys
import traceback

def generate_mesh_2d(N, boundary_type='smooth'):
    try:
        print(f"Generating mesh with {N} points for {boundary_type} boundary.")
        points = np.random.rand(N, 2).astype(np.float64)

        if boundary_type == 'edge':
            print("Applying edge refinement to the mesh.")
            points[:, 0] *= 0.5
        elif boundary_type == 'cusp':
            print("Applying cusp refinement to the mesh.")
            points[:, 1] = points[:, 1] ** 2
        elif boundary_type == 'conical':
            print("Applying conical refinement to the mesh.")
            r = np.sqrt(points[:, 0] ** 2 + points[:, 1] ** 2)
            theta = np.arctan2(points[:, 1], points[:, 0])
            r = r ** 0.5
            points[:, 0] = r * np.cos(theta)
            points[:, 1] = r * np.sin(theta)

        points = remove_close_points(points)
        tri = Delaunay(points)
        elements = tri.simplices

        areas = compute_element_areas(points, elements)
        min_area_threshold = 1e-8
        valid_elements = elements[areas > min_area_threshold]
        elements = valid_elements

        print(f"Generated mesh with {len(points)} nodes and {len(elements)} elements.")
        return cp.asarray(points, dtype=cp.float64), cp.asarray(elements, dtype=cp.int32)
    except Exception as e:
        print(f"Error during mesh generation: {e}")
        traceback.print_exc()
        sys.exit(1)

def remove_close_points(points, min_distance=1e-5):
    try:
        tree = cKDTree(points)
        pairs = tree.query_pairs(r=min_distance)
        points_to_remove = {i2 for i1, i2 in pairs}
        mask = np.ones(len(points), dtype=bool)
        mask[list(points_to_remove)] = False
        return points[mask]
    except Exception as e:
        print(f"Error during removal of close points: {e}")
        traceback.print_exc()
        sys.exit(1)

def compute_element_areas(points, elements):
    try:
        coords = points[elements]
        vec1 = coords[:, 1, :] - coords[:, 0, :]
        vec2 = coords[:, 2, :] - coords[:, 0, :]
        cross = vec1[:, 0] * vec2[:, 1] - vec1[:, 1] * vec2[:, 0]
        areas = 0.5 * np.abs(cross)
        return areas
    except Exception as e:
        print(f"Error during computation of element areas: {e}")
        traceback.print_exc()
        sys.exit(1)

def compute_local_stiffness_matrix(nodes, element):
    try:
        element_indices = element.get()
        coords = nodes.get()[element_indices, :]

        ones = np.ones(3)
        area_matrix = np.column_stack((ones, coords))

        area = 0.5 * np.linalg.det(area_matrix)
        if area <= 0:
            return np.zeros((3, 3))

        b = np.zeros(3)
        c = np.zeros(3)
        for i in range(3):
            j = (i + 1) % 3
            k = (i + 2) % 3
            b[i] = coords[j, 1] - coords[k, 1]
            c[i] = coords[k, 0] - coords[j, 0]
        b /= (2 * area)
        c /= (2 * area)

        stiffness = (np.outer(b, b) + np.outer(c, c)) * area * 2
        return stiffness
    except Exception as e:
        print(f"Error computing local stiffness matrix: {e}")
        traceback.print_exc()
        sys.exit(1)

def assemble_fem_laplacian(nodes, elements):
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

def apply_dirichlet_boundary_conditions(L_sparse, nodes):
    try:
        N = len(nodes)
        tol = 1e-5
        boundary_nodes = cp.where(
            (cp.abs(nodes[:, 0]) < tol) | (cp.abs(nodes[:, 0] - 1) < tol) |
            (cp.abs(nodes[:, 1]) < tol) | (cp.abs(nodes[:, 1] - 1) < tol)
        )[0]

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
    try:
        print(f"Computing {num_eigenvalues} smallest non-zero eigenvalues using sparse solver.")

        L_sparse = (L_sparse + L_sparse.T) / 2

        eigenvalues, _ = eigsh(L_sparse, k=num_eigenvalues + 20, which='SA', tol=1e-6, maxiter=3000)

        eigenvalues = cp.sort(eigenvalues)
        eigenvalues = eigenvalues[eigenvalues > 1e-8]
        eigenvalues = eigenvalues[:num_eigenvalues]

        print(f"Eigenvalue computation completed.")
        return eigenvalues
    except Exception as e:
        print(f"Error during eigenvalue computation: {e}")
        traceback.print_exc()
        sys.exit(1)

def main_simulation(N=5000, num_eigenvalues=100, boundary_type='smooth'):
    try:
        print(f"\nStarting simulation for {boundary_type} boundary with N = {N}.")
        start_time = time.time()
        nodes, elements = generate_mesh_2d(N, boundary_type)
        L_sparse = assemble_fem_laplacian(nodes, elements)

        L_sparse = apply_dirichlet_boundary_conditions(L_sparse, nodes)

        eigenvalues = compute_eigenvalues(L_sparse, num_eigenvalues)
        if eigenvalues is None or len(eigenvalues) == 0:
            print("Eigenvalue computation failed or returned no valid eigenvalues.")
            sys.exit(1)

        elapsed_time = time.time() - start_time
        print(f"Simulation completed in {elapsed_time:.2f} seconds.")

        result = {
            "boundary_type": boundary_type,
            "eigenvalues": eigenvalues.get().tolist(),
            "mesh_size": N,
            "num_eigenvalues": num_eigenvalues,
            "elapsed_time": elapsed_time
        }
        return result
    except Exception as e:
        print(f"Error during main simulation: {e}")
        traceback.print_exc()
        sys.exit(1)

def run_torture_tests():
    try:
        print("Starting torture tests with increased mesh sizes and number of eigenvalues...")
        boundary_types = ['smooth', 'edge', 'cusp', 'conical']
        grid_sizes = [5000, 10000, 20000]  # Mesh sizes increased by a factor of 10
        num_eigenvalues = 100  # Number of eigenvalues increased to 100
        results = []
        for boundary in boundary_types:
            for N in grid_sizes:
                print(f"\nRunning simulation for {boundary} singularity with grid size {N}.")
                result = main_simulation(N=N, num_eigenvalues=num_eigenvalues, boundary_type=boundary)
                if result:
                    results.append(result)
                    print(f"Simulation for {boundary} with N={N} completed.")
        with open('torture_test_results.json', 'w') as f:
            json.dump(results, f, indent=4)
        print("Torture tests completed and results saved.")
    except Exception as e:
        print(f"Error during torture tests: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_torture_tests()
