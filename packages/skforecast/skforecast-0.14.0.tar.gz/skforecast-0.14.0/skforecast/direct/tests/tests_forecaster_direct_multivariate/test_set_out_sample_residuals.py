# Unit test set_out_sample_residuals ForecasterDirectMultiVariate
# ==============================================================================
import re
import pytest
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.exceptions import NotFittedError
from sklearn.preprocessing import StandardScaler
from skforecast.direct import ForecasterDirectMultiVariate

# Fixtures
series = pd.DataFrame({'l1': pd.Series(np.arange(15)), 
                       'l2': pd.Series(np.arange(15))})


def test_set_out_sample_residuals_NotFittedError_when_forecaster_not_fitted():
    """
    Test NotFittedError is raised when forecaster is not fitted.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2
    )
    y_true = {1: np.array([1, 2, 3, 4, 5]), 2: np.array([1, 2, 3, 4, 5])}
    y_pred = {1: np.array([1, 2, 3, 4, 5]), 2: np.array([1, 2, 3, 4, 5])}

    err_msg = re.escape(
        ("This forecaster is not fitted yet. Call `fit` with appropriate "
         "arguments before using `set_out_sample_residuals()`.")
    )
    with pytest.raises(NotFittedError, match = err_msg):
        forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)


def test_set_out_sample_residuals_TypeError_when_y_true_is_not_dict():
    """
    Test TypeError is raised when y_true is not a dict.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2
    )
    forecaster.is_fitted = True
    y_true = 'not_dict'
    y_pred = {1: np.array([1, 2, 3, 4, 5]), 2: np.array([1, 2, 3, 4, 5])}

    err_msg = re.escape(
        f"`y_true` must be a dictionary of numpy ndarrays or pandas Series. "
        f"Got {type(y_true)}."
    )
    with pytest.raises(TypeError, match = err_msg):
        forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)


def test_set_out_sample_residuals_TypeError_when_y_pred_is_not_dict():
    """
    Test TypeError is raised when y_pred is not a dict.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2
    )
    forecaster.is_fitted = True
    y_true = {1: np.array([1, 2, 3, 4, 5]), 2: np.array([1, 2, 3, 4, 5])}
    y_pred = 'not_dict'

    err_msg = re.escape(
        f"`y_pred` must be a dictionary of numpy ndarrays or pandas Series. "
        f"Got {type(y_pred)}."
    )
    with pytest.raises(TypeError, match = err_msg):
        forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)


def test_set_out_sample_residuals_ValueError_when_y_pred_and_y_true_keys_do_not_match():
    """
    Test TypeError is raised when y_pred and y_true keys do not match.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2
    )
    forecaster.is_fitted = True
    y_true = {1: np.array([1, 2, 3, 4, 5]), 2: np.array([1, 2, 3, 4, 5])}
    y_pred = {3: np.array([1, 2, 3, 4, 5]), 4: np.array([1, 2, 3, 4, 5])}

    err_msg = re.escape(
        f"`y_true` and `y_pred` must have the same keys. "
        f"Got {set(y_true.keys())} and {set(y_pred.keys())}."
    )
    with pytest.raises(ValueError, match = err_msg):
        forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)


def test_set_out_sample_residuals_TypeError_when_y_true_contains_no_numpy_ndarrays_or_pandas_series():
    """
    Test TypeError is raised when y_true contains no numpy ndarrays or pandas series.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2
    )
    forecaster.is_fitted = True
    y_true = {1: 'not_ndarray'}
    y_pred = {1: np.array([1, 2, 3, 4, 5])}

    err_msg = re.escape(
        f"Values of `y_true` must be numpy ndarrays or pandas Series. "
        f"Got {type(y_true[1])} for step 1."
    )
    with pytest.raises(TypeError, match = err_msg):
        forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)


def test_set_out_sample_residuals_TypeError_when_y_pred_contains_no_numpy_ndarrays_or_pandas_series():
    """
    Test TypeError is raised when y_pred contains no numpy ndarrays or pandas series.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2
    )
    forecaster.is_fitted = True
    y_true = {1: np.array([1, 2, 3, 4, 5])}
    y_pred = {1: 'not_ndarray'}

    err_msg = re.escape(
        f"Values of `y_pred` must be numpy ndarrays or pandas Series. "
        f"Got {type(y_pred[1])} for step 1."
    )
    with pytest.raises(TypeError, match = err_msg):
        forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)


