from ltm import *
ltms = []

sleep = SLEEP()
hungry = ENERGY()
thirsty = WATER()
sexy = BREED()
tmp = [sleep,hungry,thirsty,sexy]
ltms += tmp

personalsafety = PERSONAL_SAFETY(tmp)
propertysafety = PROPERTY_SAFETY(tmp)
tmp = [personalsafety,propertysafety]
ltms += tmp

familyaffection = FAMILY_AFFECTION(tmp)
friendship = FRIENDSHIP(tmp)
love = LOVE(tmp)
tmp = [familyaffection,friendship,love]
ltms += tmp

respect = RESPECT(tmp)
ltms.append(respect)

from bayes_opt import BayesianOptimization
