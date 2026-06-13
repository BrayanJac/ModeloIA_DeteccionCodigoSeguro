from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    """Endpoint principal de la aplicación."""
    return jsonify({
        'message': 'API de Demostración para Pipeline CI/CD Seguro con IA',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Endpoint de health check."""
    return jsonify({
        'status': 'healthy'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
