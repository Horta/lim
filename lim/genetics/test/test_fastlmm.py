from __future__ import division

import numpy as np
from numpy.testing import assert_almost_equal

from ..fastlmm import FastLMM
from ...util.fruits import Apples
from ...cov import LinearCov
from ...cov import EyeCov
from ...cov import SumCov
from ...mean import OffsetMean
from ...random import RegGPSampler
from ...random import FastLMMSampler

def test_learn():
    random = np.random.RandomState(9458)
    N = 800
    X = random.randn(N, 900)
    X -= X.mean(0)
    X /= X.std(0)
    X /= np.sqrt(X.shape[1])
    offset = 1.2

    mean = OffsetMean()
    mean.offset = offset
    mean.set_data(N, purpose='sample')

    cov_left = LinearCov()
    cov_left.scale = 1.5
    cov_left.set_data((X, X), purpose='sample')

    cov_right = EyeCov()
    cov_right.scale = 1.5
    cov_right.set_data((Apples(N), Apples(N)), purpose='sample')

    cov = SumCov([cov_left, cov_right])

    y = RegGPSampler(mean, cov).sample(random)

    flmm = FastLMM(y, X)
    flmm.learn()

    assert_almost_equal(flmm.offset, 1.2120718670, decimal=6)
    assert_almost_equal(flmm.genetic_variance, 1.2979613599, decimal=5)
    assert_almost_equal(flmm.noise_variance, 1.6317660354, decimal=5)

def test_predict():
    random = np.random.RandomState(228)
    N = 800
    X = random.randn(N, 900)

    offset = 1.2
    scale = 3.0
    delta = 0.5
    y = FastLMMSampler(offset, scale, delta, X).sample(random)

    flmm = FastLMM(y, X)
    flmm.learn()
    assert_almost_equal(flmm.predict(X).logpdf(y), -1092.1273501778442,
                        decimal=5)
