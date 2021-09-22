## HW2 | 9/23 | Andy Chuang, Josh Jeon, Cliff Lin
"""
1. Page Rank is an algorithm which allows Google Search to rank web pages in their search results. 
-Works by counting the number and quality of links to a page => rough estimate of importance of website
-links analysis algorithm
-assigns numerical weighting to each element of a hyperlinked set of docs
-purpose is to measure relative importance within the set
-outputs a probability distribution used to represent the likelihood that a person randomly
clicking on links will arrive on a particular page. EX: document with PageRank of 0.5 = 50% chance that 
person clicking on random link will be directed to said document.
"""

"""
2. A good "metaphor" for using Markov chains in the ranking problem could be a "bandwagon fan," a fan who tends to support
whichever team is doing better. Each team starts with the same amount of fans - each fan has the choice to change teams or
stay with their current team. They can choose after each iteration.
"""

import pandas as pd
import numpy as np