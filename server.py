"""server and test

Usage (test changes in cluster.py)
    python server.py [GPU_FILTER]

In case of error pass a GPU_FILTER. skynet does not need one, but ibex requires
",gpu" without quotes

"""
from flask import Flask, render_template

from cluster import gpu_status

app = Flask(__name__)
ADD_NGPU = True


def gpu_consumption(gpu_filter=None):
    "Render avil_gpu template with skynet gpu status"
    gpus = gpu_status(gpu_filter=gpu_filter, add_ngpu=ADD_NGPU)
    nodes = []
    for hostname, status in gpus.iterrows():
        nodes.append(
            {'name': hostname, 'gpu': status['GPU_NAME'],
             'used': status['USED_GPUS'], 'count': status['NUM_GPUS']}
        )
    return nodes


@app.route('/skynet')
def skynet_consumption():
    nodes = gpu_consumption(gpu_filter=None)
    return render_template('avail_gpu.html', cluster='Skynet',
                           num_nodes=len(nodes), nodes=nodes)


@app.route('/ibex')
def ibex_consumption():
    nodes = gpu_consumption(gpu_filter=',gpu')
    return render_template('avail_gpu.html', cluster='Ibex',
                           num_nodes=len(nodes), nodes=nodes)


if __name__ == '__main__':
    import sys
    GPU_FILTER = None
    if len(sys.argv) > 1:
        GPU_FILTER = sys.argv[1]

    from cluster import cluster_info, queue_status, gpu_avail
    print(gpu_avail(gpu_filter=GPU_FILTER, add_ngpu=ADD_NGPU))

    print(cluster_info(gpu_filter=GPU_FILTER, add_ngpu=ADD_NGPU))
    print(queue_status(add_ngpu=ADD_NGPU))
    print(gpu_status(gpu_filter=GPU_FILTER, add_ngpu=ADD_NGPU))
