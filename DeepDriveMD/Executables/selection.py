#!/usr/bin/env python

import os, sys, socket
import time
import argparse
import kernel as wf

def parse_args():
    parser = argparse.ArgumentParser(description='Exalearn_miniapp_simulation')
    parser.add_argument('--phase', type=int, default=0,
                        help='the current phase of workflow, in miniapp all phases do the same thing except rng')
    parser.add_argument('--mat_size', type=int, default=5000,
                        help='the matrix with have size of mat_size * mat_size')
    parser.add_argument('--data_root_dir', default='./',
                        help='the root dir of gsas output data')
    parser.add_argument('--write_size', type=int, default=3500000,
                        help='size of bytes written to disk, -1 means write data to disk once')
    parser.add_argument('--read_size', type=int, default=6000000,
                        help='size of bytes read from disk')

    args = parser.parse_args()

    return args

def main():

    print("Temp for Darshan, selection, PID = {}, hostname = {}".format(os.getpid(), socket.gethostname()))
    start_time = time.time()

    args = parse_args()
    print(args)

    wf.readNonMPI(args.read_size)
    wf.writeNonMPI(args.write_size)

    end_time = time.time()
    print("Total running time is {} seconds".format(end_time - start_time))

if __name__ == '__main__':
    main()

