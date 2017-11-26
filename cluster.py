import subprocess

import pandas as pd


def parse_slurm_line(x, strip=True, add_gpu=True):
    ind_slice = slice(0, None)
    if strip:
        ind_slice = slice(1, -1)

    data = x[ind_slice].split(' ')
    if add_gpu:
        # cluter specific
        gpu_data = data[-1]
        num_gpus = int(gpu_data.split(':')[-1])
        data.append(num_gpus)

    return data


def cluster_info():
    """Info about nodes in the cluster"""
    cmd = ['sinfo', '-o', '"%n %A %D %P %T %c %z %m %d %w %f %G"']
    cmd_status = subprocess.run(cmd, stdout=subprocess.PIPE,
                                universal_newlines=True)
    data = cmd_status.stdout.split('\n')[:-1]
    data_keys, data_values = data[0], data[1::]

    values = [parse_slurm_line(i) for i in data_values]
    keys = parse_slurm_line(data_keys, add_gpu=False) + ['NUM_GPUS']
    table = pd.DataFrame(values, columns=keys)
    return table


def queue_status():
    """Status of the Queue"""
    cmd = ['squeue', '-o', '"%u %i %t %N %b"']
    cmd_status = subprocess.run(cmd, stdout=subprocess.PIPE,
                                universal_newlines=True)
    data = cmd_status.stdout.split('\n')[:-1]
    data_keys, data_values = data[0], data[1::]

    # TODO: fix based on output
    values = [parse_slurm_line(i) for i in data_values]
    keys = parse_slurm_line(data_keys, add_gpu=False) + ['NUM_GPUS']
    table = pd.DataFrame(values, columns=keys)
    return table


def gpu_avail(verbose=True):
    queue = queue_status()
    ind_running = queue['ST'] == 'R'
    running_jobs = queue.loc[ind_running, :]
    running_jobs_gbn = running_jobs.groupby('NODELIST')
    node_info = cluster_info()
    node_info.set_index('HOSTNAMES', inplace=True)
    if verbose:
        print('HOSTNAMES GPUs(USED/TOTAL)')
        fmt = '{} {}/{}'

    for node, group in running_jobs_gbn:
        if verbose:
            print(fmt.format(node,
                             group.loc[:, 'NUM_GPUS'].sum(),
                             node_info.loc[node, 'NUM_GPUS']))
        node_info.loc[node, 'NUM_GPUS'] -= group.loc[:, 'NUM_GPUS'].sum()

    if verbose:
        print()
    return node_info.loc[:, ['NUM_GPUS']]


if __name__ == '__main__':
    cluster_info()
    print(queue_status())
    print()
    print(gpu_avail())

