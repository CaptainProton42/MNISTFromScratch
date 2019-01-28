// #########################################################################
// #                                pyceptron.c                                 #
// #-----------------------------------------------------------------------#
// # Main code. Implements a fully connected neural network with backpro-  #
// # pagation and an optional softmax layer.                               #
// #########################################################################

#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include "activation.h"

/**
 * Node
 * ----
 * This implements one single node in the network.
 * 
 * o: Output value of the node.
 * w: Array holding the weights of the incoming connections.
 * w_grad: Array holding the error gradients of the weights.
 * b: Bias of incoming connections.
 * grad_b: Error gradient of the bias.
 * z: Net input of the nodes.
 * initLayer: Function pointer to the initialization function of the node.
 */

typedef struct nodeStruct {
    double o; /* Node output */

    double *w; /* Input weights */
    double *grad_w; /* Input weight gradients */
    double b; /* Input bias */
    double grad_b; /* Input bias gradient */

    void (*initNode)(struct nodeStruct *self, int numberOfPreviousNodes);
} Node;

/**
 * initializeNode
 * --------------
 * Standard initialization function for a Node.
 * 
 * self: Pointer to the node.
 * numberOfPreviousNodes: Number of nodes in the previous layer.
 *                        This is needed for the weights.
 */

void initializeNode(struct nodeStruct *self, int numberOfPreviousNodes)
{
    self->o = 0.0;
    self->b = 0.0;
    self->grad_b = 0.0;

    self->w = (double *)malloc(numberOfPreviousNodes * sizeof(double));
    self->grad_w = (double *)malloc(numberOfPreviousNodes * sizeof(double));

    int k;
    for ( k = 0; k < numberOfPreviousNodes; k++ )
    {
        self->w[k] = 0.0;
        self->grad_w[k] = 0.0;
    }
}

/** 
 * Layer
 * ----
 * This defines the structure of a fully connected layer in the
 * network.
 * 
 * nodes: Nodes in layer
 */

typedef struct layerStruct {
    Node *nodes; /* Nodes in layer */

    void (*initLayer)(struct layerStruct *self, int numberOfNodes, int numberOfPreviousNodes);
} Layer;

/**
 * initializeLayer
 * --------------
 * Standard initialization function for a Layer.
 * 
 * self: Pointer to the layer.
 * numberOfNodes: Number of nodes in the new layer.
 * numberOfPreviousNodes: Number of nodes in the previous layer.
 *                        The node will be fully connected to them.
 */

void initializeLayer(struct layerStruct *self, int numberOfNodes, int numberOfPreviousNodes)
{
    self->nodes = (Node *)malloc(numberOfNodes * sizeof(Node));

    int j;
    for ( j = 0; j < numberOfNodes; j++ )
    {
        self->nodes[j].initNode = initializeNode;
        self->nodes[j].initNode(&self->nodes[j], numberOfPreviousNodes);
    }
}

/**
 * NetworkObject
 * -------------
 * Structure of the neural network as a whole (as a Python object).
 * 
 * nodes: Pointer to a two-dimensional array of all nodes/neurons in the network.
 * numLayer: Number of layers in the network (including input and output).
 * numNeurons: One-dimensional array holding the number of neurons for each layer.
 * activationFunc: Function pointer to the activation function.
 * activationFuncGradient: Function pointer to the gradient fo the activation function.
 */
typedef struct {
    PyObject_HEAD

    Layer *layers; /* array of layer objects */

    int numLayers; /* number of layers */
    int *numNeurons; /* number of neurons in each layer */

    double (*activationFunc)(double); /* activation function */
    double (*activationFuncGradient)(double); /* gradient of activation function */

    int softmax;    /* enable softmax? */
} NetworkObject;

/**
 * forwardfeed
 * -----------
 * Calculates the values of the output layer by forward feed.
 * 
 * self: Pointer to the neural network Python object.
 */
void forwardfeed(NetworkObject *self)
{
    int l, j;
    for ( l = 1; l < self->numLayers; l++ )
    {
        for ( j = 0; j < self->numNeurons[l]; j++ )
        {
            /* net input */            
            int i;
            double z = 0.0;
            for ( i = 0; i < self->numNeurons[l-1]; i++ )
            {
                z += self->layers[l].nodes[j].w[i] * self->layers[l-1].nodes[i].o;
            }

            z += self->layers[l].nodes[j].b;
            self->layers[l].nodes[j].o = self->activationFunc(z);
        }
    }
    return;
}

/**
 * softmax
 * -------
 * Applies softmax normalization to the output vector.
 * Backpropagation doesn't change for cross entropy.
 * 
 * self: Pointer to the neural network Python object.
 */
