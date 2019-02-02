This project aims to display the GPUs available in Ibex and IVUL cluster.

This was born as a solo project to greedily&manually pick the best cluster to run experiments.

## Usage

Requirements: python-3, pandas

1. Login to the cluster of interest (ibex/skynet) and run

2. `python gdragon.py`@ibex or `python skynet.py`@skynet.

## Documentation

### Cluster info

Grab info about nodes

`sinfo -o "%n %A %D %P %T %c %z %m %d %w %f %G"`

### Available GPUs

Behind scenes combines [cluster info](#Cluster-info) and `squeue -o "%u %i %t %b %N"`
