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
testing_set = mnist.read(dataset="testing", path="mnist")

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

data = list()
epochs = 10

for epoch in range(epochs+1):
    print(epoch)

    # Calculate the testing error rate
    num_wrong_test = 0
    for sample in testing_set:
        prediction = network.predict(sample[0])
        prediction = np.argmax(prediction)
        expectation = np.argmax(sample[1])
        if not prediction == expectation:
            num_wrong_test += 1

    # Calculate the training error rate
    num_wrong_train = 0
    for sample in training_set:
        prediction = network.predict(sample[0])
        prediction = np.argmax(prediction)
        expectation = np.argmax(sample[1])
        if not prediction == expectation:
            num_wrong_train += 1

    data.append([epoch, num_wrong_train / len(training_set), num_wrong_test / len(testing_set)])

    network.train(training_set, epochs=1, batchsize=batchsize, eta=0.005)

np.savetxt("data/test.txt", data)
network.save_state("states/test.state")
