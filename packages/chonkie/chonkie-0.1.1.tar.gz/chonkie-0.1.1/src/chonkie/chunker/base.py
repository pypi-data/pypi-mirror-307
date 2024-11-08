from typing import List
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Chunk:
    """Dataclass representing a text chunk with metadata."""
    text: str
    start_index: int
    end_index: int
    token_count: int

class BaseChunker(ABC):
    """Abstract base class for all chunker implementations.
    
    All chunker implementations should inherit from this class and implement
    the chunk() method according to their specific chunking strategy.
    """
    def __init__(self, tokenizer):
        """Initialize the chunker with a tokenizer.
        
        Args:
            tokenizer: Tokenizer object to be used for tokenizing text
        """
        self.tokenizer = tokenizer
        self._tokenizer_backend = self._get_tokenizer_backend()

    def _get_tokenizer_backend(self):
        """Return the backend tokenizer object."""
        if "transformers" in str(type(self.tokenizer)):
            return "transformers"
        elif "tokenizers" in str(type(self.tokenizer)):
            return "tokenizers"
        elif "tiktoken" in str(type(self.tokenizer)):
            return "tiktoken"
        else:
            raise ValueError("Tokenizer backend not supported")
    
    def _encode(self, text: str):
        """Encode text using the backend tokenizer."""
        if self._tokenizer_backend == "transformers":
            return self.tokenizer.encode(text)
        elif self._tokenizer_backend == "tokenizers":
            return self.tokenizer.encode(text).ids
        elif self._tokenizer_backend == "tiktoken":
            return self.tokenizer.encode(text)
        else:
            raise ValueError("Tokenizer backend not supported.")
    
    def _encode_batch(self, texts: List[str]):
        """Encode a batch of texts using the backend tokenizer."""
        if self._tokenizer_backend == "transformers":
            return self.tokenizer.batch_encode_plus(texts)['input_ids']
        elif self._tokenizer_backend == "tokenizers":
            return self.tokenizer.encode_batch(texts)
        elif self._tokenizer_backend == "tiktoken":
            return self.tokenizer.encode_batch(texts)
        else:
            raise ValueError("Tokenizer backend not supported.")

    @abstractmethod
    def chunk(self, text: str) -> List[Chunk]:
        """Split text into chunks according to the implementation strategy.
        
        Args:
            text: Input text to be chunked
            
        Returns:
            List of Chunk objects containing the chunked text and metadata
        """
        pass

    def __call__(self, text: str) -> List[Chunk]:
        """Make the chunker callable directly.
        
        Args:
            text: Input text to be chunked
            
        Returns:
            List of Chunk objects containing the chunked text and metadata
        """
        return self.chunk(text)
    
    def __repr__(self) -> str:
        """Return string representation of the chunker."""
        return f"{self.__class__.__name__}()"