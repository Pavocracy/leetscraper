# Contributing

If you would like to add support for another coding challenge website, AWESOME! Feel free to ask for any advice if you wish. 
I keep myself busy by trying to add to this repo, so its likely I've already looked at, and thought about ways I might extend support for other website. 
If you have added support for a website and would like to put up a PR, that's appreciated! I would encourage you to follow some basic steps beforehand.

***

## Pull Requests Process
```python
pip install -r ./requirements.txt
```
- Make sure to install the requirements, as it contains the versions of librarys needed to pass formatting and linting.
- Also download chromedriver and put it in the root directory of this repo. The unit tests require it to run.

```python
black ./src
```
- Use black to format the code. This is not the be all end all solution to nicely formatted code, but it will atleast be consistent with how I've made this project.

```python
mypy ./src
```
- Use mypy to check for any obvious type issues. This mostly is about encouraging using type hints to be more human readable. 
If you are having errors such as `error: Skipping analyzing 'libraryname': found module but no type hints or library stubs`, you probably didn't install from requirements.txt.  
If you want to manually fix this instead, you can use `pip install types-libraryname` for the library being skipped. 

```python
pylint ./src --fail-under=9
```
- Use pylint to ensure there is a general level of "best practice" used. You would be surprised at how often this can give some very good suggestions to make things more readable.  
Anything over a score of 9/10 will be accepted into the main branch :)

```python
python -m unittest discover
```
- Run the unit tests and ensure they all pass. If you have added support for a website, ensure unit tests are written and passing for that website.

***

## Code of Conduct

Web scrapers are a touchy subject for some. Others have no moral objections at all. For me its all about context. 
I built this project for the purpose of being able to solve coding problems at my leisure on my local machine.
I am not always interested in signing up to a website and submitting my code to a solution checker. I just want a reason to code sometimes :)
But understanding that these websites do have their own licence and copyright protections is imporant to remember. 
If you are to use this project to scrape problems, Think VERY CAREFULLY about how and where you use those scraped problems. 
Most of the websites TOS forbid redistributing their problems and solutions. 

### **DO NOT include ANY scraped problems as part of your PR, otherwise the PR will be rejected!**
