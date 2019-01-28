import numpy
import time
import datetime
import sys
sys.path.append("extension")
import pyceptron
sys.path.append("modules")
import mnist

import numpy as np
import random
import datetime
import sys
sys.path.append("modules")
import mnist
sys.path.append("extension")
import pyceptron

# Read the training and testing set

training_set = mnist.read(dataset="training", path="mnist")

architecture = [784, 10]
activation = "ReLU"
softmax = 1

batchsize=1

network = pyceptron.Network(architecture, activation=activation, softmax=softmax)

random.seed()
for l in range(1, len(architecture)):
        for j in range(architecture[l]):
                for k in range(architecture[l-1]):
                        network.set_weight(l, j, k, 0.5-random.random())
                network.set_bias(l, j, 0.5-random.random())

init_time = time.clock()

network.train(training_set, epochs=1, batchsize=batchsize, eta=0.005)

end_time = time.clock()
process_time = end_time - init_time

print(datetime.datetime.now())
print("Ellapsed time: %.3f s" % (process_time))
print("Pasthrough: %.3f img/s" % (60000/process_time))