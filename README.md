# Page analyzer 

Webpage Analyzer is an online tool that assesses the compatibility of web pages with SEO practices, much like the functionality offered by PageSpeed Insights.

## Tests and linter status:
[![Actions Status](https://github.com/Barzabel/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Barzabel/python-project-83/actions)
[![all tests](https://github.com/Barzabel/python-project-83/workflows/all_tests/badge.svg)](https://github.com/Barzabel/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/321779d1cc616bfe1c60/maintainability)](https://codeclimate.com/github/Barzabel/python-project-83/maintainability)


this is a pet-progect
While working on it, I had the opportunity to engage with  technologies like Flask, Jinja, and PostgreSQL.
### You can check the project  [web-site](https://page-analyzer-qkil.onrender.com/)

## Requirements
* python >=3.10
* Poetry >= 1.6
* PostgreSQL >= 15.4

***

## Required packages
* psycopg2-binary ^2.9.7 for postgres.
* Other packages inside pyproject.toml
* 
*** 

## Installation
* Clone the repo: 
```git clone https://github.com/Barzabel/python-project-83```.
To use the app properly you'll need to provide it with `$DATABASE_URL` and `$SECRET_KEY` vars.

To deploy the application, you need to rename the `.env-sample` file to `.env` in the root directory. 
After that, modify the values for `SECRET_KEY` and `DATABASE_URL.`
It is important to insert your own values.

After that

Run ```make build``` to install all required packages and create necessary tables in the database.

Run ```make start``` to start.

