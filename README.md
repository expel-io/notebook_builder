# How to create and maintain Jupyter threat hunting notebooks - Example Source Code

<p align="center">
  <img width="600" height="200" src="https://github.com/expel-io/notebook_builder/blob/master/images/expel.png">
</p>

An example of scaling the use of Jupyter Notebooks with nbformat and YAML configuration files.

Below is the example source code for Expel’s blog post, “How to create and maintain Jupyter threat hunting notebooks.” You can find the blog here: [Link to blog post]

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
