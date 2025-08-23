CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- projects & sessions
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  style_guide_md TEXT DEFAULT '',
  target_metrics_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id),
  status TEXT NOT NULL DEFAULT 'open', -- open|frozen|archived
  created_at TIMESTAMPTZ DEFAULT now()
);

-- agents & config
CREATE TABLE agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id),
  role TEXT NOT NULL,                  -- showrunner|worldbuilder|...
  model_id TEXT NOT NULL,              -- e.g., anthropic/claude-3.5-sonnet
  fallbacks TEXT[] NOT NULL DEFAULT '{}',
  provider_prefs JSONB NOT NULL DEFAULT '{}'::jsonb,
  params_json JSONB NOT NULL DEFAULT '{}'::jsonb,  -- temp, top_p, max_tokens...
  tools TEXT[] NOT NULL DEFAULT '{}',              -- bound MCP tool ids
  allowlist TEXT[] NOT NULL DEFAULT '{}'           -- allowed models for this role
);

-- artifacts
CREATE TABLE artifacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES sessions(id),
  type TEXT NOT NULL,                   -- brief|lore_card|char_sheet|outline|scene_draft|edit_notes|compiled_chapter|style_guide
  path TEXT NOT NULL,                   -- object-store key
  version INTEGER NOT NULL DEFAULT 1,
  meta_json JSONB NOT NULL DEFAULT '{}'::jsonb, -- provenance: {agent, model, tokens, cost}
  canon BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- messages (A2A chatter, references artifacts)
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES sessions(id),
  from_role TEXT NOT NULL,
  to_role TEXT,
  content JSONB NOT NULL,               -- structured; see TaskEnvelope/Report below
  refs UUID[] NOT NULL DEFAULT '{}',    -- artifact ids
  headers JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- reviews / gates
CREATE TABLE reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  artifact_id UUID NOT NULL REFERENCES artifacts(id),
  reviewer_role TEXT NOT NULL,          -- dev_editor|continuity|metrics|showrunner
  verdict TEXT NOT NULL,                -- pass|fail|revise
  notes TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);
