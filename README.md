Hamu
Sam Geen, October 2012
====

Simulation analysis is a time-consuming and complex task. Hamu wraps around existing Python analysis tools to:
1) Cleanly organise your simulations with user-defined labels
For each project, give your simulation a unique name and get a list of snapshots you can analyse, or find a snapshot at a given time
2) Saves previous analysis results to speed up repeat runs
With a single line, turn your existing functions into a smart function that saves the results and reads them back on repeat runs, for example if you decide to change a figure axis or add new snapshots to a plot

Also included is "HamuLite.py", which is a stripped-down version of Hamu that focusses on saving simulation results with less focus on organising simulations. This is useful for quickly plotting results on remote machines.

Hamu is a work in progress, so use at your own risk. If you need to get in touch, e-mail samgeen@gmail.com

SETTING UP
----------

Hamu does not have any external dependencies except the code you want to use. It is developed for Pymses but there is 

The first time you run Hamu it will do some setting up and make a ".hamu" folder in your home directory and create an empty workspace "MyWorkspace". 
The ".hamu" folder is where all the saved outputs are stored, so you may want to symbolic link to somewhere else on your filesystem (e.g. "mkdir /my/big/drive/.hamu; ln -s /my/big/drive/.hamu")

STARTING UP
-----------

Make a workspace by calling, e.g.:
>>> workspace = Workspace("GalaxiesProject")
You can use multiple workspaces at the same time. For example, each paper can use a separate workspace. It's often a good idea to put this at the top of your code so you're sure you're using the correct repository.



RELEASE IS A WORK-IN-PROGRESS - USE AT YOUR OWN RISK!

See example.py for a simple example script describing basic functionality

