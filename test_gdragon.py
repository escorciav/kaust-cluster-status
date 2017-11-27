from cluster import cluster_info, queue_status, gpu_avail

GPU_FILTER = ',gpu'
ADD_NGPU = True


def main():
    print(cluster_info(gpu_filter=GPU_FILTER, add_ngpu=ADD_NGPU))
    print(queue_status(add_ngpu=ADD_NGPU))
    print(gpu_avail(gpu_filter=GPU_FILTER, add_ngpu=ADD_NGPU))


if __name__ == '__main__':
    main()

