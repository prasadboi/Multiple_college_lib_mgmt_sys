## SETTING UP 

1. Setting up pre-requisites :
      1. if you have installed Python already (not via anaconda), then do as follows :-
          1. add python to and python's scripts folder to your PATH variable 
          2. check if python is added to your path by simply entering `python` in your command line. Python should start up, else it has not been added to your path variable properly
          3. install pip 
              1. how ?
              2. execute -> `python get-pip.py` in your command line
          4. install VirtualEnv
              1. execute -> `pip install virtualenv`
      2. if you installed via anaconda, then these packages would be preinstalled, just make sure to add anaconda `to my path` while installation


2. Configuring your project
      1. `cd` into the project directory
      2. setup a virtual environment
            1. to create a new virtual environment for the project , run `python -m venv DBMS`, here *DBMS* is your environment name, and you can set it to whatever you want
            2. to activate the virtual environment run `DBMS\Scripts\activate` -> do this in your command line and not in your integrated terminal on vscode
            3. If you do wish to run it on vscode's terminal do, `$ . DBMS\Scripts\activate.ps1`
            4. once the environment has been activated you should be able to see something like this -> `(DBMS) ~_path_to_project_directory_$ ...`
            5. update your pip by running - `python -m pip install --upgrade pip` inside your environment
            6. inside your environment run ` pip install -r requirements.txt` (NOTE : incase your command line freezes then run `python -m pip install -r requirements.txt`), this should install django in your environment


## What next ? read the following
  1. *https://tutorial.djangogirls.org/en/*
  2. *https://drive.google.com/drive/folders/1zIm5DiSFhsGo-HuvGRLXAH629zxR4K29?usp=sharing*
  3. *https://csabitsh.wordpress.com/git-and-github/*
  4. *https://www.facebook.com/groups/bphcshoutbox/permalink/3132116213517635/*


*Arigato gosaimas*
