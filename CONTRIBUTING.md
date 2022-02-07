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

Contributing to this project means you are willing to follow the same conduct that others are held to! Please see [Code of Conduct](https://github.com/Pavocracy/leetscraper/blob/main/CODE_OF_CONDUCT.md) for further details.

### **DO NOT include ANY scraped problems as part of your PR, otherwise the PR will be rejected!**