def test_set_out_sample_residuals_ValueError_when_y_true_and_y_pred_have_elements_with_different_lengths():
    """
    Test ValueError is raised when y_true and y_pred have elements with different lengths.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2
    )
    forecaster.is_fitted = True
    y_true = {1: np.array([1, 2, 3, 4, 5]), 2: np.array([1, 2, 3, 4, 5])}
    y_pred = {1: np.array([1, 2, 3, 4, 5]), 2: np.array([1, 2])}

    err_msg = re.escape(
        f"`y_true` and `y_pred` must have the same length. "
        f"Got {len(y_true[2])} and {len(y_pred[2])} for step 2."
    )
    with pytest.raises(ValueError, match = err_msg):
        forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)


def test_set_out_sample_residuals_ValueError_when_y_true_and_y_pred_have_series_with_different_indexes():
    """
    Test ValueError is raised when y_true and y_pred have series with different indexes.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2
    )
    forecaster.is_fitted = True
    y_true = {1: pd.Series([1, 2, 3, 4, 5], index=[1, 2, 3, 4, 5])}
    y_pred = {1: pd.Series([1, 2, 3, 4, 5])}

    err_msg = re.escape(
        "When containing pandas Series, elements in `y_true` and "
        "`y_pred` must have the same index. Error in step 1."
    )
    with pytest.raises(ValueError, match = err_msg):
        forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)


def test_set_out_sample_residuals_ValueError_when_inputs_does_not_match_any_step():
    """
    Test ValueError is raised when inputs does not contain keys that match any step.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2
    )
    forecaster.fit(series=series)
    y_true = {5: np.array([1, 2, 3])}
    y_pred = {5: np.array([1, 2, 3])}

    err_msg = re.escape(
                "Provided keys in `y_pred` and `y_true` do not match any step. "
                "Residuals cannot be updated."
    )
    with pytest.raises(ValueError, match = err_msg):
        forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)


def test_set_out_sample_residuals_when_residuals_length_is_less_than_10000_and_no_append():
    """
    Test residuals stored when new residuals length is less than 10000 and append is False.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2,
        transformer_series=None
    )
    forecaster.fit(series=series)
    y_true = {1: np.array([1, 2, 3, 4, 5]), 2: np.array([2, 3, 4, 5, 6])}
    y_pred = {1: np.array([0, 1, 2, 3, 4]), 2: np.array([0, 1, 2, 3, 4])}

    forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)
    expected = {1: np.array([1, 1, 1, 1, 1]), 2: np.array([2, 2, 2, 2, 2])}
    results = forecaster.out_sample_residuals_

    assert expected.keys() == results.keys()
    assert all(all(expected[k] == results[k]) for k in expected.keys())


def test_set_out_sample_residuals_when_residuals_length_is_less_than_10000_and_append():
    """
    Test residuals stored when new residuals length is less than 10000 and append is True.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2,
        transformer_series=None
    )
    forecaster.fit(series=series)
    y_true = {
        1: pd.Series(np.array([1, 2, 3, 4, 5])), 
        2: pd.Series(np.array([2, 3, 4, 5, 6]))
    }
    y_pred = {
        1: pd.Series(np.array([0, 1, 2, 3, 4])), 
        2: pd.Series(np.array([0, 1, 2, 3, 4]))
    }
    
    forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)
    forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred, append=True)
    expected = {
        1: np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
        2: np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2])
    }
    results = forecaster.out_sample_residuals_

    assert expected.keys() == results.keys()
    assert all(all(expected[k] == results[k]) for k in expected.keys())


def test_set_out_sample_residuals_when_residuals_length_is_greater_than_10000():
    """
    Test len residuals stored when its length is greater than 10000.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2,
        transformer_series=None
    )
    forecaster.fit(series=series)
    y_true = {1: np.arange(20_000), 2: np.arange(20_000)}
    y_pred = {1: np.arange(20_000) + 1, 2: np.arange(20_000) + 2}
    forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)
    results = forecaster.out_sample_residuals_

    assert list(results.keys()) == [1, 2]
    assert all(len(value) == 10_000 for value in results.values())


