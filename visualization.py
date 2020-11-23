def visualize(file, atoms):
    traj = Trajectory(to.string(file), 'w', atoms)
    dyn.attach(traj.write, interval=1000)
