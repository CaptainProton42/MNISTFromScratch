import mnist
import numpy as np
import random
import sys
import os
import matplotlib.pyplot as plt
sys.path.append("modules")
import mnist
import idx
sys.path.append("extension")
import pyceptron

imgs = idx.read("Survey/img.idx3-ubyte").body
lbls = idx.read("Survey/lbl.idx1-ubyte").body

dataset = []
for i in range(len(imgs)):
    lbl = [0] * 4
    lbl[lbls[i]] = 1
    dataset.append([list(imgs[i].flatten()), list(lbl)])

random.shuffle(dataset)

fraction_testing = 0.25
sep_index = int((1 - fraction_testing) * len(dataset))

testing_set = dataset[sep_index:]
training_set = dataset[0:sep_index]

architecture = [784, 100, 4]

network = pyceptron.Network(architecture, activation="ReLU", softmax=1)

random.seed()
for l in range(1, len(architecture)):
        for j in range(architecture[l]):
                network.set_bias(l, j, 0.1*(0.5-random.random()))
                for k in range(architecture[l-1]):
                        network.set_weight(l, j, k, 0.1*(0.5-random.random()))
                        pass

train_loss = []
test_loss = []

step = 1
tot_epochs = 50
for epochs in np.arange(0, tot_epochs, step):
        network.train(training_set, batchsize=1, eta=0.000005, epochs=step)

        num_wrong = 0
        for sample in testing_set:
                prediction = np.argmax(network.predict(sample[0]))
                target = np.argmax(sample[1])
                if not prediction == target:
                        num_wrong += 1
        
        test_loss.append(num_wrong / len(testing_set))

        num_wrong = 0
        for sample in training_set:
                prediction = np.argmax(network.predict(sample[0]))
                target = np.argmax(sample[1])
                if not prediction == target:
                        num_wrong += 1
        
        train_loss.append(num_wrong / len(training_set))

        os.system('cls')
        print('[', end='')
        for i in range(int(epochs/tot_epochs*20)):
                print('|', end='')

        for i in range(int(epochs/tot_epochs*20), 20):
                print(' ', end='')
        print(']')

plt.figure(1)
plt.plot(test_loss)
plt.plot(train_loss)
plt.show()

network.save_state("states/operators.state")