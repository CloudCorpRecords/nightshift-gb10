# THE FLEET — Rene's MCP tools, shared with the whole team

*Per RENE (12:15 PT): the fleet is not Tree-only. Every agent on this team
(BINO, RENE-CLAUDE, RUSS-AI, MIKE-AI) is invited — expected — to use these
tools in their own work today, and to **log usage in `comms/LOG.md` with a
`[fleet: <tool>]` tag** so the team record shows exactly whose products did
what. That attribution feeds the submission and the README.*

All tools are Rene's open-source fleet (GitHub: CloudCorpRecords). Index of
everything: **ProdForge** — https://github.com/CloudCorpRecords/prodforge —
the fleet factory: one catalog + merged MCP config for 100+ servers, with
`list / connect / doctor / checklist / ship` in a single CLI+MCP bin. Start
there if your agent runtime takes an MCP config.

## The tools

| Tool | What it does | Where it fits today |
|---|---|---|
| **Greenlight** | Pre-flight checker for GitHub contribution targets: scans a repo/issue and reports claims, gates, and go/no-go before you invest in a PR | Any agent about to open or review a PR against an unfamiliar repo — run it before you build |
| **wallcheck** | Probes sites/pages and classifies bot-walls and exposed key-like material in served pages (OPEN / CHALLENGED / WALLED + exposure classes) | Checking any web resource the team depends on; pre-submission link checks |
| **mcpaudit** | Audits an MCP server for malicious or risky behavior | **Required by team rule**: any MCP server you connect gets audited first (pairs with mcpvet) |
| **mcpvet** | Vets MCP servers/packages before install — the gate in front of mcpaudit's verdicts | Same as above: vet, then connect |
| **claimcheck** | Verifies claims in text against sources (claim → evidence check) | Fact-checking submission copy, README claims, pitch lines before they ship |
| **prwatch** | Watches pull requests and reports state changes | Watching this repo's PR queue during the merge storm |
| **gatefile** | Policy/gate checks on files before they pass a checkpoint | Pre-push hygiene on sensitive files (nothing secret ever enters this repo) |

## Rules of the road

1. **Vet before you connect** — mcpaudit + mcpvet on any MCP server, no
   exceptions (this is Rene's standing MCP vetting rule, applied fleet-wide).
2. **Log usage** — one LOG line per real use, tagged `[fleet: <tool>]`,
   saying what it decided or changed. No log, it didn't happen.
3. **Attribution is public** — this repo is open source; the fleet's role in
   building NightShift is part of the story we tell judges, accurately.
4. Fleet tools are advisory. The approval gate for NightShift's own actions
   stays human, exactly as the product promises.

## Who used what (the ledger — append yours)

- TREE — GitHub connector + Drive/Slides connectors for coordination,
  pushes, and the deck (platform connectors, not fleet). First fleet uses
  land here as they happen.
