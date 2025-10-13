import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="Dynamic Math Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Define Constants ---
X = sp.symbols('x')
DEFAULT_FUNCTION_F = "x**2 - 2" # Updated default for clarity
DEFAULT_FUNCTION_G = "x + 1"

# --- Logic to Generate Step-by-Step Procedures ---
def get_procedure(op, expr_f, expr_g=None):
    """
    Generates tailored procedural steps based on the operation and function type.
    """
    
    # Determine the expression for primary analysis and its name
    if 'g(x)' in op and 'BOTH' not in op:
        expr = expr_g
        function_name = 'g(x)'
    else:
        expr = expr_f
        function_name = 'f(x)'

    if expr is None:
        return f"### Procedural Steps\n**Error:** Function {function_name} is required for this operation but is not defined."

    # Check for characteristics of the determined expression
    is_poly = expr.is_polynomial(X)
    is_trig = any(isinstance(arg, (sp.sin, sp.cos, sp.tan, sp.cot, sp.sec, sp.csc)) for arg in sp.preorder_traversal(expr))
    
    procedure = "### Procedural Steps\n"

    if op == "Find Intersection ($f(x) = g(x)$)":
        procedure += "The goal is to find the values of $x$ where $f(x) = g(x)$.\n"
        procedure += "1. **Set Up:** Form a new equation by setting the two functions equal: $f(x) - g(x) = 0$.\n"
        procedure += "2. **Solve:** Solve the resulting equation for $x$. If the resulting equation is a polynomial, use the appropriate formula (e.g., quadratic formula).\n"
        procedure += "3. **Verify:** Check the solutions by plugging them back into both $f(x)$ and $g(x)$ to ensure they yield the same value."

    elif op in ["Find Roots (of f(x))", "Find Roots (of g(x))"]:
        procedure += f"The goal is to find values of $x$ for which ${function_name}=0$.\n"
        if is_poly:
            procedure += "1. **Identify Type:** Since this is a polynomial, check the degree. For degree 2 (quadratic), use the Quadratic Formula. For higher degrees, look for rational roots or factorization.\n"
            procedure += "2. **Algebraic Manipulation:** Isolate the variable $x$ or use factoring techniques.\n"
        else:
            procedure += "1. **Numerical Approximation:** For complex transcendental functions, algebraic isolation is often impossible. Numerical methods (like Newton's method) are required.\n"
            procedure += "2. **Graphical Check:** The roots are visible as the points where the function's plot crosses the X-axis."
            
    elif op.startswith("Differentiation"):
        target = "each function" if "BOTH" in op else function_name
        procedure += f"This requires applying the rules of differentiation to {target}.\n"
        
        if "BOTH" in op:
            procedure += "1. **Individual Differentiation:** Apply differentiation rules separately to $f(x)$ and $g(x)$ to find $f'(x)$ and $g'(x)$.\n"
        
        if is_poly:
            procedure += "2. **Power Rule:** Apply $\\frac{d}{dx}x^n = nx^{n-1}$ to polynomial terms.\n"
            procedure += "3. **Sum/Difference Rule:** Differentiate each term separately.\n"
        elif is_trig:
            procedure += "2. **Standard Rules:** Use the known derivatives (e.g., $\\frac{d}{dx}\\sin(x)=\\cos(x)$).\n"
            procedure += "3. **Chain Rule:** If the argument is complex (e.g., $\\sin(x^2)$), use the Chain Rule: $f'(g(x)) \\cdot g'(x)$.\n"
        else:
            procedure += "2. **Product/Quotient Rule:** Determine if the function is a product or quotient of two simpler functions.\n3. **Chain Rule:** Check for nested functions where the Chain Rule must be applied iteratively."

    elif op.startswith("Indefinite Integration"):
        target = "each function" if "BOTH" in op else function_name
        procedure += f"This finds the antiderivative $F(x)$ such that $F'(x) = {target}$.\n"
        
        if "BOTH" in op:
            procedure += "1. **Individual Integration:** Apply integration rules separately to $f(x)$ and $g(x)$ to find $\\int f(x) dx$ and $\\int g(x) dx$.\n"

        if is_poly:
            procedure += "2. **Reverse Power Rule:** Apply $\\int x^n dx = \\frac{1}{n+1}x^{n+1}$ (for $n \\neq -1$) to polynomial terms.\n"
            procedure += "3. **Sum Rule:** Integrate each term separately.\n"
            procedure += "4. **Add Constant:** Always include the constant of integration, $+C$, at the end."
        elif is_trig:
            procedure += "2. **Standard Integrals:** Use known integral rules (e.g., $\\int\\cos(x)dx = \\sin(x)$).\n"
            procedure += "3. **Substitution:** Often requires $u$-substitution to simplify the integrand.\n"
            procedure += "4. **Add Constant:** Always include the constant of integration, $+C$."
    
    elif op == "Plot Functions (f(x) and g(x))":
        procedure += "The procedure involves visualizing the function's behavior across the defined domain.\n"
        procedure += "1. **Define Domain:** Choose the $x_{min}$ and $x_{max}$ values.\n2. **Calculate Points:** Compute $f(x)$ and $g(x)$ for many points within the domain.\n3. **Plot:** Connect the points to visualize the curves, identifying intercepts, extrema, and asymptotes."

    return procedure

