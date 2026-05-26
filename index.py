from flask import Flask, request, jsonify, render_template
import numpy as np
import re

app = Flask(__name__)

def parse_equations(equations):
    num_eqs = len(equations)
    A = np.zeros((num_eqs, num_eqs))
    b = np.zeros(num_eqs)
    
    for i, eq in enumerate(equations):
        eq = eq.replace(' ', '')
        if '=' not in eq:
            raise ValueError("Missing '=' sign in equation")
        
        lhs, rhs = eq.split('=')
        b[i] = float(rhs)
        
        terms = re.findall(r'([+-]?)(\d*\.?\d*)x_?(\d+)', lhs)
        for sign, coeff_str, var_idx_str in terms:
            sign_val = -1 if sign == '-' else 1
            coeff = float(coeff_str) if coeff_str else 1.0
            col_idx = int(var_idx_str) - 1
            A[i, col_idx] += sign_val * coeff
            
    return A, b

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/jacobi', methods=['POST'])
def jacobi():
    data = request.get_json()
    if not data or 'equations' not in data:
        return jsonify({"error": "Missing equations"}), 400
    
    try:
        equations = [eq for eq in data['equations'].split('\n') if eq.strip()]
        A, b = parse_equations(equations)
    except Exception as e:
        return jsonify({"error": f"Format error: {str(e)}"}), 400

    tol = float(data.get('tol', 1e-6))
    max_iter = int(data.get('max_iter', 100))
    x = np.zeros_like(b, dtype=float)

    D = np.diag(A)
    
    if np.any(D == 0):
        return jsonify({"error": "Zero on diagonal detected"}), 400

    R = A - np.diagflat(D)

    for i in range(max_iter):
        x_new = (b - np.dot(R, x)) / D
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return jsonify({
                "solution": x_new.tolist(),
                "iterations": i+1,
                "converged": True
            })
        x = x_new
        
    return jsonify({
        "solution": x.tolist(),
        "iterations": max_iter,
        "converged": False
    })

if __name__ == '__main__':
    app.run()