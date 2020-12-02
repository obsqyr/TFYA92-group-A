#!/usr/bin/env python3
# Main Molecular dynamics simulation loop
import os
import md
import ase.io
from read_mp_project import read_mp_properties
import numpy as np
from mpi4py import MPI
import io

def supercomputer_init():
    ''' Establish suitable environment for MPI
        parallelization on supercomputer
    '''
    os.environ['OPENLABS_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'
    os.environ['NUMEXPR_NUM_THREADS'] = '1'
    os.environ['OMP_NUM_THREADS'] = '1'
    print('\n Supercomputer init finished')

def main():
    # don't allow Python libraries to start spanning threads
    # over the available cores
    supercomputer_init()

    # set up variables for parallelization
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    # read in the .json file as an command line argument?
    mp_properties = read_mp_properties('test_120_materials.json')

    # create one list of all atom objects in data-file
    atoms_list = []
    for cif in mp_properties['cif']:
        f = open('tmp'+str(rank)+'.cif', 'w+')
        f.write(cif)
        f.close()
        atoms = ase.io.read('tmp'+str(rank)+'.cif', None)
        atoms_list.append(atoms)
    print("Created atoms list")
    os.remove('tmp'+str(rank)+'.cif')
   
    # Run the molecular dynamics in parallell (might want to
    # improve it)
    if rank == 0:
        jobs = np.arange(0, len(atoms_list), dtype=np.int)
        job_array = np.array_split(jobs, size)
        #print("we have", size, " processes.")
        for i in range(0, size):
            comm.isend(len(job_array[i]), dest=i, tag=i)
            comm.Isend([job_array[i], MPI.INT], dest=i, tag=i)

    # how do I send in the correct atoms-object to md_run?
    l = comm.recv(source=0, tag=rank)
    data = np.ones(l, dtype=np.int)
    comm.Recv([data, MPI.INT], source=0, tag=rank)
    for id in data:
        #print("ID: ", id)
        #print(atoms)
        md.run_md(atoms_list[id], str(id))
    comm.Barrier()
        

    '''
    try:
        for id, atoms in enumerate(atoms_list):
            print("\n \n \nRUNNING MOLECULAR DYNAMICS")
            try:
                md.run_md(atoms, str(id))
            except Exception as e:
                print("\n ERROR IN RUNNING MD \n")
                print("Exception: ", e)
            
    except KeyboardInterrupt:
        pass
    '''

if __name__ == "__main__":
    main()
