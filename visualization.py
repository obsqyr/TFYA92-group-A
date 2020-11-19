from asap3 import Trajectory

def visualization(file, atoms, n):
    traj = Trajectory(file, 'w', atoms)
    dyn.attach(traj.write, interval = n)
