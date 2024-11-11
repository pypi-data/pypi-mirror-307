# solver.py
from gurobipy import Model, GRB, GurobiError
from typing import List, Dict
from .ParentSolver import Parent_Solver
import time

class Solver_KBest(Parent_Solver):

    def solve(self, k: int) -> None:
        """
        Implements the incremental k-best column generation method.

        Args:
            k (int): The number of best routes to find in each iteration.
        """
        # Record the start time
        start = time.time()

        try:
            # Optimize the initial Gurobi model (first stage)
            self.model.optimize()
        except GurobiError as e:
            print(f"Cannot solve LP with Gurobi: {str(e)}", file=sys.stderr)
            raise

        # Check if the optimization was successful
        if self.model.status != GRB.OPTIMAL:
            print("Initial LP is infeasible or unbounded!", file=sys.stderr)
            sys.exit(1)  # EXIT_FAILURE equivalent in Python

        # Print the initial objective value
        print(f"Solved MP. Cost: {self.model.objVal}")

        iteration = 1  # Tracking iterations

        while True:
            # Record the start time of the iteration
            start_iter_time = time.time()
            print(f"\n === Iteration {iteration} ===")

            # Populate the duals map with dual variables from covering constraints
            duals = {v: cst.Pi for v, cst in self.covering.items()}

            # Solve the pricing problem to find k-best new routes with negative reduced cost
            new_routes = self.sp_solver.solve_incremental_k_best_shortest_path(duals, k)

            # Calculate the runtime for this iteration
            end_iter_time = time.time()
            runtime_iter = end_iter_time - start_iter_time
            print(f"Run time for iteration {iteration} is {runtime_iter:.3f} seconds")

            if not new_routes:
                print("Solved SP. Found no column with <0 reduced cost.")
                break

            print(f"Solved SP. Found {len(new_routes)} columns with <0 reduced cost.")

            for route in new_routes:
                print(f"\t{route}")  # Assumes Route class has __str__ or __repr__ implemented
                self.add_route_route(route)  # Add the new route to the model

            try:
                # Optimize the model again after adding new routes
                self.model.optimize()
            except GurobiError as e:
                print(f"Cannot solve LP with Gurobi: {str(e)}", file=sys.stderr)
                raise

            # Check if the optimization was successful
            if self.model.status != GRB.OPTIMAL:
                print(f"LP is infeasible or unbounded at iteration {iteration}!", file=sys.stderr)

                lp_filename = f"infeasible_lp_iter_{iteration}.lp"
                self.model.write(lp_filename)

                print(f"Model file written to {lp_filename}", file=sys.stderr)
                sys.exit(1)  # EXIT_FAILURE equivalent in Python

            # Print the new objective value
            print(f"Solved MP. Cost: {self.model.objVal}")

            iteration += 1

        # Record the end time and calculate total runtime
        end = time.time()
        runtime = end - start
        print("\n\n\n=======================================================")
        print("==================== Problem solved ===================")
        print("=======================================================")
        print(f"Time taken: {runtime:.3f} seconds")

        # Visualizing the final result
        dual_bound = self.model.objVal  # Record the objective value to compare the difference
        result_variables = self.model.getVars()  # Get all variables from the model

        print("\n=== Final active routes ===")
        for var in result_variables:
            result_var_value = var.X  # Get the value of the variable
            if result_var_value > 1e-6:
                print(f"\t{var.VarName}({result_var_value})")  # Assumes Route class has __str__ or __repr__

        # Comparing the difference between binary solution and continuous relaxation
        for var in result_variables:
            var.VType = GRB.BINARY  # Set variable type to binary

        self.model.update()
        self.model.optimize()
        primal_bound = self.model.objVal
        result_variables = self.model.getVars()  # Get all variables from the model

        print("\n=== The integer solution ===")
        for var in result_variables:
            result_var_value = var.X  # Get the value of the variable
            if result_var_value > 1e-6:
                print(f"\t{var.VarName}({result_var_value})")  # Assumes Route class has __str__ or __repr__


        print(f"\nPrimal_bound = {primal_bound}")
        print(f"Dual_bound = {dual_bound}")
        gap = (primal_bound - dual_bound) / primal_bound if primal_bound != 0 else 0
        print(f"Gap = {gap}")
        columns_generated = self.model.NumVars - self.graph.n_customers()
        print(f"Columns generated: {columns_generated}")
        print(f"Iterations run: {iteration}")

