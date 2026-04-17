# ADR 004: Multi-Dashboard Strategy (Marimo + Evidence)

## Status

Accepted

## Context

We needed a visualization strategy that serves both technical and business stakeholders. The project requirements included:

- Interactive data exploration for data scientists
- Business-friendly dashboards for stakeholders
- A portfolio piece demonstrating visualization skills
- Static site output (hostable on GitHub Pages)

## Decision

Implement **dual dashboards** with distinct purposes:

| Dashboard | Technology | Primary Audience | Purpose |
|-----------|-------------|------------------|---------|
| **Marimo** | Python notebooks | Data Scientists, Engineers | Interactive exploration, custom logic |
| **Evidence** | Markdown + SQL | Business Analysts, Executives | Static BI, self-service analytics |

## Rationale

### Marimo for Technical Users

| Factor | Assessment |
|--------|------------|
| **Customization** | High (Python code) |
| **Interactivity** | Reactive execution, sliders, inputs |
| **Learning Curve** | Python required |
| **Best For** | Data exploration, custom visualizations, algorithm testing |

**Why Marimo over Streamlit?**
- Reactive execution (automatic re-computation on change)
- No callback boilerplate
- Notebook-style execution model
- First-class Plotly support

### Evidence for Business Users

| Factor | Assessment |
|--------|------------|
| **Output** | Static HTML (hostable on GitHub Pages) |
| **Configuration** | Markdown + SQL |
| **Learning Curve** | SQL required, Markdown simple |
| **Best For** | Self-service analytics, executive dashboards, portfolio pieces |

**Why Evidence?**
- Markdown-first: dashboards are `.md` files, version-controllable
- Static output: no running server needed in production
- Native DuckDB connector
- Portfolio diversity (shows Markdown + SQL skills)
- GitHub Pages deployment

## Architecture

```
┌─────────────────────────────────────────────┐
│         DuckDB (Local, gaming_analytics)     │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
┌──────────────┐     ┌──────────────┐
│    Marimo     │     │   Evidence   │
│   :2718      │     │    :3000     │
│   Python     │     │  Markdown    │
│  (Live UI)   │     │  (Static)    │
└──────────────┘     └──────────────┘
```

## Consequences

### Positive
- **Serves both audiences**: Technical exploration + business reporting
- **Portfolio diversity**: Shows ability to work with multiple visualization paradigms
- **Static output from Evidence**: Hostable on GitHub Pages, no backend needed
- **Shared data model**: Single source of truth (marts layer)

### Negative
- **Maintenance overhead**: Two codebases to maintain
- **Consistency challenges**: Different UX patterns
- **Node 22 required**: Evidence needs compatible Node version

### Mitigation
- Shared `marts` layer ensures data consistency
- Node version managed via `fnm` (documented in justfile)
- Unified color scheme and metrics

## Alternatives Considered

| Alternative | Why Not Chosen |
|-------------|----------------|
| **Streamlit only** | Less reactive, callback-based model |
| **Rill only** | Requires running server process, no static output |
| **Plotly Dash** | More boilerplate than Marimo |
| **Metabase only** | Less interactive for data scientists |
| **Single dashboard** | Can't serve both audiences well |

## References

- [Marimo Documentation](https://marimo.io/)
- [Evidence Documentation](https://docs.evidence.dev/)
- [Why Marimo over Streamlit](https://marimo.io/blog/marimo-vs-streamlit)
