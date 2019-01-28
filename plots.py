import numpy as np
import matplotlib.pyplot as plt
path = "784_300_10_batchsize_100_ReLU_softmax"
data = np.loadtxt("C:/Users/DerSc/OneDrive/Studium/CP3/Project/data/" + path + ".txt")
epochs = data[:, 0]
training_error = data[:, 1]
testing_error = data[:, 2]

plt.plot(epochs, testing_error*100, label="Testing set")
plt.plot(epochs, training_error*100, linestyle='dashed', label="Training set")
plt.legend()
plt.grid(color='grey', linestyle='dashed')
plt.ylim(2, 20)
plt.xlim(0, 50)
plt.xlabel("Epoch")
plt.ylabel("Error rate in %")
plt.savefig("C:/Users/DerSc/OneDrive/Studium/CP3/Project/media/plots/" + path + ".png")
plt.show()