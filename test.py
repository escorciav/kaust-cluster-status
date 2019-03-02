from flask import Flask, render_template
from random import randint
app = Flask(__name__)


@app.route('/')
def hello():
    gpus = ['titan-x', 'titan-xp', 'k5000', 'tesla']
    nodes = [
        {
            'name': f'node_{i + 1}',
            'gpu': gpus[randint(0, len(gpus) - 1)],
            'used': randint(0, 4),
            'count': 4,
        }
        for i in range(100)
    ]
    return render_template('avail_gpu.html', cluster='Skeynet', num_nodes=len(nodes), nodes=nodes)
