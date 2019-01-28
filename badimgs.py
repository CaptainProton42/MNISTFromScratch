import sys
import numpy as np
import scipy.misc
import imageio
sys.path.append("modules")
import mnist
sys.path.append("extension")
import pyceptron

training_set = mnist.read(dataset="training", path="mnist")
testing_set = mnist.read(dataset="testing", path="mnist")

architecture = [784, 300, 10]
activation = "ReLU"
softmax = 1

network = pyceptron.Network(architecture, activation=activation, softmax=softmax)
network.load_state("states/784_300_10_sgd_ReLU_softmax_229.state")

bad_lbl = list()
bad_img = list()
print(len(testing_set))
# Calculate the training error rate
for i in range(len(testing_set)):
    sample = testing_set[i]
    prediction = network.predict(sample[0])
    prediction = np.argmax(prediction)
    expectation = np.argmax(sample[1])
    if not prediction == expectation:
        bad_lbl.append(np.argmax(sample[1]))
        bad_img.append(sample[0])

num_wrong = len(bad_lbl)
print(num_wrong)
sort = np.array(bad_lbl).argsort()
bad_img = np.array(bad_img)[sort]
sidelen = int(np.ceil(np.sqrt(num_wrong)))
collage = np.zeros((28*sidelen, 28*sidelen))

for y in range(sidelen):
    for x in range(sidelen):
        if sidelen * x + y < num_wrong:
            sample = bad_img[sidelen * x + y]
            sample = 1.0 - np.array(sample).reshape(28, 28)
            collage[28*x:28*(x+1), 28*y:28*(y+1)] = sample
        else:
            collage[28*x:28*(x+1), 28*y:28*(y+1)] = 1.0

imageio.imwrite('badimgs/bad.png', collage)