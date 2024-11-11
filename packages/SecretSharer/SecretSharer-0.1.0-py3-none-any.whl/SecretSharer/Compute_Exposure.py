import numpy as np


class ComputeExposure:
    """
    ComputeExposure calculates exposure scores for a set of canaries based on their perplexities
    relative to reference perplexities.

    Attributes:
        perplexities (dict): Dictionary mapping canary keys to their perplexity values.
        reference_perplexities (list): List of perplexity values for reference sequences.
    """

    def __init__(self, perplexities=None, reference_perplexities=None):
        """
        Initializes the ComputeExposure with canary and reference perplexities.

        Args:
            perplexities (dict, optional): Canary perplexities, with keys as canary identifiers.
            reference_perplexities (list, optional): List of perplexity values for reference sequences.
        """
        self.perplexities = perplexities if perplexities is not None else {}
        self.reference_perplexities = (
            reference_perplexities if reference_perplexities is not None else []
        )

    def compute_exposure_rank_method(self):
        """
        Computes exposure scores for each canary sequence based on perplexities.

        Returns:
            dict: Exposure scores for each canary, mapped by their unique identifiers.
        """
        if not self.perplexities or not self.reference_perplexities:
            raise ValueError(
                "Perplexities and reference_perplexities must not be empty."
            )

        # Initialize list with baseline perplexities
        perplexities_concat = [(p, -1) for p in self.reference_perplexities]

        # Append perplexities of each canary, associating each with its unique index
        for i, (k, p) in enumerate(self.perplexities.items()):
            perplexities_concat.append((p, i))

        # Sort by perplexity (first element of each tuple)
        indices_concat = np.fromiter(
            (i for _, i in sorted(perplexities_concat)), dtype=int
        )
        cum_sum = np.cumsum(indices_concat == -1)

        # Define ranks based on cumulative sum and store exposures
        keys = list(self.perplexities.keys())
        ranks = {keys[i]: cum_sum[indices_concat == i][0] + 1 for i in range(len(keys))}
        exposures = {
            k: np.log2(len(perplexities_concat)) - np.log2(ranks[k]) for k in ranks
        }

        return exposures
