from typing import List
from tokenizers import Tokenizer

from .base import Chunk, BaseChunker
class TokenChunker(BaseChunker):
    def __init__(self, tokenizer: Tokenizer, chunk_size: int = 512, chunk_overlap: int = 128):
        """Initialize the TokenChunker with configuration parameters.

        Args:
            tokenizer: The tokenizer instance to use for encoding/decoding
            chunk_size: Maximum number of tokens per chunk
            chunk_overlap: Number of tokens to overlap between chunks

        Raises:
            ValueError: If chunk_size <= 0 or chunk_overlap >= chunk_size
        """
        super().__init__(tokenizer)
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str) -> List[Chunk]:
        """Split text into overlapping chunks of specified token size.

        Args:
            text: Input text to be chunked

        Returns:
            List of Chunk objects containing the chunked text and metadata
        """
        if not text.strip():
            return []

        # Encode full text
        encoding = self._encode(text)
        text_tokens = encoding
        chunks = []

        # Calculate chunk positions
        start_indices = range(0, len(text_tokens), self.chunk_size - self.chunk_overlap)

        for start_idx in start_indices:
            # Get token indices for this chunk
            end_idx = min(start_idx + self.chunk_size, len(text_tokens))

            # Extract and decode tokens for this chunk
            chunk_tokens = text_tokens[start_idx:end_idx]
            chunk_text = self.tokenizer.decode(chunk_tokens)

            chunks.append(Chunk(
                text=chunk_text,
                start_index=start_idx,
                end_index=end_idx,
                token_count=len(chunk_tokens)
            ))

            # Break if we've reached the end of the text
            if end_idx == len(text_tokens):
                break

        return chunks

    def __repr__(self) -> str:
        return (f"TokenChunker(chunk_size={self.chunk_size}, "
                f"chunk_overlap={self.chunk_overlap})")