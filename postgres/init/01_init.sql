-- 1. Enable the vector extension (Essential for NLP)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Create a table for 384-dim MiniLM NLP embeddings
CREATE TABLE IF NOT EXISTS embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,         -- The actual text/sentence
    vector_data VECTOR(384),      -- MUST BE 384 for MiniLM-Multilingual-L12
    metadata JSONB,               -- Extra info (author, date, etc.)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Add an index to make searches fast (IVFFlat or HNSW)
CREATE INDEX ON embeddings USING hnsw (vector_data vector_cosine_ops);