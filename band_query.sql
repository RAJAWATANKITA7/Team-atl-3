-- Suppliers that protect a meaningful number of other businesses within two
-- hops, without being the giant hubs. Depth is 2 on purpose: at 3 hops a
-- well-connected supplier reaches ~200 of 230 businesses and the cascade
-- stops being informative.
-- Counts DISTINCT businesses, not paths (paths overstate reach).
-- Band of 5 to 25 is the notebook's suggested starting point, not a rule.
-- Caveat: a supplier that is the ONLY business in its industry here collects
-- every edge for that input (check: SELECT naics4, COUNT(*) FROM
-- a4i_econ.businesses GROUP BY naics4). Its buyers could often source outside
-- the corridor, so treat its reach as an upper bound.

GRAPH a4i_econ.LocalEconomy
MATCH (seed:Business)-[:Supplies]->{1,2}(exposed:Business)
RETURN seed.name AS business, seed.naics4 AS industry,
       COUNT(DISTINCT exposed.business_id) AS exposed_2hop
NEXT
FILTER exposed_2hop >= 5 AND exposed_2hop <= 25
RETURN business, industry, exposed_2hop
ORDER BY exposed_2hop DESC
