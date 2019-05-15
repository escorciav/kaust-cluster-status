This project aims to display the GPUs available in Ibex and IVUL cluster.

This was born as a solo project to greedily&manually pick the best cluster to run experiments.

## Usage

Requirements: python-3, pandas

1. Login to the cluster of interest (ibex/skynet) and run

2. Launch servers

    1. @skynet

        ```bash
        conda activate cluster_status
        FLASK_PORT=5000; FLASK_APP=server.py flask run --port=$FLASK_PORT
        ```

    1. @ibex `python gdragon.py`

3. (Optional) Make server accessible if ports are blocked

    Should be as simple as `ssh -vR 8000:localhost:5000 [user-name]@[server]`

## Setup

1. [Install miniconda or anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html#installing-on-linux).

    > Skip this step if you already have

1. Create the environment

    `conda env create -f environment-x86_64.yml`

That's all. Don't forget to activate the environment before running any program.

`conda activate cluster-status`

## Documentation

### Cluster info

Grab info about nodes

`sinfo -o "%n %A %D %P %T %c %z %m %d %w %f %G"`

### Available GPUs

Behind scenes combines [cluster info](#Cluster-info) and `squeue -o "%u %i %t %b %N"`

## Extras

1. Show reservation

  `scontrol show reservation | grep -A 3 GROUP_IVUL`

2. List node info

  `scontrol -o show node`

## TODO - Help wanted

Implement the feats described in issues #9, #5 .

- Get users

  `sacctmgr list users --noheader format=User%-20`

- Get gres list

  `scontrol show config | grep -e "GresTypes"`

- Get partitions list

  `scontrol show partitions | grep PartitionName`

- List of unaveilable nodes

  `sinfo -N --states=DOWN,DRAIN,DRAINED,DRAINING -o \"%N\" --noheader`

- List of nodes or nodes in given partition

  `sinfo -h -o %n`

  `sinfo -h -p $partition_list -o %n`

- Extract computer info

  `scontrol show nodes --oneliner --detail | sed 's/\\s/\\n/g' | grep -e "NodeName=" -e "Gres=" -e "GresUsed" -e "CfgTRES=" -e "AllocTRES=" -e "Partitions="`

- List jobs

  `scontrol show jobs --oneliner --detail | grep "JobState=RUNNING" | sed 's/\\s/\\n/g' | grep -e "JobId" -e "NumNodes" -e "ArrayJobId" -e "ArrayTaskId" -e "JobName" -e "UserId" -e "StartTime" -e "Partition" -e "^Nodes=" -e "CPU_IDs" -e "Mem=" -e "Gres=" -e "TRES=" -e "TresPerNode="`

  Tested in ibex. `Gres` did not work instead @escorciav found `TresPerNode` or `GRES_IDX`.

Credits to [situpf](https://github.com/situpf/smem)
