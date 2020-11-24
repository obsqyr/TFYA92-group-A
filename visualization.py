def visualize(file, atoms):
    traj = Trajectory(file, 'w', atoms)
    dyn.attach(traj.write, interval=1000)
