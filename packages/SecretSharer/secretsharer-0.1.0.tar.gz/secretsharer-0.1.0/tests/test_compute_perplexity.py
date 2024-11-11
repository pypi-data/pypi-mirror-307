# tests/test_compute_perplexity.py
import pytest
from transformers import AutoModelForCausalLM, AutoTokenizer
from SecretSharer import PerplexityCalculator 

@pytest.fixture
def mock_perplexity_calculator():
    tokenizer = AutoTokenizer.from_pretrained("distilbert/distilgpt2", use_fast = False)
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    
    model = AutoModelForCausalLM.from_pretrained("distilbert/distilgpt2", trust_remote_code = True)
    return model, tokenizer

def test_compute_perplexity(mock_perplexity_calculator):
    text = "This is a test sentence."
    model, tokenizer = mock_perplexity_calculator
    tokenizer.add_tokens([text])
    model.resize_token_embeddings(len(tokenizer)) 
    perplexity = PerplexityCalculator(model, tokenizer).compute_perplexity(text)
    assert isinstance(perplexity, float), "Perplexity should be a float."
    assert perplexity > 0, "Perplexity should be positive."

def test_compute_perplexities_for_canaries(mock_perplexity_calculator):
    canaries = ["This is a test canary.", "Another test canary."]
    references = ["This is a reference sentence.", "Another reference."]
    model, tokenizer = mock_perplexity_calculator
    tokenizer.add_tokens(canaries)
    model.resize_token_embeddings(len(tokenizer))
    canary_perplexities, reference_perplexities = PerplexityCalculator(model, tokenizer).compute_perplexities_for_canaries(canaries, references)
    
    assert isinstance(canary_perplexities, dict), "Canary perplexities should be a dictionary."
    assert isinstance(reference_perplexities, list), "Reference perplexities should be a list."
    assert len(canary_perplexities) == len(canaries), "Each canary should have a perplexity score."
    assert len(reference_perplexities) == len(references), "Each reference should have a perplexity score."
