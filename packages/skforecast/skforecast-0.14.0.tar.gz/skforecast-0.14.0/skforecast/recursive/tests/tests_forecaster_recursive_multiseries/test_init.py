# Unit test __init__ ForecasterRecursiveMultiSeries
# ==============================================================================
import re
import pytest
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from ....preprocessing import RollingFeatures
from ....recursive import ForecasterRecursiveMultiSeries


def test_init_ValueError_when_no_lags_or_window_features():
    """
    Test ValueError is raised when no lags or window_features are passed.
    """
    err_msg = re.escape(
        "At least one of the arguments `lags` or `window_features` "
        "must be different from None. This is required to create the "
        "predictors used in training the forecaster."
    )
    with pytest.raises(ValueError, match = err_msg):
        ForecasterRecursiveMultiSeries(
            regressor       = LinearRegression(),
            lags            = None,
            window_features = None
        )


@pytest.mark.parametrize("lags, window_features, expected", 
                         [(5, None, 5), 
                          (None, True, 6), 
                          ([], True, 6), 
                          (5, True, 6)], 
                         ids = lambda dt: f'lags, window_features, expected: {dt}')
def test_init_window_size_correctly_stored(lags, window_features, expected):
    """
    Test window_size is correctly stored when lags or window_features are passed.
    """
    if window_features:
        window_features = RollingFeatures(
            stats=['ratio_min_max', 'median'], window_sizes=[5, 6]
        )

    forecaster = ForecasterRecursiveMultiSeries(
                     regressor       = LinearRegression(),
                     lags            = lags,
                     window_features = window_features
                 )
    
    assert forecaster.window_size == expected
    if lags:
        np.testing.assert_array_almost_equal(forecaster.lags, np.array([1, 2, 3, 4, 5]))
        assert forecaster.lags_names == [f'lag_{i}' for i in range(1, lags + 1)]
        assert forecaster.max_lag == lags
    else:
        assert forecaster.lags is None
        assert forecaster.lags_names is None
        assert forecaster.max_lag is None
    if window_features:
        assert forecaster.window_features_names == ['roll_ratio_min_max_5', 'roll_median_6']
        assert forecaster.window_features_class_names == ['RollingFeatures']
    else:
        assert forecaster.window_features_names is None
        assert forecaster.window_features_class_names is None


@pytest.mark.parametrize("dif", 
                         [0, 0.5, 1.5, 'not_int'], 
                         ids = lambda dif: f'differentiation: {dif}')
def test_init_ValueError_when_differentiation_argument_is_not_int_or_greater_than_0(dif):
    """
    Test ValueError is raised when differentiation is not an int or greater than 0.
    """
    err_msg = re.escape(
        f"Argument `differentiation` must be an integer equal to or "
        f"greater than 1. Got {dif}."
    )
    with pytest.raises(ValueError, match = err_msg):
        ForecasterRecursiveMultiSeries(
            regressor       = LinearRegression(),
            lags            = 5,
            differentiation = dif
        )


@pytest.mark.parametrize("dif", 
                         [1, 2], 
                         ids = lambda dif: f'differentiation: {dif}')
def test_init_window_size_is_increased_when_differentiation(dif):
    """
    Test window_size is increased when including differentiation.
    """
    forecaster = ForecasterRecursiveMultiSeries(
                     regressor       = LinearRegression(),
                     lags            = 5,
                     differentiation = dif
                 )
    
    assert forecaster.window_size == 5 + dif


def test_init_ValueError_invalid_encoding():
    """
    Test ValueError is raised when encoding is not valid.
    """

    err_msg = re.escape(
        "Argument `encoding` must be one of the following values: 'ordinal', "
        "'ordinal_category', 'onehot' or None. Got 'invalid_encoding'."
    )
    with pytest.raises(ValueError, match = err_msg):
        ForecasterRecursiveMultiSeries(
            regressor = LinearRegression(),
            lags      = [1, 2, 3],
            encoding  = 'invalid_encoding',
        )


def test_ForecasterRecursiveMultiSeries_init_not_scaling_with_linear_model():
    """
    Test Warning is raised when Forecaster has no transformer_series and it
    is using a linear model.
    """

    warn_msg = re.escape(
        "When using a linear model, it is recommended to use a transformer_series "
        "to ensure all series are in the same scale. You can use, for example, a "
        "`StandardScaler` from sklearn.preprocessing."
    )
    with pytest.warns(UserWarning, match = warn_msg):
        ForecasterRecursiveMultiSeries(
            regressor = LinearRegression(),
            lags      = [1, 2, 3]
        )


def test_init_TypeError_transformer_series_dict_encoding_None():
    """
    Test TypeError is raised when transformer_series is a dictionary 
    and encoding is None.
    """

    err_msg = re.escape(
        "When `encoding` is None, `transformer_series` must be a single "
        "transformer (not `dict`) as it is applied to all series."
    )
    with pytest.raises(TypeError, match = err_msg):
        ForecasterRecursiveMultiSeries(
            regressor          = LinearRegression(),
            lags               = [1, 2, 3],
            encoding           = None,
            transformer_series = {'1': StandardScaler(), '_unknown_level': StandardScaler()}
        )


def test_init_ValueError_transformer_series_dict_with_no_unknown_level():
    """
    Test ValueError is raised when transformer_series is a dictionary 
    and no '_unknown_level' key is provided.
    """

    err_msg = re.escape(
        "If `transformer_series` is a `dict`, a transformer must be "
        "provided to transform series that do not exist during training. "
        "Add the key '_unknown_level' to `transformer_series`. "
        "For example: {'_unknown_level': your_transformer}."
    )
    with pytest.raises(ValueError, match = err_msg):
        ForecasterRecursiveMultiSeries(
            regressor          = LinearRegression(),
            lags               = [1, 2, 3],
            encoding           = 'ordinal',
            transformer_series = {'1': StandardScaler()}
        )
