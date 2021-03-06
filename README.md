# PoE-analysis

An analysis of races in Path of Exile. The companion code for the blog post 
[Path of Exile Leagues Analysis](http://stevejbrown.com/blog/PoE-analysis).

## Setup

For a detailed guide for how to get setup for scraping data please consult 
the setup section of the blog post 
[Path of Exile Scraping](http://stevejbrown.com/blog/PoE-scraping).

Python requirements can be installed using [conda](https://conda.io/docs/index.html):

scraping:

```bash
conda env create -f scraping-environment.yml
```

analysis:

```bash
conda env create -f analysis-environment.yml
```

Please note the scraping code uses python2 while the analysis code uses python3.
