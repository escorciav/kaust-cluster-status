from cluster import gpu_avail

GPU_FILTER = ',gpu'
ADD_NGPU = True


def main():
    gpus = gpu_avail(gpu_filter=GPU_FILTER, add_ngpu=ADD_NGPU)
    print(gpus)


if __name__ == '__main__':
    main()

