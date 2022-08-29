# SidePolishFibre

Here is a small package for moddeling your fibres Siyu. 


## Installing WSL 

Although MEEP runs using python its backend unfortunatly doesn't run on windows natively, however you can install windows subsystem for linux (WSL) and run MEEP using this. 

To install WSL follow these instructions on the windows website [WSL](https://docs.microsoft.com/en-us/windows/wsl/install) 

1) Open up powershell as a administrator (right click and click open as administrator)

2) Exicute the following command: 

    > `wsl --install`

Thats it! Yous should get a few prompts appear after exicuting that command, including choosing a username and password for the linux virtual machine. Don't forget these! 

Now you should be able to run linux in windows, I'd reccomend using [Windows Terminal](https://devblogs.microsoft.com/commandline/introducing-windows-terminal/) for accessing WSL.


## Installing the Anaconda package manager for python in WSL

Now you need to install anaconda for python, navagate to the anaconda website and download the installer for [Linux](https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh).

You now have most of the tools required here, now you need to open up WSL and navagate to where you downloaded the anaconda installer. 

To do this open up WSL and navagate to the directory using the `cd` commdand. WSL has a entirely different file directory setup however, by default the windows filesystem is mounted automatically in `/mnt/c/`. So for me I can get to my downloads folder by exicuting the command:

> `cd /mnt/c/Users/Christian/Downloads/` 

You'll need to replace `Christian` with your windows username. Then you can exicute the anaconda installer with the command: 

> `bash Anaconda3-2022.05-Linux-x86_64.sh` 

Note again that your anaconda installer may have a slightly different name, remmeber you can tab autocomlete on commands. 

There will be a few prompts you'll have to go through when installing anaconda, the default settings should suffice. 

Once that's installed restart WSL by closing and re-opening the WSL window. 

## Finally installing MEEP

Now that you have an anaconda instance installed in WSL, we can now install MEEP. You can follow the instuctions here for [MEEP](https://meep.readthedocs.io/en/latest/Installation/) But in essance you can just use the following command to create a python virtual enviroment with all the packages you'll need: 

> `conda create -n mp -c conda-forge pymeep pymeep-extras numpy matplotlib jupyter lmfit scipy pandas`

I've added a few extra python packages there that will likely be useful for our work. Activate the newly created python virtual enviroment now with:

> `conda activate mp`

You'll have to run that last command every time you open WSL, finally when you are in a directory you want to work in, open up jupyter notebook with the following command: 

> `jupyter notebook`


## Downloading this repository

What you will want to do now you have everything installed is to clone this repository with all its files, to do this you need to have either git installed on WSL or download the windows app [Github Desktop](https://desktop.github.com) then you can clone the repository with this pages URL https://github.com/Chriscrossing/SidePolishFibre.


Now you can open WSL and `cd` into this cloned repo, open jupyter notebook using the command `jupyter notebook` and then navigate to a notebook that I've set up for you to mess with [here](2D_DirectModeExcitement/ModeSolving/PolishedFibreCavity_Tutorial.ipynb) in: `/2D_DirectModeExcitement/ModeSolving/
`

Let me know if you get stuck. 