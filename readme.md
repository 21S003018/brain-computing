## How to run the code?

The use method is as the following steps:

1. download the code
2. pip install the package: SPARQLWrapper
3. unzip apache-jena-fuseki-3.12.0.zip and run fuseki-server.bat(the file is a little large, please go the official website to download it.)
4. open http://localhost3030 and then create dataset for your agent, and the name of a dataset should be the same to the agent's name that can be found under 'externalsettting' folder.
5. now you can run the code with the following order:
   1. python externalsetting/environment.py
   2. python UI.py

After running the code for a while, you will get some logs. There are some log message about the agent's states and position. You can use visualize.py to observe the agent's actions. The concrete use method can refer to the example.zip.

## How to modify the code?

First you can read the theory framework at [https://1173710224.github.io/brain_computing/](https://1173710224.github.io/brain_computing/).

Then let me explain the structure of the code a little bit.

### What if you want to add an agent?

1. create dataset for the agent in you local server data base
2. mkdir for the agent under 'externalsetting' folder and the content of the folder should be the same to those existing agents.
3. add update message method for your new agent in externalsetting/environment.py like `update` method.

### What if you want to change the environment?

please change the head part of environment.py, i.e. the initial position of predator or agent, and some other message like agent's viewable range.

### Other qustions?

The implementation of this version is very rough. If more questions, please connect with bozhouchen@hit.edu.cn.

## Cite

```latex
@article{DBLP:journals/corr/abs-2004-04376,
  author    = {Hongzhi Wang and
               Bozhou Chen and
               Yueyang Xu and
               Kaixin Zhang and
               Shengwen Zheng and
               Shirong Liu},
  title     = {ConsciousControlFlow(CCF): {A} Demonstration for conscious Artificial
               Intelligence},
  journal   = {CoRR},
  volume    = {abs/2004.04376},
  year      = {2020},
  url       = {https://arxiv.org/abs/2004.04376},
  archivePrefix = {arXiv},
  eprint    = {2004.04376},
  timestamp = {Tue, 14 Apr 2020 16:40:34 +0200},
  biburl    = {https://dblp.org/rec/journals/corr/abs-2004-04376.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

