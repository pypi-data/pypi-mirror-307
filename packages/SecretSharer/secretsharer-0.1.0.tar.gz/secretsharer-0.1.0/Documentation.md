---
# Compute Exposure

## 1. `ComputeExposure`
This class calculates exposure scores for a set of canaries based on their perplexities relative to reference perplexities.

### Arguments
- **`perplexities`** *(dict, optional)*: Dictionary where keys are canary identifiers and values are their perplexity values. Default is an empty dictionary `{}`.
- **`reference_perplexities`** *(list, optional)*: List of perplexity values for reference sequences. Default is an empty list `[]`.

### Methods
- **`compute_exposure_rank_method()`**: Computes exposure scores based on the perplexity ranks.
  - **Returns**: `dict` where keys are canary identifiers, and values are the exposure scores (as `float`).

---

# Compute Perplexity

## 2. `PerplexityCalculator`
This class computes perplexity scores for a set of sequences (canaries and references) using a language model.

### Arguments
- **`model`**: A pre-trained language model (e.g., `transformers` model). Default is `None`.
- **`tokenizer`**: A tokenizer compatible with the pre-trained model, used to tokenize input texts. Default is `None`.
- **`max_length`** *(int, optional)*: Maximum token length for each input sequence. Default is `1024`.
- **`device`** *(str or `torch.device`, optional)*: Device for model inference, either `'cpu'` or `'cuda'`. Default is `torch.device("cpu")`.

### Methods
- **`compute_perplexity(text)`**: Computes perplexity for a single text sequence.
  - **Arguments**:
    - **`text`** *(str)*: The text sequence for which to compute perplexity.
  - **Returns**: `float`, representing the computed perplexity score.

- **`compute_perplexities_for_canaries(canaries, references)`**: Computes perplexity scores for a list of canary and reference sequences.
  - **Arguments**:
    - **`canaries`** *(list of str)*: List of unique canary text sequences.
    - **`references`** *(list of str)*: List of reference text sequences.
  - **Returns**: `tuple` containing:
    - **`canary_perplexities`** *(list of float)*: Perplexity scores for each canary sequence.
    - **`reference_perplexities`** *(list of float)*: Perplexity scores for each reference sequence.

---
# Generate Canaries

## 3. `CanaryDatasetGenerator`
This class generates a dataset of unique canary sequences and reference sequences with specified patterns and repetitions.

### Arguments
- **`vocabulary`** *(list of str)*: List of tokens that can be used to generate sequences.
- **`pattern`** *(str)*: Pattern string with placeholders `{}` for formatting each canary sequence.
- **`repetitions`** *(list of int)*: List specifying the number of times each canary set should be repeated.
- **`secrets_per_repetition`** *(list of int)*: List specifying the number of unique canary sequences in each repetition group.
- **`num_references`** *(int)*: Number of reference sequences to be generated.
- **`seed`** *(int, optional)*: Seed value for random number generation for reproducibility. Default is `0`.

### Methods
- **`create_dataset()`**: Generates a dataset of canary sequences with repetitions and reference sequences.
  - **Returns**: `dict` containing:
    - **`dataset`** *(list of str)*: List of canary sequences, with specified repetitions.
    - **`references`** *(list of str)*: List of unique reference sequences.
