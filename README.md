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

##### Using Massey and Colley Ratings
- Massey 
  - A linear system using the score differential of games

- Colley
  - A linear system that uses wins and losses, with more complex weighting added by home ground advantage and date of win

##### Download Ranking Data
- [https://masseyratings.com/](https://masseyratings.com/) <br/>
