Hamu
Sam Geen, 2012-2017
====

Simulation analysis is a time-consuming and complex task. Hamu wraps around existing Python analysis tools to:
1) Cleanly organise your simulations with user-defined labels
For each project, give your simulation a unique name and get a list of snapshots you can analyse, or find a snapshot at a given time
2) Saves previous analysis results to speed up repeat runs
With a single line, turn your existing functions into a smart function that saves the results and reads them back on repeat runs, for example if you decide to change a figure axis or add new snapshots to a plot

Also included is "HamuLite.py", which is a stripped-down version of Hamu that focusses on saving simulation results with less focus on organising simulations. This is useful for quickly plotting results on remote machines. See below for more information on this module.

Hamu is a work in progress, so use at your own risk. It is published under the MIT license (see LICENSE.md). If you need to ask for help or report a bug, e-mail samgeen@gmail.com

SETTING UP
----------

Hamu does not have any external dependencies except the analysis package you want to use. It is developed for Pymses but there is a wrapper for YT included (email if you have problems with this wrapper). Make sure the directory containing Hamu is in your PYTHONPATH environment variable:
> $PYTHONPATH=$PYTHONPATH:/my/scripts/directory

Hamu should work on any Unix system (OSX, Linux, Ubuntu on Windows) with Python 2.7 or similar.

The first time you run Hamu it will do some setting up and make a ".hamu" folder in your home directory and create an empty workspace "MyWorkspace". 
The ".hamu" folder is where all the saved outputs are stored, so you may want to symbolic link to somewhere else on your filesystem (e.g. "mkdir /my/big/drive/.hamu; ln -s /my/big/drive/.hamu")

A basic example script called example.py is given for reference.

STARTING UP
-----------

First, import Hamu
>>> import Hamu

Make a workspace by calling, e.g.:
>>> workspace = Hamu.Workspace("GalaxiesProject")
You can use multiple workspaces at the same time. For example, each time you start a distinct suite of simulations you can use a separate workspace. It's often a good idea to put this at the top of your code so you're sure you're using the correct repository.

Now, you can make a simulation object. The easiest way to set up a simulation is to go to where your outputs are stored, open python and enter (for example):
>>> import Hamu
>>> Hamu.MakePymses("DarkMatterOnlyRun")
where "DarkMatterOnlyRun" is a unique name to describe your simulation that you will use from now on.

Hamu now knows where your simulation is. To access it anywhere on the machine, use:
>>> sim = Hamu.Simulation("DarkMatterOnlyRun")
"sim" is an object that you can use to access your snapshots.

You can give a simulation a second label, e.g. for plotting with readable legends
>>> sim.Label("Dark Matter Only (No Gas)")
>>> # do stuff here
>>> plt.plot(radii,profile,label=sim.Label())
>>> plt.legend()

If you want to use the same simulations for multiple projects without splitting into separate workspaces (which will duplicate the saved results), you can use Project objects. To create a project and add "sim" to it, call:
>>> project = Hamu.Project("GalaxyComparisonProject")
>>> project.AddSimulation(sim)
The project will be saved in the workspace and will exist when you re-load python. To remove a simulation, use:
>>> project.Remove(sim)
You can also pass the simulation's unique name instead of a simulation object:
>>> project.Remove("DarkMatterOnlyRun")

To run through the simulations in a project, call, e.g.
>>> for sim in project.Simulations():
>>>     print "Simulation name:", sim.Name()

ANALYSING A SIMULATION
----------------------

A Simulation holds a set of snapshots. These are wrappers around snapshot objects given by the analysis code (Pymses,YT,etc). To run through all the snapshots in a simulation, call:
>>> for snap in sim.Snapshots():
>>>     print "Snapshot number, time:", snap.OutputNumber(), snap.Time()

To analyse a function, you need to first create an Algorithm. This is a smart function that wraps around your existing analysis functions. You must use functions with the following structure:
- First argument is a snapshot
- Arguments after this are hashable variables (e.g. integers, floats with reliable precision, strings, tuples)
- Has a return value that can be pickled by python (optional)
Say you have a function:
>>> def MakeProfile(pymsesoutput,"temperature",maxradius=4.0):
>>>     # do stuff here
>>>     return radii, profile
Call the following line:
>>> MakeProfileHamu = Hamu.Algorithm(MakeProfile)
Now MakeProfileHamu is a smart function you can call on Hamu snapshots like a normal function
>>> for snap in sim.Snapshots():
>>>     radii, profile = MakeProfileHamu(snap,"temperature",maxradius=4.0)
>>>     plt.plot(radii, profile, label="Snapshot "+str(snap.OutputNumber())
The first time you run this Hamu will run MakeProfile and save the data. The second time you run it (e.g. you have more outputs, you want to change the axes or linestyles), it will read it from a "cache" file in the .hamu folder.

WARNING: Hamu does not (yet) know if you changed the snapshots or functions. You will have to go into "~/.hamu/workspaces/WorkspaceName/Simulations/SimulationName/snap*/" and delete by hand any files that begin with "MakeProfile" (or the name of your function). To check which files you used with which inputs, you can check the ".info" files.

If you want to avoid rerunning something but don't need to save the results, just return None in your function. For example, if you are making images as your simulation is running and don't want to re-make the image every time your simulation advances.

Each snapshot contains a function RawData() that returns the raw (e.g. Pymses) snapshots:
>>> ro = snap.RawData()
>>> print "Snapshot number", ro.iout
Likewise, Hamu will add a "hamusnap" variable to the raw snapshots to allow the code to reach back up:
>>> snap = ro.hamusnap
>>> radii, profile = MakeProfileHamu(snap,"temperature",maxradius=4.0)

You can also nest Hamu functions in this way. For example, if you want to run a function inside another one and make both Hamu smart functions, you can use:
>>> def SecondFunction(snap,var):
>>>     return snap.iout*var**2.0 # or whatever
>>> SecondFunctionHamu = Hamu.Algorithm(SecondFunction)
>>> def FirstFunction(snap,var):
>>>     return SecondFunctionHamu(snap.hamusnap,var+2)
>>> FirstFunctionHamu = Hamu.Algorithm(FirstFunction)
>>> for snap in sim.Snapshots():
>>>     print "My result:", FirstFunctionHamu(snap,20.0)

HAMULITE.py
-----------

HamuLite.py is a stripped-down version of Hamu that doesn't save simulation structures but does allow you to cache/save function results. The advantage is that it's a single file that is a lot easier to move around and deploy. It will make a "cache/" folder in the working directory instead of using "~/.hamu".

SOURCE CODE
-----------

Experienced users are encouraged to explore the code. Hamu is a more-or-less object oriented code. Objects and object methods have camel-case names. Methods beginning with a "_" are private methods that should not be called by a different class (of course, I can't stop you, but they're not designed to work like that, so use with caution).

Suggestions for new features and updates are welcome.

CREDITS
-------

This code is developed by Sam Geen (samgeen@gmail.com)