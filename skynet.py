from cluster import gpu_avail

GPU_FILTER = None
ADD_NGPU = True


def main():
    gpus = gpu_avail(gpu_filter=GPU_FILTER, add_ngpu=ADD_NGPU)
    gpus = gpus.loc[gpus['NUM_GPUS'] > 0, :]
    print(gpus)


if __name__ == '__main__':
    main()

