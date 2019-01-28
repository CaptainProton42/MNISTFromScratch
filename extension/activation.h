// #########################################################################
// #                             activation.h                              #
// #-----------------------------------------------------------------------#
// # Activation functions are defined here. There are two functions for    #
// # each activation function: The function itself and its gradient        #
// # expressed as dependent of the function output.                        #
// #########################################################################

#ifndef ACTIVATION_H
#define ACTIVATION_H

#include <math.h>

/* Sigmoid activation function */
double act_sigmoid(double z)
{
    return 1 / ( 1 + exp(-z) );
}

double act_sigmoid_grad(double sigma_z)
{
    return sigma_z * (1 - sigma_z );
}

/* tanh activation function */
double act_tanh(double z)
{
    return 0.5 * (1. + tanh(z));
}

double act_tanh_grad(double sigma_z)
{
    return 0.5 - 0.5 * sigma_z*sigma_z;
}

/* ReLU activation function */
double act_relu(double z)
{
    return fmax(0, z);
}

double act_relu_grad(double sigma_z)
{
    if ( sigma_z > 0 )
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

/* Leaky ReLU activation function*/
double act_leaky_relu(double z)
{
    if ( z > 0 )
    {
        return z;
    }
    else
    {
        return 0.01*z;
    }
}

double act_leaky_relu_grad(double sigma_z)
{
    if ( sigma_z > 0 )
    {
        return 1;
    }
    else
    {
        return 0.01;
    }
}

/* Linear activation function */
double act_linear(double z)
{
    return z;
}

double act_linear_grad(double sigma_z)
{
    return 1;
}

#endif