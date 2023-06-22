#!/usr/bin/env python

import sys
import numpy as np
import io, os, sys
import time
import argparse
from mpi4py import MPI

def parse_args():
    parser = argparse.ArgumentParser(description='Exalearn_miniapp_training')
    parser.add_argument('--num_epochs', type=int, default=30, metavar='N',
                        help='number of epochs to train (default: 30)')
    parser.add_argument('--device', default='cpu',
                        help='Wheter this is running on cpu or gpu, currently does not support GPU')
    parser.add_argument('--phase', type=int, default=0,
                        help='the current phase of workflow, phase0 will not read model')
    parser.add_argument('--data_root_dir', default='./',
                        help='the root dir of gsas output data')
    parser.add_argument('--model_dir', default='./',
                        help='the directory where save and load model')
    parser.add_argument('--mat_size', type=int, default=3000,
                        help='the matrix with have size of mat_size * mat_size')
    parser.add_argument('--num_mult', type=int, default=10,
                        help='number of matrix mult to perform, need to be larger than num_worker!')
    parser.add_argument('--sim_rank', type=int, default=1,
                        help='number of rank used for simulation. This is needed to determine the size of data in those files')
    parser.add_argument('--preprocess_time', type=float, default=5.0,
                        help='time for doing preprocess')

    args = parser.parse_args()

    return args

def load_data(args, rank):
    root_path = args.data_root_dir + '/phase{}'.format(args.phase) + '/'
    msz = args.mat_size
    X_scaled = np.load(root_path + 'all_X_data_rank_0.npy')
    y_scaled = np.load(root_path + 'all_Y_data_rank_0.npy')
    tile_time = (args.num_mult + args.sim_rank - 1 - rank) // args.sim_rank
    X = np.tile(X_scaled, (tile_time, 1, 1))
    y = np.tile(y_scaled, (tile_time, 1, 1))
    print(X.shape, y.shape)
    return X, y

def preprocess(seconds):
    time.sleep(seconds)


def main():

    start_time = time.time()
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    args = parse_args()
    if rank == 0:
        print(args)

    X, y = load_data(args)
    X = np.float32(X)
    y = np.float32(y)
    preprocess(args.preprocess_time)
    for epoch in range(args.num_epochs):
        tt = time.time()
        for index, mi in enumerate(range(rank, args.num_mult, args.sim_rank)):
            R_temp=np.matmul(X[index], y[index])
        print("Rank is {}, epoch is {}, mult takes {}".format(rank, epoch, time.time() - tt))
        tt = time.time()
        R = np.zeros_like(R_temp)
        comm.Allreduce(R_temp, R, op=MPI.SUM)
        print("Rank is {}, epoch is {}, allreduce takes {}".format(rank, epoch, time.time() - tt))

    if rank == 0:
        with open(args.model_dir + '/result_phase{}.npy'.format(args.phase), 'wb') as f:
            np.save(f, R)

    end_time = time.time()
    print("Rank is {}, total running time is {}) seconds".format(rank, end_time - start_time))

if __name__ == '__main__':
    main()
