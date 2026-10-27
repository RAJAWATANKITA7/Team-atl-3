-- Tool queries for the agent lane. Graph: a4i_econ.LocalEconomy (no backticks).
-- Parameters: @supplier_id (business_id string), @min_intensity (FLOAT64, default 0.05),
-- @naics4 (string). Query parameters inside GRAPH patterns are untested: if one
-- fails to parse, interpolate a validated literal instead of free text.
-- Tested by hand with literals: Cumaica Coffee = 60 strong buyers, total 5.4334.
--
-- Known ids: Cumaica Coffee 1051477-01-161, Sour Flour 1088753-08-161,
--            Tradespace 1282809-07-211 (113 links, strongest 0.0209, so none >= 0.05).
-- Caveats the agent must carry: supply strengths are INDUSTRY AVERAGES (every buyer
-- in the same industry gets the same weight), some buyers are duplicate registrations,
-- and a supplier that is the only business in its industry collects every edge for
-- that input (buyers could often source outside the corridor).

-- TOOL 1: strong buyers of one supplier, strongest first (the traversal, shown as rows).
GRAPH a4i_econ.LocalEconomy
MATCH (s:Business WHERE s.business_id = @supplier_id)
      -[e:Supplies WHERE e.intensity >= @min_intensity]->(b:Business)
WHERE s.business_id <> b.business_id
RETURN b.business_id AS buyer_id, b.name AS buyer, b.naics4 AS industry,
       b.address AS address, e.intensity AS intensity, e.metres AS metres
ORDER BY intensity DESC;

-- TOOL 2: summary for the memo (strong buyers and total strength).
GRAPH a4i_econ.LocalEconomy
MATCH (s:Business WHERE s.business_id = @supplier_id)
      -[e:Supplies WHERE e.intensity >= @min_intensity]->(b:Business)
WHERE s.business_id <> b.business_id
RETURN s.name AS supplier,
       COUNT(DISTINCT b.business_id) AS strong_buyers,
       SUM(e.intensity) AS total_intensity;

-- TOOL 3: sole-source check (1 means the only local business in its industry).
SELECT COUNT(*) AS businesses_in_same_industry
FROM a4i_econ.businesses
WHERE naics4 = @naics4;

-- TOOL 4: hub check (all links, to show weak-link hubs like Tradespace).
GRAPH a4i_econ.LocalEconomy
MATCH (s:Business WHERE s.business_id = @supplier_id)-[e:Supplies]->(b:Business)
RETURN COUNT(*) AS links, MAX(e.intensity) AS strongest_link;
