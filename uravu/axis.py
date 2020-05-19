"""
The Axis class controls the organisation of axes in the uravu code.
"""

# Copyright (c) Andrew R. McCluskey
# Distributed under the terms of the MIT License
# author: Andrew R. McCluskey


import numpy as np
from uravu import UREG
from uravu.distribution import Distribution
from scipy.stats import gaussian_kde


class Axis:
    """
    The Axes class is a flexible storage option for both numerical (:py:class:`numpy.ndarray`) and distribution (:py:class:`uravu.distribution.Distribution`) arrays. 

    Attributes:
        values (:py:attr:`list` or :py:class:`uravu.distribution.Distribution` or :py:attr:`array_like`): Array of values.
        kde (:py:class:`scipy.stats.kde.gaussian_kde`): Multi-dimensional kernal density approximation for the axes. 

    Args:
        values (:py:attr:`list` or :py:class:`uravu.distribution.Distribution` or :py:attr:`array_like`): Array of values.
    """
    def __init__(self, values):
        """
        Initialisation function for a :py:class:`~uravu.axis.Axis` object.
        """
        self.kde = None
        if isinstance(values[0], Distribution):
            self.values = values
            self.kde = _get_kde(self.values)
        else:
            self.values = np.array(values)

    @property
    def n(self):
        """
        Get the median of each value in the axis.

        Returns:
            :py:attr:`array_like`: Medians for axis.
        """
        v = np.zeros(self.shape)
        if isinstance(self.values[0], Distribution):
            for i, o in enumerate(self.values):
                v[i] = o.n
            return v 
        else:
            return self.values
    
    @property
    def s(self):
        """
        Get the uncertainty from confidence intervals of each value in the axis.

        Returns:
            :py:attr:`array_like`: Uncertainties for axis.
        """
        if isinstance(self.values[0], Distribution):
            dv = np.zeros((2, self.size))
            for i, o in enumerate(self.values):
                dv[:, i] = np.abs(o.con_int - o.n)
            return dv 
        else:
            return np.zeros(self.shape)

    @property
    def size(self):
        """
        Get the axis size.

        Returns:
            :py:attr:`int`: Size of axis.
        """
        if isinstance(self.values[0], Distribution):
            return len(self.values)
        else:
            return self.values.size

    @property
    def shape(self):
        """
        Get the axis shape.

        Returns:
            :py:attr:`int`: Shape of axis.
        """
        if isinstance(self.values[0], Distribution):
            return len(self.values)
        else:
            return self.values.shape

    def pdf(self, x):
        """"
        Get the probability density function for all of the distributions in the axes.

        Args:
            x (:py:attr:`array_like`): Values to return probability of.
        
        Return:
            :py:attr:`array_like`: Probability.
        """
        return self.kde.pdf(x)

    def logpdf(self, x):
        """"
        Get the natural log probability density function for all of the distributions in the axes.

        Args:
            x (:py:attr:`array_like`): Values to return natural log probability of.
        
        Return:
            :py:attr:`array_like`: Natural log probability.
        """
        return self.kde.logpdf(x)


def _get_kde(values):
    min_size = values[0].size
    for v in values:
        if v.size < min_size:
            min_size = v.size
    random_list = [np.random.choice(v.samples, size=min_size) for v in values]
    return gaussian_kde(np.vstack(random_list)) 