void softmax(NetworkObject *self)
{
    int l = self->numLayers-1;

    /* apply softmax */
    double z = 0;
    int j;
    for ( j = 0; j < self->numNeurons[l]; j++)
    {
        z += exp(self->layers[l].nodes[j].o);
    }

    for ( j = 0; j < self->numNeurons[l]; j++)
    {
        self->layers[l].nodes[j].o = exp(self->layers[l].nodes[j].o) / z;
    }
}

/**
 * delta
 * -----
 * The "delta" tensor for backpropagation.
 * 
 * self: Pointer to the neural network Python object.
 * l: Target layer.
 * j: Target node.
 * output: Target output vector.
 */
double delta(NetworkObject *self, int l, int j, double *output)
{
    if ( l < self->numLayers-1)
    {
        double sum = 0;
        int i;
        for ( i = 0; i < self->numNeurons[l+1]; i++ )
        {
            sum += delta(self, l+1, i, output) * self->layers[l+1].nodes[i].w[j];
        }
        return sum * self->activationFuncGradient(self->layers[l].nodes[j].o);
    }
    else
    {
        /* The same for square error and softmax with cross entropy. */
        return self->activationFuncGradient(self->layers[l].nodes[j].o) * (self->layers[l].nodes[j].o - output[j]);
    }
}

/**
 * backpropagation
 * ---------------
 * Executes a full backpropagation in the current state of the network and sets all gradients accordingly.
 * 
 * self: Pointer to the neural network Python object.
 * output: Target output vector.
 * numSets: Numver of training sets (only used for gradient calculation).
 */

void backpropagation(NetworkObject *self, double *output)
{
    int l, j, k; /* target indices */

    /* back propagation */
    /* compute weight gradients */
    for ( l = 1; l < self->numLayers ; l++ )   /* target layer */
    {
        for ( j = 0; j < self->numNeurons[l]; j++)   /* target neuron */
        {
            double d = delta(self, l, j, output);
            for ( k = 0; k < self->numNeurons[l-1]; k++ ) /* previous neuron */
            {
                self->layers[l].nodes[j].grad_w[k] += d * self->layers[l-1].nodes[k].o;
            }
            self->layers[l].nodes[j].grad_b += d;
        }
    }
}

/**
 * Network_new
 * -----------
 * Creates a new neural network and returns the created network as a Python object.
 * 
 * architecture: Python list the length of the layer number containing the number of nodes in each layer.
 * activation: "sigmoid" or "tanh", activation function is chosen accordingly.
 * 
 * Returns:
 *  Python object representing the network.
 */
static PyObject* Network_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    NetworkObject *self;
    self = (NetworkObject *) type->tp_alloc(type, 0);

    static char *kwlist[] = {"architecture", "activation", "softmax", NULL};

    PyObject * listObj; /* the list of strings */
    char * actString = "sigmoid";
    int softmax = 0; /* should there be a softmax layer? */

    if (! PyArg_ParseTupleAndKeywords( args, kwargs, "O!|si", kwlist, &PyList_Type, &listObj, &actString, &softmax )) return NULL;

    if (strcmp(actString, "sigmoid") == 0)
    {
        self->activationFunc = &act_sigmoid;
        self->activationFuncGradient = &act_sigmoid_grad;
    }
    else if (strcmp(actString, "tanh") == 0)
    {
        self->activationFunc = &act_tanh;
        self->activationFuncGradient = &act_tanh_grad;
    }
    else if (strcmp(actString, "ReLU") == 0)
    {
        self->activationFunc = &act_relu;
        self->activationFuncGradient = &act_relu_grad;
    }
    else if (strcmp(actString, "Leaky ReLU") == 0)
    {
        self->activationFunc = &act_leaky_relu;
        self->activationFuncGradient = &act_leaky_relu_grad;
    }
    else if (strcmp(actString, "linear") == 0)
    {
        self->activationFunc = &act_linear;
        self->activationFuncGradient = &act_linear_grad;
    }
    else
    {
        PyErr_SetString(PyExc_ValueError, "Unknown activation function!");
        return NULL;
    }

    self->softmax = softmax;

    /* get the number of lines passed to us */
    self->numLayers = PyList_Size(listObj);

    self->numNeurons = (int *)malloc(self->numLayers * sizeof(int));

    /* build the neural network */
    self->layers = (Layer *)malloc(self->numLayers * sizeof(Layer));

    int l;
    for ( l = 0; l < self->numLayers; l++ )   /* set neurons in layers */
    {
        PyObject* listItem = PyList_GetItem(listObj, l);
        self->numNeurons[l] = PyLong_AsLong(listItem);


        self->layers[l].initLayer = initializeLayer;
        if ( l > 0)
        {
            self->layers[l].initLayer(&self->layers[l], self->numNeurons[l], self->numNeurons[l-1]);
        }
        else /* no input weights/biases */
        {
            self->layers[l].initLayer(&self->layers[l], self->numNeurons[l], 1);
        }
    }

    return (PyObject *) self;
}

