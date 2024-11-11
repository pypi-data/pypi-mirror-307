# tests/test_compute_exposure.py
import pytest
from SecretSharer import ComputeExposure 

def test_compute_exposure_rank_method():
    # Set up test data for canary and reference perplexities
    canary_perplexities = {"canary1": 10.0, "canary2": 20.0, "canary3": 15.0}
    reference_perplexities = [5.0, 25.0, 30.0, 35.0]

    # Instantiate ComputeExposure and calculate exposures
    exposure_calculator = ComputeExposure(canary_perplexities, reference_perplexities)
    exposures = exposure_calculator.compute_exposure_rank_method()

    # Check if exposures are calculated correctly
    assert isinstance(exposures, dict), "Exposures should be returned as a dictionary."
    assert set(exposures.keys()) == set(canary_perplexities.keys()), "Exposure keys should match canary keys."
    for exposure in exposures.values():
        assert exposure >= 0, "Exposure scores should be non-negative."