# --- Main App Title and Inputs ---
st.title("🧮 Dynamic Equation Solver & Interactive Plotter")
st.markdown("Define your functions using standard operators. The app provides comprehensive analysis for $f(x)$ and $g(x)$.")

# --- Sidebar Inputs for Function and Range ---
with st.sidebar:
    st.header("Function Input")
    
    # Function 1: f(x)
    function_str_f = st.text_input(
        "Enter Function f(x)",
        value=DEFAULT_FUNCTION_F,
        help="Example: x**3 + 2*x, exp(-x)*cos(x). This is the primary function for calculus."
    )
    
    # Function 2: g(x)
    function_str_g = st.text_input(
        "Enter Function g(x) (Optional)",
        value=DEFAULT_FUNCTION_G,
        help="Example: 2*x + 1. Required for intersection, g(x) roots/calculus, and dual plots."
    )
    
    # Variable Name (Usually x, but can be customized)
    variable_str = st.text_input(
        "Variable Name",
        value="x",
        max_chars=1
    )

    st.header("Analysis and Plot Range")
    
    # Select Operation - Now with individual and combined options
    operation = st.selectbox(
        "Select Mathematical Operation",
        [
            "Plot Functions (f(x) and g(x))", 
            "Find Intersection ($f(x) = g(x)$)",
            "Find Roots (of f(x))", 
            "Find Roots (of g(x))",
            "Differentiation (d/dx of f(x))", 
            "Differentiation (d/dx of g(x))",
            "Differentiation (d/dx of BOTH functions)",
            "Indefinite Integration (of f(x))",
            "Indefinite Integration (of g(x))",
            "Indefinite Integration (of BOTH functions)"
        ]
    )
    
    # Plot Range
    col_min, col_max = st.columns(2)
    with col_min:
        x_min = st.number_input("Min X", value=-5.0, step=0.5)
    with col_max:
        x_max = st.number_input("Max X", value=5.0, step=0.5)

# --- Core Processing Logic ---

