-- Migration: Performance indexes for leads table
-- Task: ENV-4

-- Chronological listing (default sort order in any admin view).
CREATE INDEX idx_leads_created_at ON leads (created_at DESC);

-- Filter by sales pipeline stage (most-queried column in the CRM).
CREATE INDEX idx_leads_status ON leads (status);

-- Duplicate lead detection by email before insert.
CREATE INDEX idx_leads_email ON leads (email);
