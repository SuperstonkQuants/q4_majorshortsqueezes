# q4_majorshortsqueezes
Using this repo we try to answer the question how many major short squeezes have happened in the US stock market.

# Getting Started
## Install

We have the same building infrastructure as the GameStonkTerminal:
https://github.com/GamestonkTerminal/GamestonkTerminal

If you want to use or contribute to the GameStonkTerminal you can use the same tech stack.
### Install

This project supports Python 3.9.

Our current recommendation is to use this project with Anaconda's Python distribution - either full [__Anaconda3 Latest__](https://repo.anaconda.com/archive/) or [__Miniconda3 Latest__](https://repo.anaconda.com/archive/). Several features in this project utilize Machine Learning. Machine Learning Python dependencies are optional. If you decided to add Machine Learning features at a later point, you will likely have better user experience with Anaconda's Python distribution.

1. Install Anaconda

Confirm that you have it with: `conda -V`. The output should be something along the lines of: `conda 4.9.2`

2. Install git

```
conda install -c anaconda git
````

3. Clone the Project

  - Via HTTPS: `git clone https://github.com/DidierRLopes/GamestonkTerminal.git`
  - via SSH:  `git clone git@github.com:DidierRLopes/GamestonkTerminal.git`

4. Navigate into the project's folder

```
cd GamestonkTerminal/
```

5. Create Environment

You can name the environment whatever you want. Although you could use names such as: `welikethestock`, `thisistheway` or `diamondhands`, we recommend something simple and intuitive like `gst`. This is because this name will be used from now onwards.

```
conda create -n q4 --file conda/conda-3-9-env.yaml
````

6. Activate the virtual environment

```
conda activate q4
```

Note: At the end, you can deactivate it with: `conda deactivate`.

7. Install poetry dependencies

```
poetry install
```

This is a library for package management, and ensures a smoother experience than: ``pip install -r requirements.txt``

8.  You are ready to interact with the package:

```
poetry run python -c "from q4_majorshortsqueezes.hello_world import hello_world; print(hello_world())"
```
(The above prints `Hello World!`)
