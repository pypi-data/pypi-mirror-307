# tests/test_generate_canaries.py
import pytest
from SecretSharer import CanaryDatasetGenerator 

def test_count_placeholders():
    generator = CanaryDatasetGenerator(
        vocabulary=["a", "b", "c"],
        pattern="secret-{0}-{1}",
        repetitions=[2],
        secrets_per_repetition=[3],
        num_references=5,
    )
    placeholder_count = generator._count_placeholders()
    assert placeholder_count == 2, "The pattern should contain 2 placeholders."

def test_generate_unique_sequences():
    generator = CanaryDatasetGenerator(
        vocabulary=["a", "b", "c", "d"],
        pattern="secret-{0}-{1}",
        repetitions=[2],
        secrets_per_repetition=[3],
        num_references=5,
    )
    sequences = generator._generate_unique_sequences(6)
    assert len(sequences) == 6, "Should generate 6 unique sequences."
    assert len(set(sequences)) == 6, "All generated sequences should be unique."

def test_create_dataset():
    generator = CanaryDatasetGenerator(
        vocabulary=["a", "b", "c", "d"],
        pattern="secret-{0}-{1}",
        repetitions=[2, 1],
        secrets_per_repetition=[3, 2],
        num_references=5,
    )
    dataset_info = generator.create_dataset()

    total_canaries = sum(generator.repetitions[i] * generator.secrets_per_repetition[i] for i in range(len(generator.repetitions)))
    assert len(dataset_info["dataset"]) == total_canaries, "The dataset size should match the specified repetitions and secrets per repetition."
    assert len(dataset_info["references"]) == generator.num_references, "Reference set size should match num_references."
