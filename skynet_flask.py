from flask import Flask, render_template

from cluster import gpu_status

app = Flask(__name__)
GPU_FILTER = None
ADD_NGPU = True


@app.route('/')
def skynet_gpus():
    "Render avil_gpu template with skynet gpu status"
    gpus = gpu_status(gpu_filter=GPU_FILTER, add_ngpu=ADD_NGPU)
    nodes = []
    for hostname, status in gpus.iterrows():
        nodes.append(
            {'name': hostname, 'gpu': status['GPU_NAME'],
             'used': status['USED_GPUS'], 'count': status['NUM_GPUS']}
        )
    return render_template('avail_gpu.html', cluster='Skynet',
                           num_nodes=len(nodes), nodes=nodes)


if __name__ == '__main__':
    from cluster import cluster_info, queue_status, gpu_avail
    print(cluster_info(gpu_filter=GPU_FILTER, add_ngpu=ADD_NGPU))
    print(queue_status(add_ngpu=ADD_NGPU))
    print(gpu_avail(gpu_filter=GPU_FILTER, add_ngpu=ADD_NGPU))
