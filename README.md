# Jupyter Notebooks at Scale Example Source Code

An example of scaling the use of Jupyter Notebooks with nbformat and YAML configuration files.

This is the example source code for Expel's blog post on Jupyter Notebooks at Scale: [blog link here]

## Instructions

Follow the steps below to see the example in use.

1. Clone this repo and change into the repo directory:

```
$ git clone git@github.com:expel-io/notebook_builder.git
```
```
$ cd notebook_builder
```

2. Build:

```
$ docker-compose build
```

3. Build the notebooks and run the Jupyter server:

```
$ docker-compose run --service-ports notebook
```

4. Continue to test, learn, iterate!
