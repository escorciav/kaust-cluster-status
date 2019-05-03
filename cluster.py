import subprocess

import pandas as pd


def parse_slurm_line(x, strip=True, add_ngpu=True):
    """Split info from slurm and (optionally) add GPU

    TODO:
        PR to get rid of this in favor of other SLURM command is welcome.
    """
    ind_slice = slice(1, None)
    if strip:
        ind_slice = slice(1, -1)

    data = x[ind_slice].split(' ')
    # Non-generalizable depends on your SLURM config
    # GPUs must be set as SLURM-GRES.
    # Need small patch if you manage other resources with GRES.
    if add_ngpu:
        gpu_data = data[-1]
        # Sanitize: remove " or ' added by users
        gpu_data = gpu_data.replace("'", '')
        gpu_data = gpu_data.replace('"', '')
        num_gpus = 1
        gpu_name = 'null'
        if ':' in gpu_data:
            seq_gpu_data = gpu_data.split(':')
            if len(seq_gpu_data) == 2:
                _, num_gpus = seq_gpu_data
                # in case someone request `gpu:gpu_name`
                if not int_as_str(num_gpus):
                    num_gpus = '1'
            else:
                _, gpu_name, num_gpus = seq_gpu_data
            num_gpus = int(num_gpus)
        data.extend([num_gpus, gpu_name])
    return data


def cluster_info(gpu_filter=None, add_ngpu=True):
    """Info about nodes in the cluster

    Grab info with `sinfo -o "%n %A %D %P %T %c %z %m %d %w %f %G"`,
    Then form a list of list with the following info per node:
        TODO

    """
    cmd = ['sinfo', '-o', '"%n %A %D %P %T %c %z %m %d %w %f %G"']
    cmd_status = subprocess.run(cmd, stdout=subprocess.PIPE,
                                universal_newlines=True)
    data = cmd_status.stdout.split('\n')[:-1]
    data_keys, data_values = data[0], data[1::]

    keys = parse_slurm_line(data_keys, add_ngpu=False)
    feat_ind = -2
    if add_ngpu:
        keys += ['NUM_GPUS', 'GPU_NAME']
        feat_ind -= 2
    values = []
    for i in data_values:
        data = parse_slurm_line(i, add_ngpu=add_ngpu)
        if gpu_filter is None:
            values.append(data)
        elif gpu_filter in data[feat_ind]:
            values.append(data)

    table = pd.DataFrame(values, columns=keys)
    return table


def queue_status(add_ngpu=True):
    """Status of the queue

    Grab info with `squeue -o "%u %i %t %N %b"`,
    Then form a list of list with the following info per node:
        TODO

    """
    cmd = ['squeue', '-o', '"%u %i %t %N %b"']
    cmd_status = subprocess.run(cmd, stdout=subprocess.PIPE,
                                universal_newlines=True)
    data = cmd_status.stdout.split('\n')[:-1]
    data_keys, data_values = data[0], data[1::]

    # TODO: fix based on output
    values = [parse_slurm_line(i, strip=False, add_ngpu=add_ngpu)
              for i in data_values]
    keys = parse_slurm_line(data_keys, add_ngpu=False)
    if add_ngpu:
        keys += ['NUM_GPUS', 'GPU_NAME']
    table = pd.DataFrame(values, columns=keys)
    return table


def gpu_avail(verbose=True, gpu_filter='', add_ngpu=True):
    "Utility to return a pandas-table with gpu available per node"
    queue = queue_status(add_ngpu=add_ngpu)
    ind_running = queue['ST'] == 'R'
    running_jobs = queue.loc[ind_running, :]
    running_jobs_gbn = running_jobs.groupby('NODELIST')
    node_info = cluster_info(gpu_filter=gpu_filter, add_ngpu=add_ngpu)
    node_info.set_index('HOSTNAMES', inplace=True)
    if verbose:
        print('HOSTNAMES GPUs(USED/TOTAL)')
        fmt = '{} {}/{}'

    for node, group in running_jobs_gbn:
        if node not in node_info.index:
            continue

        if verbose:
            print(fmt.format(node,
                             group.loc[:, 'NUM_GPUS'].sum(),
                             node_info.loc[node, 'NUM_GPUS']))
        node_info.loc[node, 'NUM_GPUS'] -= group.loc[:, 'NUM_GPUS'].sum()

    if verbose:
        print()
    return node_info.loc[:, ['NUM_GPUS', 'GPU_NAME']]


def gpu_status(verbose=True, gpu_filter='', add_ngpu=True):
    "Utility to return a pandas-table with gpu consumption per node"
    queue = queue_status(add_ngpu=add_ngpu)
    ind_running = queue['ST'] == 'R'
    running_jobs = queue.loc[ind_running, :]
    running_jobs_gbn = running_jobs.groupby('NODELIST')
    node_info = cluster_info(gpu_filter=gpu_filter, add_ngpu=add_ngpu)
    node_info.set_index('HOSTNAMES', inplace=True)

    used_gpus = []
    indices = []
    for node, group in running_jobs_gbn:
        if node not in node_info.index:
            continue
        used_gpus.append(group.loc[:, 'NUM_GPUS'].sum())
        indices.append(node)
    node_info['USED_GPUS'] = pd.Series(used_gpus, index=indices)

    return node_info.loc[:, ['GPU_NAME', 'USED_GPUS', 'NUM_GPUS']]


def int_as_str(s):
    "return True if string is integer"
    try:
        int(s)
        return True
    except ValueError:
        return False
