# [leetscraper](https://pypi.org/project/leetscraper/ "leetscraper on pypi") &middot; [![Downloads](https://pepy.tech/badge/leetscraper)](https://pepy.tech/project/leetscraper "Total downloads from pypi") &middot; [![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/pavocracy/leetscraper.svg)](http://isitmaintained.com/project/pavocracy/leetscraper "Average time to resolve an issue") &middot; [![Percentage of issues still open](http://isitmaintained.com/badge/open/pavocracy/leetscraper.svg)](http://isitmaintained.com/project/pavocracy/leetscraper "Percentage of issues still open")
leetscraper is a web scraper for leetcode and other coding challenge websites!  
It was created as a way to gather coding problems to solve without having to sign up to a website or submit code to a problem checker.

***
 
# Usage
  
### Install package and dependencies
```python
pip install leetscraper tqdm urllib3 beautifulsoup4 selenium webdriver-manager
```

### Examples

Import the module and Instantiate the class. The class has some kwargs options to control the behaviour of the scraper.
However, all the default values will start to scrape all problems from [leetcode.com](https://leetcode.com "leetcode website") to the cwd.
  
The most basic usage looks like this:
```python
from leetscraper import Leetscraper

if __name__ == "__main__":
    Leetscraper()
```
  
The avaliable kwargs to control the behaviour of the scraper are:
```python
"""
website_name: "leetcode.com", "projecteuler.net", "codechef.com" ("leetcode.com" is set if ignored)
scraped_path: "path/to/save/scraped_problems" (Current working directory is set if ignored)
scrape_limit: Integer of how many problems to scrape at a time (-1 is set if ignored, which is no limit)
auto_scrape: "True", "False" (True is set if ignored)
"""
```
  
Example of how to automatically scrape the first 50 problems from [projecteuler.net](https://projecteuler.net "project euler website") to a directory called SOLVE-ME:
```python
from leetscraper import Leetscraper

if __name__ == "__main__":
    Leetscraper(website_name="projecteuler.net", scraped_path="~/SOLVE-ME", scrape_limit=50)
```
  
Example of how to scrape all problems from all supported websites:
```python
from leetscraper import Leetscraper

if __name__ == "__main__":
    websites = ["leetcode.com", "projecteuler.net", "codechef.com"]

    for site in websites:
        Leetscraper(website_name=site)
```
  
You can pass through different arguments for different websites to control exactly how the scraper behaves.
You can also disable scraping problems at time of instantiation by using the kwarg `auto_scrape=False`.
This allows you to call the class functions in different order, or one at a time.
This will change how the scraper works, as its designed to look in a directory for already scraped problems to avoid duplicates.
I would encourage you to look at the function docstrings if you wish to use this scraper outside of its intended automated use.

***

# Contributing
If you would like to contribute, adding support for a new coding challenge website, or fixing current bugs is always appreciated!
I would encourage you to see [CONTRIBUTING.md](https://github.com/Pavocracy/leetscraper/blob/main/docs/CONTRIBUTING.md "Contributing doc") for further details.
If you would like to report bugs or suggest websites to support, please add a card to [Issues](https://github.com/Pavocracy/leetscraper/issues "Github issues").
Thank you to all contributors to this project!  
  
<a href="https://github.com/pavocracy/leetscraper/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=pavocracy/leetscraper" />
</a>  

***

# Code of Conduct

Contributing to this project means you are willing to follow the same conduct that others are held to! Please see [Code of Conduct](https://github.com/Pavocracy/leetscraper/blob/main/docs/CODE_OF_CONDUCT.md "Code of conduct doc") for further details.

***

# Licence  
This project uses the GPL-2.0 License, As generally speaking, I want you to be able to do whatever you want with this project, But still have the ability to add your changes
to this codebase should you make improvements or extend support.
For further details on what this licence allows, please see [LICENSE.md](https://github.com/Pavocracy/leetscraper/blob/main/LICENSE.md "GPL v2 Licence")
