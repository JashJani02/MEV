# Mathematical Equation Visualizer (MEV)

A powerful, interactive web application for symbolic math analysis and function visualization — built with Python, Streamlit, and Plotly.

---

## Project Structure

```
MEV/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## Features

- Symbolic computation powered by **SymPy**
- Interactive plots powered by **Plotly**
- Step-by-step procedural explanations tailored to function type
- Real-time analysis for two simultaneous functions `f(x)` and `g(x)`
- Supports polynomials, trigonometric, exponential, and logarithmic functions
- Configurable plot range (`x_min` to `x_max`)

---

## Tech Stack

| Technology | Role |
|------------|------|
| **Python** | Core language |
| **Streamlit** | Web UI framework |
| **SymPy** | Symbolic mathematics (CAS) |
| **NumPy** | Numerical computation for plotting |
| **Plotly** | Interactive graph rendering |

---

### Installation

```bash
# Clone the repository
git clone https://github.com/JashJani02/MEV.git
cd MEV

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Dependencies (`requirements.txt`)

```
streamlit
sympy
numpy
plotly
```



---

## Supported Operations

| Operation | Description |
|-----------|-------------|
| **Plot Functions** | Visualizes both `f(x)` and `g(x)` on the same interactive graph |
| **Find Intersection** | Solves `f(x) = g(x)` symbolically and displays intersection points |
| **Find Roots of f(x)** | Solves `f(x) = 0` for real roots |
| **Find Roots of g(x)** | Solves `g(x) = 0` for real roots |
| **Differentiation of f(x)** | Computes `f'(x)` and plots it alongside the original |
| **Differentiation of g(x)** | Computes `g'(x)` and plots it alongside the original |
| **Differentiation of BOTH** | Computes and plots `f'(x)` and `g'(x)` simultaneously |
| **Indefinite Integration of f(x)** | Computes `∫f(x)dx` and plots the antiderivative (C = 0) |
| **Indefinite Integration of g(x)** | Computes `∫g(x)dx` and plots the antiderivative (C = 0) |
| **Indefinite Integration of BOTH** | Computes and plots both antiderivatives simultaneously |

---

## Functions & Methods Reference

### `get_procedure(op, expr_f, expr_g=None)`

Generates human-readable, step-by-step procedural instructions tailored to the selected operation and the type of function provided.

| Parameter | Type | Description |
|-----------|------|-------------|
| `op` | `str` | The selected mathematical operation (e.g., `"Differentiation (d/dx of f(x))"`) |
| `expr_f` | `sympy.Expr` | The primary SymPy expression for `f(x)` |
| `expr_g` | `sympy.Expr` or `None` | Optional SymPy expression for `g(x)` |
| **Returns** | `str` | A Markdown-formatted string containing numbered procedural steps |

**Behavior by operation:**

| Operation | Key Logic |
|-----------|-----------|
| Intersection | Explains setting up and solving `f(x) - g(x) = 0` |
| Root Finding | Adapts steps based on whether the expression is polynomial or transcendental |
| Differentiation | Applies Power Rule, Chain Rule, or Product/Quotient Rule based on function type |
| Integration | Applies Reverse Power Rule, substitution, or standard integrals based on function type |
| Plotting | Describes domain definition and point computation |

---

### `process_function(func_str_f, func_str_g, op, x_min, x_max)`

The main processing pipeline. Parses user input, performs the selected symbolic operation, displays results, and renders the interactive Plotly graph.

| Parameter | Type | Description |
|-----------|------|-------------|
| `func_str_f` | `str` | Raw string input for `f(x)` (e.g., `"x**2 - 2"`) |
| `func_str_g` | `str` | Raw string input for `g(x)` (e.g., `"x + 1"`) |
| `op` | `str` | The selected mathematical operation |
| `x_min` | `float` | Minimum x-value for the plot range |
| `x_max` | `float` | Maximum x-value for the plot range |
| **Returns** | `None` | Renders results and chart directly into the Streamlit UI |

**Internal pipeline steps:**

| Step | Action |
|------|--------|
| 1 | Validates that `x_min < x_max` |
| 2 | Converts string inputs to SymPy expressions via `sp.sympify()` |
| 3 | Determines the target expression (`f(x)` or `g(x)`) based on the selected operation |
| 4 | Executes the symbolic computation (solve, diff, integrate) |
| 5 | Builds a list of expressions to plot, each with name, color, and dash style |
| 6 | Displays the symbolic result and procedural steps in a two-column layout |
| 7 | Renders the interactive Plotly figure with hover support and a zero-line |

**Error handling:**

| Error Type | Handling |
|------------|----------|
| `sp.SympifyError` | Shows a formatted error for invalid math syntax |
| Missing `g(x)` | Shows a warning when an operation requires `g(x)` but it's undefined |
| General exceptions | Caught and displayed via `st.error()` |

---

## UI Layout

| Component | Location | Description |
|-----------|----------|-------------|
| Function inputs (`f(x)`, `g(x)`) | Sidebar | Text inputs for defining the two functions |
| Variable name | Sidebar | Customizable variable (default: `x`) |
| Operation selector | Sidebar | Dropdown with all 10 supported operations |
| Plot range (`x_min`, `x_max`) | Sidebar | Number inputs for the graph domain |
| Symbolic result | Main panel (left column) | LaTeX-rendered output of the computation |
| Procedural steps | Main panel (right column) | Step-by-step mathematical guidance |
| Interactive plot | Main panel (full width) | Plotly chart with hover, zoom, and pan |

---

## Usage Examples

Enter these directly into the `f(x)` or `g(x)` input fields:

| Expression | Input String |
|------------|--------------|
| x² − 2 | `x**2 - 2` |
| sin(x) · e^x | `sin(x) * exp(x)` |
| Natural log of x | `log(x)` |
| √x | `sqrt(x)` |
| 3x³ + 2x − 1 | `3*x**3 + 2*x - 1` |

---
