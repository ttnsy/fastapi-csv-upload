# Home Assignment 2
## Part 1
As a user, I want to be able to see all of my datasets at a glance with their respective metadata.

To achieve this, you need to retrieve the metadata when the file is being uploaded and save it somewhere.

Requirements:
- Storage mechanism for the metadata
- Some kind of relation mechanism between the data file and its metadata
- Metadata itself is defined as:
	- file size
	- shape (number of rows and columns)
	- column types

Hints/Considerations:
- The default "storage mechanism" is probably a SQL database, but what other options can you think of?
- Look into ORM, what libraries are popular in Python for that
- Data file saving, and a database entry insert - are two completely independent operations. How to establish a relationship between them?
- How do you make sure that the database is always present in the application, even if it is started for the first time?
- How would you test the new functionality?
  

  # Home Assignment 3 - technical side quest

## Part 1
We begin to write quite a bit of code, and it's easy to lose track of the code quality. Let's make sure that we continuously maintain high standard here.

Requirements:
- Install and configure MyPy
- Install and configure Ruff
- Define a simple GIthub Actions pipeline

## Part 2
It is important to have a fresh database every time we run the tests. One common pattern to achieve this, is to have a separate testing DB.

Requirements:
- Create an Environment Variable that controls database connectivity
	- In our case this is just a filename
- Define a function that creates a SQLite file and creates all required tables in there
	- Use this function in 2 places: inside the (1) `lifespan` context of your application, (2) in the `conftest` file where before yielding a testing client
- Make a small research on what might be the best way to change the Environment Variable in testing
	- There are multiple approaches, including env files, inline pytest arguments, pyproject configuration, and various "tooling" files, e.g. makefile, justfile, taskfile

## Part 3
Whenever we begin to work with a database, it is worth knowing of a concept called "database migrations". One of the most popular tools in Python ecosystem that works well with SQLAlchemy is Alembic.

Here is the official tutorial https://alembic.sqlalchemy.org/en/latest/tutorial.html.

Requirements:
- Read the tutorial, make sure you understand everything
- Configure alembic in your own project
- Make that you run all necessary migrations whenever necessary (before creating a new db file, both in main app and in testing)

## Bonus
In case you are getting overwhelmed with the amount of different commands that you have to run (run the app, set env variables, run migrations, tests, all the checkes, etc) - consider using a special file to run commands. Personally, I use Justfile in my projects, but recently I learned about Taskfile - and it looks amazing.


-----

# Home Assignment 4. Logging
## Part 1
Logging is very important in the production application: observability and transparency into what happened in the app. Error traces, additional info, profiling, etc.

You need to configure your own logger in the app using the builtin `logging` module.

**Requirements:**
- [ ] Run the app using `uvicorn` command, not `fastapi` - I will explain on the call why I think it's better
- [ ] Configure the logger using `logging.config.dictConfig` for maintainable configuration
- [ ] Write logs (at least) in two places - stream (aka console) and a file. Think about possible formats for the log, what common options do you know? Experiment with different formats.
**Hints:**
- Check out how shiny.telemetry stores logs in file. What is the format, and why do you think it is done like that?

## Part 2
We are always concerned about the application performance. To be able to constantly profile your application, you need to measure the processing time for every endpoint that you have in the application.

Configure `http` middleware in FastAPI to calculate how much time did the request processing take - and log it.

Requirements:
- On every endpoint access there is a log entry saying how long did it take to process the request
Hints:
- You may want to add a couple more simple endpoints to the app for more visible results. Make one endpoint artificially slow.

## Part 3
Write a simple script that would read, parse and aggregate the logs.

Requirements
- Given a log file saved from part 1, read it and display a table with average processing time per endpoint

Home Assignment 5

## Part I
Description
This assignment is dedicated to working with the files more. First of all, CSV is not a very good format for storing large quantities of files. For this purpose I suggest that we read files uploaded by the users and save them in parquet format.
Requirements:

Store files in parquet format
Read files in parquet format
Hints:

Current codebase might require some refactoring to make sure that we're not reading the file twice

## Part 2
Description
The existing metadata that we are currently getting from an uploaded dataset is very minimal. For future work we will require more information about the dataset (listed in the requirements) to conduct some analysis. To achieve this, you would need to extend the extract_csv_metadata function and write more data to the database.

Requirements:
Guess the "ID" column in the dataset --- also detect by the name
Guess the "DATE" column in the dataset
Guess the "VALUE" column in the dataset

Store this information in CSVMetadata table
You must test a few different datasets to demonstrate robustness of your guessing heuristics
You must test negative scenarios as well (DATE column not present, DATE column present but not identified, etc)

Hints:
You probably need to update your testing data
You need to add some function to guess the columns mentioned in the requirements. Think for yourself how you would like to approach it.
## Part 3
Description
Now that we have more info about the uploaded datasets, we can start doing some analysis. As a user, I want to be able to see how the VALUE was changing over DATE.
Requirements:
Add an endpoint that would return a table-like response with every row representing a date and a value
Depending on the user request aggregate data on a daily, weekly, monthly basis
Depending on the user request aggregate data via sum, average, and median
Depending on the user request group data by ID column or don't
Hints:
Once again, think about how you want to prepare your testing data. Use LLMs to generate it for you.
This about the "user request" - how would you implement this in FastAPI





Q:
- logger error vs exception