/**
 * Network_predict
 * ---------------
 * Makes a single prediction using the current network configuration.
 * 
 * listObj: Input vector as Python list.
 * 
 * Returns:
 *  Output vector as Python list.
 */
static PyObject* Network_predict(NetworkObject *self, PyObject *args)
{
    PyObject *listObj;
    if (! PyArg_ParseTuple( args, "O!", &PyList_Type, &listObj)) return NULL;

    long inputDim = PyList_Size(listObj);

    if ( inputDim != self->numNeurons[0] )
    {
        PyErr_SetString(PyExc_ValueError, "Input dimension must match the input layers dimension!");
        return NULL;
    }

    double* input = (double *)malloc(inputDim * sizeof(double));
    int i;
    for ( i = 0; i < inputDim; i++ )
    {
        PyObject *itemObj = PyList_GetItem(listObj, i);
        input[i] = PyFloat_AsDouble(itemObj);
    }

    int j;
    for ( j = 0; j < self->numNeurons[0]; j++ )
    {
        self->layers[0].nodes[j].o = input[j];
    }

    forwardfeed(self);
    if (self->softmax) softmax(self);

    PyObject* outputList = PyList_New(0);
    for ( j = 0; j < self->numNeurons[self->numLayers-1]; j++ )
    {
        PyObject* objItem = PyFloat_FromDouble(self->layers[self->numLayers-1].nodes[j].o);
        int result = PyList_Append(outputList, objItem);
    }

    free(input);

    return outputList;
}

/**
 * Network_train
 * -------------
 * Trains the network using the supplied training sets.
 * 
 * listObj: Nested Python list containing input and target output vectors of each set.
 * epochs: Number of epochs to train for.
 * eta: Learning rate used for training.
 */
static PyObject* Network_train(NetworkObject *self, PyObject *args, PyObject *kwargs)
{
    long epochs;
    long batchsize;
    double eta;

    PyObject *listObj;

    static char *kwlist[] = {"set", "epochs", "batchsize", "eta", NULL};

    if (! PyArg_ParseTupleAndKeywords( args, kwargs, "O!lld", kwlist, &PyList_Type, &listObj, &epochs, &batchsize, &eta)) return NULL;

    int numSamples = PyList_Size(listObj);
    double** inputs = (double **)malloc(numSamples * sizeof(double *));
    double** outputs = (double **)malloc(numSamples * sizeof(double *));

    int i;
    for ( i = 0; i < numSamples; i++ )
    {
        PyObject *IoTuple = PyList_GetItem(listObj, i);
        PyObject* inputVectorItem = PyList_GetItem(IoTuple, 0);
        PyObject* outputVectorItem = PyList_GetItem(IoTuple, 1);
        long inputDim = PyList_Size(inputVectorItem);
        long outputDim = PyList_Size(outputVectorItem);

        if ( inputDim != self->numNeurons[0] )
        {
            PyErr_SetString(PyExc_ValueError, "Input dimension must match the input layers dimension!");
            return NULL;
        }

        if ( outputDim != self->numNeurons[self->numLayers-1] )
        { 
            PyErr_SetString(PyExc_ValueError, "Output dimnesion must match the output layers dimension!");
            return NULL;
        }

        inputs[i] = (double *)malloc(inputDim * sizeof(double));
        outputs[i] = (double *)malloc(outputDim * sizeof(double));

        int j;
        for ( j = 0; j < inputDim; j++ )
        {
            PyObject* inputItem = PyList_GetItem(inputVectorItem, j);
            double input = PyFloat_AsDouble(inputItem);
            inputs[i][j] = input;
        }

        for ( j = 0; j < outputDim; j++ )
        {
            PyObject* outputItem = PyList_GetItem(outputVectorItem, j);
            double output = PyFloat_AsDouble(outputItem);
            outputs[i][j] = output;
        }
    }

    int epoch;
    for (epoch = 0; epoch < epochs; epoch++ )
    {
        int batch;
        int sampleInBatch, sample;
        int l, j, k;
        for (batch = 0; batch < numSamples / batchsize; batch++ )
        {
            for ( sampleInBatch = 0; sampleInBatch < batchsize; sampleInBatch++ )
            {
                sample = sampleInBatch + batch * batchsize; // mini-batch offset

                for ( j = 0; j < self->numNeurons[0]; j++ )
                {
                    self->layers[0].nodes[j].o = inputs[sample][j];
                }

                forwardfeed(self);
                if (self->softmax) softmax(self);
                backpropagation(self, outputs[sample]);
            }
            
            /* apply weight gradients and set to 0 for next batch */
            for ( l = 1; l < self->numLayers ; l++ )   /* weight to layer */
            {
                for ( j = 0; j < self->numNeurons[l]; j++)   /* to neuron */
                {
                    self->layers[l].nodes[j].b -= eta / batchsize * self->layers[l].nodes[j].grad_b;
                    self->layers[l].nodes[j].grad_b = 0.0;
                    for ( k = 0; k < self->numNeurons[l-1]; k++ ) /* from neuron */
                    {
                        self->layers[l].nodes[j].w[k] -= eta / batchsize * self->layers[l].nodes[j].grad_w[k];
                        self->layers[l].nodes[j].grad_w[k] = 0.0;
                    }
                }
            }
        }
    }

    for ( i = 0; i < numSamples; i++ )
    {
        free(inputs[i]);
        free(outputs[i]);
    }
    free(inputs);
    free(outputs);
    return Py_None;
}

