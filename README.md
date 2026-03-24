# Immunefi Smart Contract Mega Repo (Program Organized)

This snapshot is organized by Immunefi program slug at repo root.

Generated on: 2026-03-24 (America/New_York)

## Filters Applied

- Included asset type: `smart_contract`
- Excluded: audit competitions
- Excluded: shutdown programs (`endDate` before 2026-03-24 UTC)
- Excluded program: `instadapp`
- Included only programs with `maxBounty >= 50000`

## Snapshot Totals

- Programs: 173
- Smart-contract asset references: 5968
- Linked via manifest-resolved outputs: 3894
- Linked GitHub blob snapshots: 906
- Linked GitHub repo assets: 183
- Linked GitHub gists: 5
- Unresolved in filtered export: 980
  - On-chain unresolved: 705
  - GitHub blob unresolved: 30
  - Other unresolved (unsupported/unmatched): 245

## Resolution Notes

- Added non-EVM recovery for Tronscan and Solana (Alchemy RPC)
- Added EVM bytecode recovery via Etherscan v2 `proxy.eth_getCode`
- Placeholder rows/files were removed; unresolved assets are now explicit as `unresolved.json`

## Layout

- `<program-slug>/assets.json`: source asset refs for the program
- `<program-slug>/summary.json`: linked counts per program
- `<program-slug>/resolved-by-manifest/`: symlinks keyed by `asset_id` when resolved
- `<program-slug>/unresolved.json`: unresolved asset refs for that program
- `mega-repo/assets/`: shared resolved asset store (target of symlinks)
- `mega-repo/manifests/`: source manifests from the builder run
- `.meta/summary.json`: global totals and filter metadata
- `.meta/summary_by_program.json`: per-program compact summary
