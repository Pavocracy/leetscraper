# Contributing

If you would like to add support for another coding challenge website, AWESOME! Feel free to ask for any advice if you wish. 
I keep myself busy by trying to add to this repo, so its likely I've already looked at, and thought about ways I might extend support for other website. 
If you have added support for a website and would like to put up a PR, that's appreciated! I would encourage you to follow some basic steps beforehand.

***

## Pull Requests Process

### Automated Process

For your (and mine!) convenience, this repo contains a bash script [contributing.sh](https://github.com/Pavocracy/leetscraper/blob/main/tools/contributing.sh "contributing bash script") in the tools directory.  
It can be passed flags to automatically run different tools required to enable your PR to be merged into the main branch.  
-i is to install requirments.txt  
-a is to run autopep8  
-d is to run docformatter  
-m is to run mypy  
-p is to run pylint  
  
You can pass in one flag at a time, or multiple flags. An example of how to use this script to run all tools before you submit a PR:  
*note: this script requires you to have python3 installed and have it correctly in your path*  
*to use this exact example you must run it from the root of the leetscraper directory*
*always open and read scripts before you run them. this is a very basic script and easy to follow and understand*
```
bash tools/contributing.sh -iadmp
```

### Manual Process

If you do not wish to use the contributing.sh script (or it doesn't work for you), Then please follow the below manual steps before submitting a PR:
```python
pip install -r requirements.txt
```
- Make sure to install the requirements, as it contains the versions of librarys needed to pass formatting and linting.

```python
python3 -m autopep8 -i -r src/
```
- Use autopep8 to format the code. This is not the be all end all solution to nicely formatted code, but it will atleast be consistent with how I've made this project.

```python
python3 -m docformatter -i -r src/
```
- Use docformatter to format docstrings. This is purely a convenience tool to conform to pep8.

```python
python3 -m mypy src/
```
- Use mypy to check for any obvious type issues. This mostly is about encouraging using type hints to be more human readable. 
If you are having errors such as `error: Skipping analyzing 'libraryname': found module but no type hints or library stubs`, you probably didn't install from requirements.txt.  
If you want to manually fix this instead, you can use `pip install types-libraryname` for the library being skipped. 

```python
python3 -m pylint src/
```
- Use pylint to ensure there is a general level of "best practice" used. You would be surprised at how often this can give some very good suggestions to make things more readable. 
Anything over a score of 9/10 will be accepted into the main branch :)

```python
python3 -m unittest discover
```
- Run the unit tests and ensure they all pass. If you have added support for a website, ensure unit tests are written and passing for that website.

***

## Code of Conduct

Contributing to this project means you are willing to follow the same conduct that others are held to! Please see [Code of Conduct](https://github.com/Pavocracy/leetscraper/blob/main/docs/CODE_OF_CONDUCT.md "Code of conduct doc") for further details.

### **DO NOT include ANY scraped problems as part of your PR, otherwise the PR will be rejected!**