/**
 * Network_set_weight
 * ------------------
 * Manually set a single weight of the network.
 * 
 * l: Layer of the weights target node.
 * j: Index of the weights target node in layer.
 * k: Index of the weights origin node in layer.
 * new_weight: New weight to set.
 */
static PyObject* Network_set_weight(NetworkObject *self, PyObject *args)
{
    int l;  /* to layer */
    int j;  /* to neuron */
    int k;  /* from neuron */
    double new_weight;

    if (! PyArg_ParseTuple(args, "iiid", &l, &j, &k, &new_weight)) return NULL;

    if ( l == 0 || l > self->numLayers-1 || j > self->numNeurons[l] - 1 || k > self->numNeurons[l-1] - 1 )
    {
        PyErr_SetString(PyExc_ValueError, "One ore more indices are out of bounds!");
        return NULL;
    }

    self->layers[l].nodes[j].w[k] = new_weight;

    Py_INCREF(Py_None);
    return Py_None;
}

/**
 * Network_set_bias
 * ----------------
 * Manually set a single bias of the network.
 * 
 * l: Layer of the biases node.
 * j: Index of the biases node in layer.
 * new_bias: New bias to set.
 */
static PyObject* Network_set_bias(NetworkObject *self, PyObject *args)
{
    int l;  /* to layer */
    int j;  /* to neuron */

    double new_bias;

    if (! PyArg_ParseTuple(args, "iid", &l, &j, &new_bias)) return NULL;

    if ( l == 0 || l > self->numLayers-1 || j > self->numNeurons[l] - 1 )
    {
        PyErr_SetString(PyExc_ValueError, "One ore more indices are out of bounds!");
        return NULL;
    }

    self->layers[l].nodes[j].b = new_bias;

    Py_INCREF(Py_None);
    return Py_None;
}

/**
 * Network_get_weight
 * ------------------
 * Returns the value a single weight in the network.
 * 
 * l: Layer of the weights target node.
 * j: Index of the weights target node in layer.
 * k: Index of the weights origin node in layer.
 */
static PyObject* Network_get_weight(NetworkObject *self, PyObject *args)
{
    int l;  /* to layer */
    int j;  /* to neuron */
    int k;  /* from neuron */

    if (! PyArg_ParseTuple(args, "iii", &l, &j, &k)) return NULL;

    if ( l == 0 || l > self->numLayers-1 || j > self->numNeurons[l] - 1 || k > self->numNeurons[l-1] - 1 )
    {
        PyErr_SetString(PyExc_ValueError, "One ore more indices are out of bounds!");
        return NULL;
    }

    return Py_BuildValue("d", self->layers[l].nodes[j].w[k]);
}

/**
 * Network_save_state
 * ------------------
 * Saves all biases and weights of the network to a file a the supplied location.
 * 
 * filePath: path to the file to which to save to
 */
