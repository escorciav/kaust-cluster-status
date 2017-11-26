# Documentation

## Cluster info

Grab info about nodes

Behind scene: `sinfo -o "%n %A %D %P %T %c %z %m %d %w %f %G"`

## Available GPUs

Behind scenes combines cluster info with `squeue -o "%u %i %t %b %N"`
