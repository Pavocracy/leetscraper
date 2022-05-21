# Advanced usage

Leetscraper is a package fully intended for automated use. However, there is nothing stopping you from using these class methods
and module functions separately as part of a manual process. This can be as simple as utalising the kwargs to control intended
behaviour, or calling functions and methods as you see fit. Below is some examples of advanced usage.

***

## kwargs with leetscraper

Leetscraper allows you to pass through different kwargs to control exactly how the scraper behaves.
You can also disable scraping problems at time of initialization by using the kwarg `auto_scrape=False`.
This allows you to call the class functions in different order, or one at a time.
This will change how the scraper works, as its designed to look in a directory for already scraped problems to avoid duplicates.
This scraper was built with automation in mind. Run the script and forget, and come back to scraped coding problems.
For manual use you will need the help of this doc and I would also encourage you to read the methods and functions docstrings.
Below is some good examples of how to control the automation of leetscraper, or use it manually.

***

## Examples 

Example of how to automatically scrape the first 50 problems from projecteuler.net to a directory called SOLVE-ME:
```python
from leetscraper import Leetscraper

if __name__ == "__main__":
    Leetscraper(website_name="projecteuler.net", scrape_path="~/SOLVE-ME", scrape_limit=50)
```

Example of how to scrape all problems from all supported websites:
```python
from leetscraper import Leetscraper

if __name__ == "__main__":
    websites = [
        "leetcode.com",
        "projecteuler.net",
        "codechef.com",
        "hackerrank.com",
        "codewars,com",
    ]
    for site in websites:
        Leetscraper(website_name=site)
```

Example of how to manually scrape 3 specific problems from leetcode.com:  
*note: this requires you to know the difficulty of the problem when building get_problems*  
*get_problems pattern is a list, of lists of problems, where each problem is [problem name, difficulty]*
```python
from leetscraper import Leetscraper

if __name__ == "__main__":
    scraper = Leetscraper(
        website_name="leetcode.com",
        auto_scrape=False,
    )
    scraper.driver, scraper.get_problems = scraper.setup_scraper()
    scraper.get_problems = [
        ["number-of-longest-increasing-subsequence", 2],
        ["partition-equal-subset-sum", 2],
        ["minimum-possible-integer-after-at-most-k-adjacent-swaps-on-digits", 3],
    ]
    scraper.scraped = scraper.start_scraping()
```
