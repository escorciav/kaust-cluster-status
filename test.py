from flask import Flask, render_template
app = Flask(__name__)

@app.route('/<cluster>/')
def hello(cluster=None):
    nodes = [{'name': 'modar', 'gpu': 'titan', 'used': 0, 'count': 1000}] * 10
    return render_template('avail_gpu.html', num_nodes=len(nodes), nodes=nodes)
