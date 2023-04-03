## Py Data Cardiff Hack Night at the Bike Lock

### What is this?

PyData Cardiff organised a hack night at the [Bike Lock](https://www.thebikelock.co.uk/) on the 6th of April 2023, sponsored by [engi.ai](www.engi.ai). The aim of the hack night was to get people together to work on projects that they are interested in. The event was open to anyone who was interested in data science, machine learning, data visualisation, or any other related topic. 

### What are we doing?

The [R For Data Science](https://github.com/rfordatascience/tidytuesday) community publishes a small data set every week for people to practice programming [R](https://www.r-project.org/). PyData Cardiff decided to do the same for Python. We chose to use the [cats of the UK data set from 2023-01-31](https://github.com/rfordatascience/tidytuesday/tree/5909ea94b47e9d17b2e6287f38e5ba4760e65a51/data/2023/2023-01-31). 

### How do I get started?

(step 0 is to make sure you have a github account and install[git](https://github.com/git-guides) on your machine)

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) this repository
1. [Clone](https://github.com/git-guides/git-clone#git-clone) your forked repository to your local machine
1. Avoid modifying the `tidy_tuesdays_original` folder directly.
1. Make a folder with your github user name in the pydata_cardiff folder
    * You could even pair up with someone else and make a folder with both your user names
1. [Add](https://github.com/git-guides/git-add) your code to the folder you created

### What do I make?

1. Anything you want! If you think you might be able to do it, have a go. Think about what you want to learn, and try to do that. Or maybe think about what you've seen cats do around you and see if you can prove it from the data.

(But if you are stuck for ideas heres a few)

* Topic specific ideas
    * A static data visualisation of a single cats path accouring to the lat and long data, with the path connected by the timestamps
    * An interactive data visualisation of the cats elevation over time with a user input to select a specific cat
    * An investigation into the typical geographic range of a cat, and if this is different between male and female cats
    * Join the data with UK geographical data to visualise the geographic range of the cats and count cats per county
    * Identify if any cat on the study met another cat on the study at a particular place and time to complain about the stupid collars they had to wear
    * Analyse the data to see if there is a correlation between cats of periods of increased activity, and see if that supports the hypothesis that cats are [nocturnal](https://en.wikipedia.org/wiki/Nocturnality), [diurnal](https://en.wikipedia.org/wiki/Diurnality) or [crepuscular](https://en.wikipedia.org/wiki/Crepuscular_animal)
* Tool specific ideas
    * An interactive plot made using [plotly](https://plotly.com/python/), [bokeh](https://docs.bokeh.org/en/latest/) or [holoviz](https://holoviz.org/)
    * A data visualisation that you can deploy to Web Assembly using [PyScript](https://github.com/pyscript/pyscript)
    * A comparison of the performance of base Pandas with a 'fast' alternative such as [Polars](https://github.com/pola-rs/polars), [Dask](https://github.com/dask/dask)  or [Vaex](https://github.com/vaexio/vaex) when performing the same operation (e.g. a join on the same key, a filter on the same column, etc.)
    * A local web server/API that can be queried for a specific cat, and returns the cats path as a GeoJSON object (see [GeoJSON](https://geojson.org/)) built with [FastAPI](https://fastapi.tiangolo.com/) or [Flask](https://flask.palletsprojects.com/en/2.0.x/)
    * Manage your project dependencies and development environment using `pip freeze > requirements.txt` [conda](https://docs.conda.io/en/latest/), [poetry](https://python-poetry.org/), [hatch](https://hatch.pypa.io/latest/), [venv](https://realpython.com/python-virtual-environments-a-primer/) or [docker](https://www.docker.com/blog/how-to-dockerize-your-python-applications/).
* Machine learning specific ideas
    * Predict the chance of a cat jumping based on it's location and time of day
    * Catagorise cat activities such as 'sleeping', 'feeding', 'patroling', 'exploring'.
    * Predict a cats age based on their level of activity
    * Predict a cat's gender based on the geographic size of thier range
    * Define when a cat is 'pouncing' on something

> @DaveParr does not take any responsibility for the quality of the ideas listed above. For any given idea it may be too hard, too easy, or just plain stupid.

### What do I do when I am done?

1. [Commit](https://github.com/git-guides/git-commit#git-commit) your changes to your local repository.
1. [Push](https://github.com/git-guides/git-push) your changes to your forked repository.
1. Create a [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) to merge your changes into this repository.
1. Use your new knowledge for the good of cats everywhere

### What if I have questions?

1. Ask someone near you, they're probably really nice.
1. Google it, reading the docs isn't cheating!
1. Ask one of the organisers.