def process_function(func_str_f, func_str_g, op, x_min, x_max):
    
    if x_min >= x_max:
        st.error("Error: Minimum X must be less than Maximum X.")
        return

    try:
        # 1. Convert user strings to SymPy expressions
        expr_f = sp.sympify(func_str_f)
        expr_g = sp.sympify(func_str_g) if func_str_g else None
        
        result_text = ""
        # List of expressions to plot: [{'expr': expr, 'name': 'f(x)', 'color': '...', 'dash': '...'}]
        result_exprs_to_plot = [] 
        
        # Determine target expression for single analysis operations
        is_g_op = 'g(x)' in op and 'BOTH' not in op
        target_expr = expr_g if is_g_op else expr_f
        target_name = 'g(x)' if is_g_op else 'f(x)'

        # Check for missing g(x) where required
        if expr_g is None and ('g(x)' in op or 'Intersection' in op or 'BOTH' in op):
             st.warning(f"Please enter a function for g(x) to perform the '{op}' operation.")
             return

        # 2. Perform the selected operation
        
        # --- Multi-Function Plotting ---
        if op == "Plot Functions (f(x) and g(x))":
            result_text = f"**Functions:** $f(x) = {sp.latex(expr_f)}$ and $g(x) = {sp.latex(expr_g)}$"
            result_exprs_to_plot.append({'expr': expr_f, 'name': 'f(x)', 'color': '#10b981', 'dash': 'solid'})
            result_exprs_to_plot.append({'expr': expr_g, 'name': 'g(x)', 'color': '#f59e0b', 'dash': 'solid'})
                
        # --- Intersection / Solving $f(x) = g(x)$ ---
        elif op == "Find Intersection ($f(x) = g(x)$)":
            intersection_equation = expr_f - expr_g
            intersections = sp.solve(intersection_equation, X)
            real_intersections = [r for r in intersections if sp.re(r) == r]
            
            if real_intersections:
                result_text = f"**Intersections:** Solutions for $f(x) = g(x)$ are: "
                result_text += ", ".join([f"$x = {sp.latex(root)}$" for root in real_intersections])
                y_values = [expr_f.subs(X, root) for root in real_intersections if root.is_real]
                if y_values:
                    # Display the first point coordinate for brevity
                    result_text += f"<br>Example point: $( {sp.latex(real_intersections[0])}, {sp.latex(y_values[0])} )$"
            else:
                result_text = "No simple real intersections found symbolically."
            
            # Plot both original functions to visualize intersection
            result_exprs_to_plot.append({'expr': expr_f, 'name': 'f(x)', 'color': '#10b981', 'dash': 'solid'})
            result_exprs_to_plot.append({'expr': expr_g, 'name': 'g(x)', 'color': '#f59e0b', 'dash': 'solid'})
        
        # --- Root Finding Operations ---
        elif 'Find Roots' in op:
            roots = sp.solve(target_expr, X)
            real_roots = [r for r in roots if sp.re(r) == r]
            if real_roots:
                result_text = f"**Roots of ${target_name}$:** Solutions for ${target_name}=0$ are: "
                result_text += ", ".join([f"$x = {sp.latex(root)}$" for root in real_roots])
            else:
                result_text = f"No simple real roots found symbolically for ${target_name}$."
            
            result_exprs_to_plot.append({'expr': target_expr, 'name': target_name, 'color': '#10b981' if not is_g_op else '#f59e0b', 'dash': 'solid'})
        
        # --- Differentiation Operations ---
        elif 'Differentiation' in op:
            if 'BOTH' in op:
                # Differentiate Both
                result_f_prime = sp.diff(expr_f, X)
                result_g_prime = sp.diff(expr_g, X)
                result_text = f"**Derivative $f'(x)$:** ${sp.latex(result_f_prime)}$<br>**Derivative $g'(x)$:** ${sp.latex(result_g_prime)}$"
                
                result_exprs_to_plot.append({'expr': result_f_prime, 'name': 'f\'(x)', 'color': '#3b82f6', 'dash': 'solid'})
                result_exprs_to_plot.append({'expr': result_g_prime, 'name': 'g\'(x)', 'color': '#ef4444', 'dash': 'dash'})
            else:
                # Differentiate f(x) or g(x)
                result_prime = sp.diff(target_expr, X)
                result_text = f"**Derivative ${target_name}'$:** $\\frac{{d}}{{d{variable_str}}} ({sp.latex(target_expr)}) = {sp.latex(result_prime)}$"
                
                result_exprs_to_plot.append({'expr': target_expr, 'name': target_name, 'color': '#10b981' if not is_g_op else '#f59e0b', 'dash': 'dot'})
                result_exprs_to_plot.append({'expr': result_prime, 'name': f'{target_name}\' (Derivative)', 'color': '#3b82f6' if not is_g_op else '#ef4444', 'dash': 'solid'})

        # --- Integration Operations ---
        elif 'Indefinite Integration' in op:
            if 'BOTH' in op:
                # Integrate Both
                result_f_int = sp.integrate(expr_f, X)
                result_g_int = sp.integrate(expr_g, X)
                result_text = f"**Integral $\int f(x) dx$:** ${sp.latex(result_f_int)} + C_1$<br>**Integral $\int g(x) dx$:** ${sp.latex(result_g_int)} + C_2$"
                
                # Plotting (C=0 assumption)
                plot_f_int = result_f_int.subs({s: 0 for s in result_f_int.free_symbols if s.name.startswith('C')})
                plot_g_int = result_g_int.subs({s: 0 for s in result_g_int.free_symbols if s.name.startswith('C')})

                result_exprs_to_plot.append({'expr': plot_f_int, 'name': 'F(x) (Integral C1=0)', 'color': '#3b82f6', 'dash': 'solid'})
                result_exprs_to_plot.append({'expr': plot_g_int, 'name': 'G(x) (Integral C2=0)', 'color': '#ef4444', 'dash': 'dash'})

            else:
                # Integrate f(x) or g(x)
                result_int = sp.integrate(target_expr, X)
                result_text = f"**Indefinite Integral $\int {target_name} dx$:** ${sp.latex(result_int)} + C$"
                
                # Plotting (C=0 assumption)
                plot_int = result_int.subs({s: 0 for s in result_int.free_symbols if s.name.startswith('C')})
                
                result_exprs_to_plot.append({'expr': target_expr, 'name': target_name, 'color': '#10b981' if not is_g_op else '#f59e0b', 'dash': 'dot'})
                result_exprs_to_plot.append({'expr': plot_int, 'name': f'Integral (C=0)', 'color': '#3b82f6' if not is_g_op else '#ef4444', 'dash': 'solid'})
        
        # 3. Display the Symbolic Result and Procedure side-by-side
        col_res, col_proc = st.columns(2)

        with col_res:
            st.markdown("### Symbolic Result")
            st.write(result_text)

        with col_proc:
            # Pass the function chosen for the procedure to guide the steps
            procedure_expr = expr_g if is_g_op else expr_f
            procedure = get_procedure(op, procedure_expr, expr_g)
            st.markdown(procedure)

        # 4. Plotting Setup
        st.markdown("### Interactive Plot")
        
        fig = go.Figure()
        x_vals = np.linspace(x_min, x_max, 500)

        # Plot all required expressions
        for plot_data in result_exprs_to_plot:
            plot_expr = plot_data['expr']
            plot_name = plot_data['name']
            
            f_numerical = sp.lambdify(X, plot_expr, 'numpy')
            y_vals = f_numerical(x_vals)
            
            fig.add_trace(go.Scatter(
                x=x_vals, y=y_vals,
                mode='lines',
                # Ensure long expressions fit by only showing the short name in the legend
                name=plot_name, 
                line=dict(color=plot_data['color'], width=3, dash=plot_data['dash']),
                # Show full expression on hover
                hovertemplate=f'{plot_name}: %{{y}}<br>x: %{{x}}<extra>{sp.latex(plot_expr)}</extra>'
            ))
            
        # Add interactivity features
        fig.add_hline(y=0, line_dash="dot", line_color="gray", opacity=0.7)
        fig.update_layout(
            title={'text': f"Plot for {op}", 'x':0.5, 'xanchor': 'center'},
            xaxis_title=f"Variable ${variable_str}$",
            yaxis_title="Value",
            hovermode="x unified",
            margin=dict(l=20, r=20, t=60, b=20),
            template="plotly_white",
            height=550
        )
        
        st.plotly_chart(fig, use_container_width=True)

    except sp.SympifyError:
        st.error(f"Invalid mathematical syntax. Please ensure your functions are correctly formatted (e.g., `2*x**2 + 3` or `log(x)`).")
    except Exception as e:
        st.error(f"An unexpected error occurred during processing: {e}")

# Run the function if inputs are ready
if function_str_f:
    process_function(function_str_f, function_str_g, operation, x_min, x_max)
else:
    st.info("Please enter a mathematical function in the sidebar to begin the analysis.")
