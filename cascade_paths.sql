-- One supplier's cascade as paths, ready for the graph visualization.
-- Replace SUPPLIER NAME HERE with a name from the band query.
-- TO_JSON(p) is required, or the viewer shows a table instead of a graph.
-- ANY SHORTEST returns one path per source-destination pair so the picture
-- stays legible. The notebook visualization caps at 2 MB, so keep one seed.
-- For the agent's tool, parameterize the seed on business_id instead of name.

GRAPH a4i_econ.LocalEconomy
MATCH p = ANY SHORTEST (seed:Business WHERE seed.name = 'SUPPLIER NAME HERE')
          -[:Supplies]->{1,2}(exposed:Business)
RETURN TO_JSON(p) AS paths
