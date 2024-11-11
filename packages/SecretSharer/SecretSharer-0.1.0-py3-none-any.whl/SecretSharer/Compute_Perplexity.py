import torch


class PerplexityCalculator:
    """
    PerplexityCalculator computes perplexity scores for a given set of canary and reference sequences.

    Attributes:
        model: Pre-trained language model for predictions.
        tokenizer: Tokenizer for processing text inputs.
        max_length (int): Maximum token length for each input.
        device (str): Device for model inference (e.g., 'cuda' or 'cpu').
    """

    def __init__(
        self, model=None, tokenizer=None, max_length=1024, device=torch.device("cpu")
    ):
        """
        Initializes the PerplexityCalculator with model and tokenizer.

        Args:
            model: The pre-trained model used for predictions.
            tokenizer: The tokenizer corresponding to the model.
            max_length (int): Maximum token length for each input.
            device (str): The device (e.g., 'cuda' or 'cpu') for model inference.
        """
        self.model = model
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.device = device

    def compute_perplexity(self, text):
        """
        Computes perplexity for a single text sequence.

        Args:
            text (str): The input text for which perplexity is computed.

        Returns:
            float: The computed perplexity score.
        """
        input_ids = self.tokenizer.encode(
            text, return_tensors="pt", max_length=self.max_length, padding="max_length"
        ).to(self.device)

        # Check vocabulary 
        max_vocab_id = self.model.config.vocab_size - 1
        
        if input_ids.max() > max_vocab_id:
            raise ValueError("Input IDs exceed the model's vocabulary size.")

        # Forward pass to calculate loss
        with torch.no_grad():
            outputs = self.model(input_ids, labels=input_ids)
            loss = outputs.loss.item()

        # Convert loss to perplexity
        perplexity = torch.exp(torch.tensor(loss)).item()
        return perplexity

    def compute_perplexities_for_canaries(self, canaries, references):
        """
        Computes perplexity scores for lists of canary and reference sequences.

        Args:
            canaries (list of str): List of unique canary text inputs.
            references (list of str): List of reference text inputs.

        Returns:
            tuple: A tuple containing two lists:
                - canary_perplexities: Perplexities for each canary sequence.
                - reference_perplexities: Perplexities for each reference sequence.
        """
        # Calculate perplexity for each canary
        canary_perplexities = {
            canary: self.compute_perplexity(canary) for canary in canaries
        }

        # Calculate perplexity for each reference
        reference_perplexities = [
            self.compute_perplexity(reference) for reference in references
        ]

        return canary_perplexities, reference_perplexities