def test_set_out_sample_residuals_when_residuals_length_is_more_than_10000_and_append():
    """
    Test residuals stored when new residuals length is more than 10000 and append is True.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2,
        transformer_series=None
    )
    forecaster.fit(series=series)
    y_true = {1: np.random.normal(size=5_000), 2: np.random.normal(size=5_000)}
    y_pred = {1: np.random.normal(size=5_000), 2: np.random.normal(size=5_000)}
    forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)
    y_true = {1: np.random.normal(size=10_000), 2: np.random.normal(size=10_000)}
    y_pred = {1: np.random.normal(size=10_000), 2: np.random.normal(size=10_000)}
    forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred, append=True)
    results = forecaster.out_sample_residuals_

    assert all([len(v) == 10_000 for v in results.values()])


def test_set_out_sample_residuals_when_residuals_keys_partially_match():
    """
    Test residuals are stored only for matching keys.
    """
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2,
        transformer_series=None
    )
    forecaster.fit(series=series)
    y_pred = {1: np.repeat(1, 5), 4: np.arange(10)}
    y_true = {1: np.arange(5), 4: np.arange(10)}
    forecaster.set_out_sample_residuals(y_true=y_true, y_pred=y_pred)
    results = forecaster.out_sample_residuals_
    expected = {1: np.array([-1,  0,  1,  2,  3]), 2: None}
    for key in expected.keys():
        if expected[key] is not None:
            assert np.allclose(expected[key], results[key])
        else:
            assert results[key] is None


def test_forecaster_set_outsample_residuals_when_transformer_y_and_diferentiation():
    """
    Test set_out_sample_residuals when forecaster has transformer_y and differentiation.
    Stored should equivalent to residuals calculated manually if transformer_y and
    differentiation are applied to `y_true` and `y_pred` before calculating residuals.
    """
    rng = np.random.default_rng(12345)
    series_train = pd.DataFrame({
        'l1': pd.Series(
            rng.normal(loc=0, scale=1, size=100),
            index = pd.date_range(start='1-1-2018', periods=100, freq='D')
        ),
        'l2': pd.Series(
            rng.normal(loc=0, scale=1, size=100),
            index = pd.date_range(start='1-1-2018', periods=100, freq='D')
        )
    })
    y_true  = {
        1: rng.normal(loc=0, scale=1, size=5),
        2: rng.normal(loc=0, scale=1, size=5)
    }
    y_pred = {
        1: rng.normal(loc=0, scale=1, size=5),
        2: rng.normal(loc=0, scale=1, size=5)
    }
    forecaster = ForecasterDirectMultiVariate(
        regressor=LinearRegression(),
        level='l1',
        lags=3,
        steps=2,
        differentiation=1,
        transformer_series=StandardScaler()
    )
    forecaster.fit(series=series_train)
    forecaster.set_out_sample_residuals(
        y_true = y_true,
        y_pred = y_pred
    )

    y_true[1] = forecaster.transformer_series_['l1'].transform(y_true[1].reshape(-1, 1)).flatten()
    y_true[2] = forecaster.transformer_series_['l1'].transform(y_true[2].reshape(-1, 1)).flatten()
    y_pred[1] = forecaster.transformer_series_['l1'].transform(y_pred[1].reshape(-1, 1)).flatten()
    y_pred[2] = forecaster.transformer_series_['l1'].transform(y_pred[2].reshape(-1, 1)).flatten()
    y_true[1] = forecaster.differentiator_['l1'].transform(y_true[1])[forecaster.differentiation:]
    y_true[2] = forecaster.differentiator_['l1'].transform(y_true[2])[forecaster.differentiation:]
    y_pred[1] = forecaster.differentiator_['l1'].transform(y_pred[1])[forecaster.differentiation:]
    y_pred[2] = forecaster.differentiator_['l1'].transform(y_pred[2])[forecaster.differentiation:]
    residuals = {}
    residuals[1] = y_true[1] - y_pred[1]
    residuals[2] = y_true[2] - y_pred[2]

    for key in residuals.keys():
        assert np.allclose(residuals[key], forecaster.out_sample_residuals_[key])
