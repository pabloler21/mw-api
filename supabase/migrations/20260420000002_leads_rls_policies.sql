-- Migration: RLS policies for leads table
-- Task: ENV-4

ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

-- Anonymous visitors can insert a lead from the public form.
-- WITH CHECK (true) is intentional: data validation happens in FastAPI (Pydantic).
CREATE POLICY "leads_anon_insert"
  ON leads
  FOR INSERT
  TO anon
  WITH CHECK (true);

-- Only authenticated users (admins) can read leads.
CREATE POLICY "leads_auth_select"
  ON leads
  FOR SELECT
  TO authenticated
  USING (true);

-- Only authenticated users can update status and notes.
-- Prevents the client from modifying the sales pipeline directly.
CREATE POLICY "leads_auth_update"
  ON leads
  FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

-- Deletion is explicitly restricted to service_role.
-- An authenticated JWT user cannot accidentally delete leads from the client.
-- Deletes must go through the backend (service key) or the Supabase dashboard.
CREATE POLICY "leads_deny_delete"
  ON leads
  FOR DELETE
  TO authenticated
  USING (false);
