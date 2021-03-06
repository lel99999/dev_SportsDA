# dev_SportsDA
Sports Data Analytics 

##### Set up Jupyter Notebook
- Ubuntu
  - Install python dependencies, pip, virtualenv, jupyter
  ```
  $sudo apt install python3-pip python3-dev
  $sudo -H pip3 install --upgrade pip
  $sudo -H pip3 install virtualenv

  $mkdir ~/jupyter_project
  $cd ~/jupyter_project

  $virtualenv jupyter_project_env

  or

  $python3 -m venv jupyter_project_env

  $source jupyter_project_env/bin/activate

  $pip3 install jupyter
  ```

  - Run Jupyter Notebook
  ```
  $(jupyter_project_env) jupyter notebook
  ```
  ![https://github.com/lel99999/dev_SportsDA/blob/main/jupyternotebook_browser-01.png](https://github.com/lel99999/dev_SportsDA/blob/main/jupyternotebook_browser-01.png) <br/>

- RHEL7/CentOS7
  - INstall python epel, python dependencies, vitualenv, pip, jupyter
  ```
  $sudo yum install epel-release

  ## Requires the following for RHEL7: --enablerepo=rhel-7-server-optional-rpms
  $sudo yum install -y python3-pip python3-devel python3-virtualenv --enablerepo=rhel-7-server-optional-rpms
  $sudo yum groupinstall 'Development Tools'

  $python3 -m venv jupyter_project_env
  $source jupyter_project_env/bin/activate
  (jupyter_project_env) [user@system ~]$pip3 install jupyter
  (jupyter_project_env) [user@system ~]$pip3 install --upgrade pip
  ```
  - Run Jupter Notebook
  ```
  $jupyter notebook
  ```
  ![https://github.com/lel99999/dev_SportsDA/blob/main/jupyternotebook_browser_centos7-01.png](https://github.com/lel99999/dev_SportsDA/blob/main/jupyternotebook_browser_centos7-01.png) <br/>
  
##### Using Massey and Colley Ratings
- Massey 
  - A linear system using the score differential of games

- Colley
  - A linear system that uses wins and losses, with more complex weighting added by home ground advantage and date of win

##### Download Ranking Data
- [https://masseyratings.com/](https://masseyratings.com/) <br/>

##### College Football
- Ratings and Rankings 
  - SP+ A tempo and opponent adjusted measure of college football efficiency
  - FEI (Fremeau Efficiency Index) Ratings 
    Represents the per-possession socring advantage each team would be expected to have on a neutral field agains an average opponent 
  - F+ Ratings

- Links
  - [Analyzing Data and Film Concurrently](https://www.sloansportsconference.com/event/college-football-analytics-analyzing-tracking-data-and-film-concurrently-to-get-an-upper-hand) <br/>