static PyObject* Network_save_state(NetworkObject *self, PyObject *args)
{
    char *filePath;

    if (!PyArg_ParseTuple(args, "s", &filePath)) return NULL;

    FILE *fp = fopen(filePath, "wb");

    int l;
    int j;
    int k;
    for ( l = 1; l < self->numLayers; l++ )
    {
        for ( j = 0; j < self->numNeurons[l-1]; j++ )
        {
            for ( k = 0; k < self->numNeurons[l]; k++ )
            {
                fwrite(&self->layers[l].nodes[k].w[j], sizeof(double), 1, fp);
            }
        }
    }

    for ( l = 1; l < self->numLayers; l++ )
    {
        for ( j = 0; j < self->numNeurons[l]; j++ )
        {
            fwrite(&self->layers[l].nodes[j].b, sizeof(double), 1, fp);
        }
    }
    
    fclose(fp);

    Py_INCREF(Py_None);
    return Py_None;
}

/**
 * Network_load_state
 * ------------------
 * Tries to read weights and biases from a file at the supplied location and
 * applies them to the network. Checks only whether the file you're trying
 * to load has the correct size so make sure you're using the correct file.
 * 
 * filePath: path to the file to which to save to
 */
static PyObject* Network_load_state(NetworkObject *self, PyObject *args)
{
    char *filePath;

    if (!PyArg_ParseTuple(args, "s", &filePath)) return NULL;

    FILE *fp = fopen(filePath, "rb");

    int l;
    int j;
    int k;

    long exptectedFileSize = 0;

    for ( l = 1; l < self->numLayers; l++ )
    {
        exptectedFileSize += self->numNeurons[l]; /* number of biases */
        exptectedFileSize += self->numNeurons[l] * self->numNeurons[l-1] ;/* number of weights */
    }
    exptectedFileSize *= sizeof(double);

    long fileSize = 0;
    fseek(fp, 0L, SEEK_END);
    fileSize = ftell(fp);
    rewind(fp);

    if ( fileSize != exptectedFileSize )
    {
        PyErr_SetString(PyExc_ValueError, "The file size doesn't match the expected value for this network.");
        return NULL;       
    }

    for ( l = 1; l < self->numLayers; l++ )
    {
        for ( j = 0; j < self->numNeurons[l-1]; j++ )
        {
            for ( k = 0; k < self->numNeurons[l]; k++ )
            {
                fread(&self->layers[l].nodes[k].w[j], sizeof(double), 1, fp);
            }
        }
    }

    for ( l = 1; l < self->numLayers; l++ )
    {
        for ( j = 0; j < self->numNeurons[l]; j++ )
        {
            fread(&self->layers[l].nodes[j].b, sizeof(double), 1, fp);
        }
    }
    
    fclose(fp);

    Py_INCREF(Py_None);
    return Py_None;    
}


/**
 * Network_methods
 * ---------------
 * Python method definitions that will be exposed by the Python network object.
 */
static PyMethodDef Network_methods[] = {
    {"predict", (PyCFunction)Network_predict, METH_VARARGS,
     "Forward feed prediction."
    },
    {"train", (PyCFunction)Network_train, METH_VARARGS | METH_KEYWORDS,
     "Train the network."
    },
    {
    "set_weight", (PyCFunction)Network_set_weight, METH_VARARGS,
    "Set a weight manually."
    },
    {
    "set_bias",(PyCFunction)Network_set_bias, METH_VARARGS,
    "Set a bias manually."
    },
    {
    "get_weight", (PyCFunction)Network_get_weight, METH_VARARGS,
    "Get a single weight."
    },
    {"save_state", (PyCFunction)Network_save_state, METH_VARARGS,
    "Saves the current weights and biases to disk."
    },
    {
    "load_state", (PyCFunction)Network_load_state, METH_VARARGS,
    "Loads weights and biases from disk."
    },
    {NULL}  /* Sentinel */
};

/**
 * NetworkType
 * -----------
 * Python type definition for NetworkObject.
 */
static PyTypeObject NetworkType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "pyceptron.Network",
    .tp_doc = "Perceptron for Python.",
    .tp_basicsize = sizeof(NetworkObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = (PyCFunction)Network_new,
    .tp_methods = Network_methods,
};

/**
 * pyceptron
 * ----
 * Python extension definitions.
 */
static struct PyModuleDef pyceptron =
{
    PyModuleDef_HEAD_INIT,
    "pyceptron", // name of the module
    "Perceptron for Python.",  // description
    -1,		// size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
};

/**
 * PyInit_pyceptron
 * -----------
 * Extension initialization.
 */
PyMODINIT_FUNC PyInit_pyceptron(void)
{
    PyObject *m;
    if (PyType_Ready(&NetworkType) < 0)
        return NULL;

    m = PyModule_Create(&pyceptron);
    if (m == NULL)
        return NULL;

    Py_INCREF(&NetworkType);
    PyModule_AddObject(m, "Network", (PyObject *) &NetworkType);
    return m;
}