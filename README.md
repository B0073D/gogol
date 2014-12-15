gogol
=======

Game of Game of Life

This is my attempt at using a genetic algorithm to create an optimal starting set.

TODO:
-----

- Currently no 'mating' only mutation (Emulates asexual cells??)
- Change tracking - Images of the leader are currently stored
- Fitness graphing - DONE in a roundabout hackish way
- Better gif creation. Currently using GIMP manually

Fitness Algorithms
-----

0:

This algorithm simply multiplies the number of iterations that life has survived with the amount of life.

1:

This algorithm multiplies the number of iterations with the inverse proportion of starting life to 'finishing' life. This theoretically encourages a smaller start point and more 'growth'

Examples
-----

- Leader for fitness algorithm 0

![alt tag](https://raw.github.com/B0073D/gogol/master/images/leader_0.gif)

- Leader for fitness algorithm 1

![alt tag](https://raw.github.com/B0073D/gogol/master/images/leader_1.gif)

Smaller examples:

- Leader for fitness algorithm 0

![alt tag](https://raw.github.com/B0073D/gogol/master/images/leader_0_small.gif)

- Leader for fitness algorithm 1

![alt tag](https://raw.github.com/B0073D/gogol/master/images/leader_1_small.gif)

Graph of Fitness of Population
-----
(Please keep in mind that all evolutions have various random factors, so any differences in these graphs [or any images here] may be purely coincidental)

- Algorithm 0

![alt tag](https://raw.github.com/B0073D/gogol/master/images/stats_0.jpg)

- Algorithm 1

![alt tag](https://raw.github.com/B0073D/gogol/master/images/stats_1.jpg)