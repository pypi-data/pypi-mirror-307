# This py file defines a parent solver to be inherited to other solvers
from gurobipy import Model, GurobiError, GRB, LinExpr, Column
from typing import List, Dict
from . import cppWrapper
import plotly.graph_objects as go
import plotly.express as px


class Parent_Solver:
    def __init__(self, graph: cppWrapper.Graph):
        """
        Initializes the Solver with a given Graph.
        
        Args:
            graph (cppWrapper.Graph): The VRP graph.
        """
        self.graph: cppWrapper.Graph = graph  # C++ Graph object
        self.sp_solver: cppWrapper.ShortestPathSolver = cppWrapper.ShortestPathSolver(self.graph)  # C++ ShortestPathSolver
        self.routes: List[list] = []  # List to store Route objects
        # self.x: List = []  # List to store Gurobi variables
        self.covering: Dict[int, object] = {}  # Mapping from customer vertex to Gurobi constraint

        # Initialize Gurobi model
        try:
            self.model: Model = Model()
            self.model.setParam('OutputFlag', 0)
            self.model.setParam('LogToConsole', 0)
        except GurobiError as e:
            print(f"Cannot start Gurobi: {str(e)}")
            raise

        # Setting up covering constraints
        for v in self.graph.customers():
            constr_name = f"cover_{v}"
            # Add a covering constraint: sum of x[r] where r covers customer v >= 1
            # Initialize the constraint with 0 (no variables yet)
            self.covering[v] = self.model.addConstr(
                LinExpr(),
                GRB.GREATER_EQUAL,
                1.0,
                name=constr_name
            )

        # Initializing columns (variables) pool with Source->v->Sink routes
        for v in self.graph.customers():
            self.add_route(v)

    def add_route(self, v: int) -> None:
        """
        Adds a route to the model. This method handles routes specified by a list of vertices.

        Args:
            vertices (List[int]): A list of vertex IDs representing the route.
        """
        cost = self.graph.cost(self.graph.departing_depot(), v) + self.graph.cost(v, self.graph.returning_depot())
        try:
            # Create a Gurobi variable for this route
            c = Column()
            c.addTerms(1.0, self.covering[v]) # New constraint to add
            var = self.model.addVar(
                lb=0.0,  # Lower bound
                ub=GRB.INFINITY,  # Upper bound
                obj=cost,  # Objective coefficient
                vtype=GRB.CONTINUOUS,  # Variable type
                name=f"0 {v} {self.graph.returning_depot()}({cost})",
                column = c
            )

            # # Add the variable to the list
            # self.x.append(var)
            self.routes.append([0, v, self.graph.returning_depot()])
        except GurobiError as e:
            print(f"Error adding route: {str(e)}")
            raise




    def add_route_route(self, route: cppWrapper.Route) -> None:
        """
        Adds a Route object to the model.

        Args:
            route (cppWrapper.Route): The route to add.
        """
        try:
            # Associate the variable with covering constraints
            c = Column()
            vec = []
            for v in route.vertices:
                if v != self.graph.departing_depot() and v != self.graph.returning_depot():
                    # Add coefficient 1.0 to the covering constraint for customer v
                    vec.append(self.covering[v])
            c.addTerms([1.0] * len(vec), vec)
            # Create a Gurobi variable for this route
            var = self.model.addVar(
                lb=0.0,  # Lower bound
                ub=GRB.INFINITY,  # Upper bound
                obj=route.cost,  # Objective coefficient
                vtype=GRB.CONTINUOUS,  # Variable type
                name=str(route),
                column = c
            )


            # # Add the variable to the list
            # self.x.append(var)
            self.routes.append(list(route.vertices))
        except GurobiError as e:
            print(f"Error adding route: {str(e)}")
            raise


    def plot_vrp_map(self, x_coords, y_coords):
        """
        Plots a VRP map with departure and return depots highlighted.

        Parameters:
        - x_coords (list of float): X-axis coordinates of the points.
        - y_coords (list of float): Y-axis coordinates of the points.

        Returns:
        - fig (plotly.graph_objects.Figure): The Plotly figure object.
        """
        
        x_coords = list(x_coords)
        y_coords = list(y_coords)
        if not (len(x_coords) == len(y_coords)):
            raise ValueError("x_coords and y_coords must be of the same length.")

        if len(x_coords) < 2:
            raise ValueError("At least two points are required (departure and return depots).")

        # Create a scatter plot for all points
        fig = go.Figure()

        # Plot intermediate points
        if len(x_coords) > 2:
            fig.add_trace(go.Scatter(
                x=x_coords[1:-1],
                y=y_coords[1:-1],
                mode='markers',
                marker=dict(
                    size=10,
                    color='blue',
                    symbol='circle'
                ),
                name='Customers'
            ))

        # Plot departure depot
        fig.add_trace(go.Scatter(
            x=[x_coords[0]],
            y=[y_coords[0]],
            mode='markers',
            marker=dict(
                size=15,
                color='green',
                symbol='triangle-up'
            ),
            name='Departure Depot'
        ))

        # Plot return depot
        fig.add_trace(go.Scatter(
            x=[x_coords[-1]],
            y=[y_coords[-1]],
            mode='markers',
            marker=dict(
                size=15,
                color='red',
                symbol='triangle-down'
            ),
            name='Return Depot'
        ))

        # Update layout for better aesthetics
        fig.update_layout(
            title="VRP Map Visualization",
            xaxis_title="X Coordinate",
            yaxis_title="Y Coordinate",
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255,255,255,0.5)',
                bordercolor='Black',
                borderwidth=1
            ),
            plot_bgcolor='rgba(240,240,240,0.95)',
            width=800,
            height=600
        )

        # Add gridlines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

        # Show the figure
        fig.show()

        return fig
    
    def plot_vrp_routes(self, x_coords, y_coords):
        """
        Plots a VRP map with departure and return depots highlighted and visualizes the routes.

        Parameters:
        - x_coords (list of float): X-axis coordinates of the points.
        - y_coords (list of float): Y-axis coordinates of the points.
        - routes (list of list of int): Each inner list contains indices of vertices representing a route.

        Returns:
        - fig (plotly.graph_objects.Figure): The Plotly figure object with the VRP map and routes.
        """

        x_coords = list(x_coords)
        y_coords = list(y_coords)
        routes = []
        result_variables = self.model.getVars()  # Get all variables from the model
        for i, var in enumerate(result_variables):
            result_var_value = var.X  # Get the value of the variable
            if result_var_value > 1e-6:
                routes.append(self.routes[i])
        starting_depot_index = 0
        ending_depot_index = self.graph.returning_depot()
        # Input Validation
        if not (len(x_coords) == len(y_coords)):
            raise ValueError("x_coords and y_coords must be of the same length.")

        num_vertices = len(x_coords)

        if not (0 <= starting_depot_index < num_vertices):
            raise ValueError(f"starting_depot_index {starting_depot_index} is out of bounds.")

        if not (0 <= ending_depot_index < num_vertices):
            raise ValueError(f"ending_depot_index {ending_depot_index} is out of bounds.")

        if starting_depot_index == ending_depot_index:
            raise ValueError("starting_depot_index and ending_depot_index must be different.")

        # Extract customer indices (exclude depots)
        customer_indices = set(range(num_vertices)) - {starting_depot_index, ending_depot_index}

        # Create a scatter plot for all customers
        customer_x = [x_coords[i] for i in customer_indices]
        customer_y = [y_coords[i] for i in customer_indices]

        fig = go.Figure()

        if customer_x and customer_y:
            fig.add_trace(go.Scatter(
                x=customer_x,
                y=customer_y,
                mode='markers',
                marker=dict(
                    size=10,
                    color='blue',
                    symbol='circle'
                ),
                name='Customers',
                hoverinfo='text+x+y',
                text=[f"Customer {i}" for i in customer_indices]
            ))

        # Plot starting depot
        fig.add_trace(go.Scatter(
            x=[x_coords[starting_depot_index]],
            y=[y_coords[starting_depot_index]],
            mode='markers',
            marker=dict(
                size=15,
                color='green',
                symbol='triangle-up'
            ),
            name='Starting Depot',
            hoverinfo='text+x+y',
            text=[f"Starting Depot {starting_depot_index}"]
        ))

        # Plot ending depot
        fig.add_trace(go.Scatter(
            x=[x_coords[ending_depot_index]],
            y=[y_coords[ending_depot_index]],
            mode='markers',
            marker=dict(
                size=15,
                color='red',
                symbol='triangle-down'
            ),
            name='Ending Depot',
            hoverinfo='text+x+y',
            text=[f"Ending Depot {ending_depot_index}"]
        ))

        # Define a color palette for routes
        colors = px.colors.qualitative.Plotly
        num_colors = len(colors)
        if len(routes) > num_colors:
            # Extend the color palette if needed
            colors = px.colors.qualitative.Dark24
            num_colors = len(colors)

        # Plot each route
        for idx, route in enumerate(routes):
            # Validate route structure
            if len(route) < 2:
                raise ValueError(f"Route {idx + 1} must contain at least two vertices (start and end depots).")

            if route[0] != starting_depot_index:
                raise ValueError(f"Route {idx + 1} does not start with the starting depot index {starting_depot_index}.")

            if route[-1] != ending_depot_index:
                raise ValueError(f"Route {idx + 1} does not end with the ending depot index {ending_depot_index}.")

            # Validate all vertices in the route
            for vertex in route:
                if not (0 <= vertex < num_vertices):
                    raise ValueError(f"Route {idx + 1} contains invalid vertex index {vertex}.")

            # Extract x and y coordinates for the route
            route_x = [x_coords[vertex] for vertex in route]
            route_y = [y_coords[vertex] for vertex in route]

            # Assign a unique color for the route
            color = colors[idx % num_colors]

            # Add the route to the plot
            fig.add_trace(go.Scatter(
                x=route_x,
                y=route_y,
                mode='lines+markers',
                line=dict(
                    color=color,
                    width=2
                ),
                marker=dict(
                    size=8,
                    symbol='circle'
                ),
                name=f'Route {idx + 1}',
                hoverinfo='text+x+y',
                text=[f"Vertex {vertex}" for vertex in route]
            ))

        # Update layout for better aesthetics
        fig.update_layout(
            title="VRP Map Visualization with Routes",
            xaxis_title="X Coordinate",
            yaxis_title="Y Coordinate",
            legend=dict(
                x=0.01,
                y=0.99,
                bgcolor='rgba(255,255,255,0.5)',
                bordercolor='Black',
                borderwidth=1
            ),
            plot_bgcolor='rgba(240,240,240,0.95)',
            width=800,
            height=600
        )

        # Add gridlines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')

        # Show the figure
        fig.show()

        return fig
