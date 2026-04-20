-- Migration: Create leads table
-- Task: ENV-4

CREATE TABLE leads (
  id               UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at       TIMESTAMPTZ DEFAULT now()             NOT NULL,
  updated_at       TIMESTAMPTZ DEFAULT now()             NOT NULL,

  -- Contact info
  name             TEXT        NOT NULL,
  company          TEXT        NOT NULL,
  email            TEXT        NOT NULL,
  destination_port TEXT,
  product          TEXT        NOT NULL,
  message          TEXT,

  -- Sales pipeline
  status           TEXT        DEFAULT 'new'             NOT NULL
    CHECK (status IN ('new', 'contacted', 'qualified', 'closed')),
  notes            TEXT,

  -- Lead origin (web form, chatbot, manual entry)
  source           TEXT        DEFAULT 'form'            NOT NULL
    CHECK (source IN ('form', 'chatbot', 'manual'))
);

-- Keep updated_at in sync on every UPDATE
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER leads_set_updated_at
  BEFORE UPDATE ON leads
  FOR EACH ROW
  EXECUTE FUNCTION set_updated_at();
