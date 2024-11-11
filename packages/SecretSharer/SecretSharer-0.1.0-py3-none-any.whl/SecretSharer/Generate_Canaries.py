import numpy as np
import string


class CanaryDatasetGenerator:
    """
    EfficientCanaryDatasetGenerator generates a dataset of canary sequences with specified repetitions and patterns.

    Attributes:
        vocabulary (list): List of possible tokens for sequence generation.
        pattern (str): Pattern to format each canary sequence.
        repetitions (list): Number of repetitions for each canary set.
        secrets_per_repetition (list): Number of canaries for each repetition group.
        num_references (int): Number of reference sequences to include.
        seed (int): Seed for random number generation to ensure reproducibility.
    """

    def __init__(
        self,
        vocabulary,
        pattern,
        repetitions,
        secrets_per_repetition,
        num_references,
        seed=0,
    ):
        """
        Initializes the generator with configuration parameters.

        Args:
            vocabulary (list): List of possible tokens for sequence generation.
            pattern (str): The pattern for formatting sequences.
            repetitions (list): Repetitions per canary set.
            secrets_per_repetition (list): Number of canaries per repetition group.
            num_references (int): Number of random reference sequences.
            seed (int): Seed for reproducibility.
        """
        self.vocabulary = vocabulary
        self.pattern = pattern
        self.repetitions = repetitions
        self.secrets_per_repetition = secrets_per_repetition
        self.num_references = num_references
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def _count_placeholders(self):
        """Counts the placeholders in the pattern for replacement."""
        return sum(
            1 for _ in string.Formatter().parse(self.pattern) if _[1] is not None
        )

    def _generate_unique_sequences(self, count):
        """Generates a unique set of sequences following the pattern and vocabulary size."""
        length = self._count_placeholders()
        if len(self.vocabulary) ** length < count:
            raise ValueError(
                "Vocabulary size is too small to generate the required unique sequences."
            )

        # Generate unique sequences directly
        sequences = set()
        while len(sequences) < count:
            indices = self.rng.choice(self.vocabulary, (count - len(sequences), length))
            new_sequences = [self.pattern.format(*sequence) for sequence in indices]
            sequences.update(new_sequences)

        return list(sequences)

    def _build_dataset(self, sequences):
        """Constructs the dataset and reference set with specified repetitions."""
        dataset = []
        ref_start_index = sum(self.secrets_per_repetition)
        canary_sequences = sequences[:ref_start_index]
        reference_sequences = sequences[
            ref_start_index : ref_start_index + self.num_references
        ]

        for repeat_count, secret_count in zip(
            self.repetitions, self.secrets_per_repetition
        ):
            dataset.extend(canary_sequences[:secret_count] * repeat_count)
            canary_sequences = canary_sequences[secret_count:]

        return dataset, reference_sequences

    def create_dataset(self):
        """
        Generates the canary dataset with repeated sequences and references.

        Returns:
            dict: Contains 'dataset' with canary sequences and 'references' with extra sequences.
        """
        total_secrets = sum(self.secrets_per_repetition)
        total_required_sequences = total_secrets + self.num_references

        sequences = self._generate_unique_sequences(total_required_sequences)
        dataset, references = self._build_dataset(sequences)

        return {"dataset": dataset, "references": references}
