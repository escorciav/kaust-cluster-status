This project aims to display the GPUs available in Ibex and IVUL cluster.

This was born as a solo project to greedily&manually pick the best cluster to run experiments.

## Usage

Requirements: python-3, pandas

1. Login to the cluster of interest (ibex/skynet) and run

2. Launch servers

  1. @skynet

    ```bash
    conda activate cluster_status
    FLASK_PORT=5000; FLASK_APP=skynet_flask.py flask run --port=$FLASK_PORT
    ```

  1. @ibex `python gdragon.py`

3. (Optional) Expose server with ngrok

  1. Download and logging to [ngrok](https://ngrok.com/)

  1. Re-direct port

      `ngrok http $FLASK_PORT`

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
