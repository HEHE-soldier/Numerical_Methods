from flask import Flask, request, jsonify,render_template
import numpy as np

app = Flask(__name__)

@app.route('/', defaults={'path':''})
@app.route('/<path:path>', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/jacobi', methods=['POST'])
def jacobi():
    data = request.get_json()
    if not data or 'A' not in data or 'b' not in data:
        return jsonify({"error": "Missing matrix A or vector b"}), 400
    
    A = np.array(data['A'], dtype=float)
    b = np.array(data['b'], dtype=float)
    tol = float(data.get('tol', 1e-6))
    max_iter = int(data.get('max_iter', 100))
    n = len(b)
    x = np.zeros_like(b, dtype=float)

    if 'x0' in data:
        x = np.array(data['x0'], dtype=float)

    D = np.diag(A)
    R = A - np.diagflat(D)

    for i in range(max_iter):
        x_new = (b - np.dot(R,x)) / D
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