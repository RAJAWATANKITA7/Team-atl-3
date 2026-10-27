# Data lane: design decisions and limitations

Corridor: Central Market. Track: micro-producer & supply continuity.
Draft, written before the graph queries were run. Update with results.

## What we loaded (measured from our own run)
- 231 businesses, 65 distinct 4-digit industries, after privacy filters
  (1,389 raw registry rows; 390 had no usable industry code).
- 989 supply edges, 1,024 footfall edges, 122 employer blocks, 7 tracts,
  4 matched SBA loans (3 businesses, none charged off).
- Validation: 25 of 25 checks passed, including unique graph element keys.

## Decisions
1. **Depth: two hops.** Three hops saturates the corridor and stops being informative.
2. **Weighting: path intensity, not buyer count.** Buyer count and intensity rank
   suppliers differently (for example Tradespace has the most buyers but weak links).
3. **Count distinct businesses, never paths.** Paths overstate reach.
4. **Sole-source caveat.** Several top suppliers are the only business in their industry
   in the corridor, so they collect every edge for that input. Their buyers could often
   source outside the corridor. Show reach with that caveat.
5. **Hub rule.** Do not fund a supplier just because it is the biggest hub. Decline
   suppliers whose reach is implausibly large (Tradespace reaches about 84% of the
   corridor), that are not micro-producers, or whose reach comes from being the only
   local source in their industry.
6. **Duplicate registrations: not merged.** Merging risks inventing dependencies.
   Check any supplier before recommending it.
7. **Footfall edges are in the graph but secondary** for this track.

## Real vs modeled
- Real: businesses, SBA loans, LEHD job counts, ACS tract demographics, BEA
  industry-level purchase intensities.
- Modeled (ours): which specific business buys from which, and how worker counts are
  allocated to nearby shops.

## Limitations to state in the deck
- Supply edges are modeled; industry-group coefficients mean some businesses have
  identical reach (for example Sour Flour and Cumaica Coffee).
- Edge generator keeps only the top 5 suppliers per buyer and drops 21 ubiquitous
  supplier industries; both choices shape every cascade.
- Footfall blocks are placed at tract centers, so location is approximate.
- Only 3 businesses matched an SBA loan and none were charged off, so we cannot
  check our fragility signal against real failures in this corridor.
- Tract join kept 7 of 14 requested tracts; ACS vintage is 2016-2020.
- No per-business job counts exist; the cascade counts businesses, not jobs.

## Open questions
- Reconcile two-hop counts: notebook said 80 of 231, validation said 85.
  Use distinct businesses and state the definition.
