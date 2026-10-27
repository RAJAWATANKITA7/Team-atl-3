-- Creates the property graph over the Central Market tables in a4i_econ.
-- Nodes: Business (231), Employer (122 census-block worker counts).
-- Edges: Supplies (supplier -> buyer, modeled from BEA intensities),
--        DrawsFootfall (employer block -> business, modeled allocation).
-- borrowed_from is NOT in the graph: it has no edge key and its far end is a
-- bank, not a node. Join it in plain SQL when loan history is needed.
-- Naming: dataset-qualified and unbackticked in NODE/EDGE TABLES; no dataset in
-- REFERENCES. Backticking a three-part name breaks the REFERENCES lookup.

CREATE OR REPLACE PROPERTY GRAPH a4i_econ.LocalEconomy
  NODE TABLES (
    a4i_econ.businesses
      KEY (business_id)
      LABEL Business PROPERTIES (business_id, name, address, zip, naics4, latitude, longitude),
    a4i_econ.employer_blocks
      KEY (block_id)
      LABEL Employer PROPERTIES (block_id, tract, jobs)
  )
  EDGE TABLES (
    a4i_econ.supplies
      KEY (edge_id)
      SOURCE KEY (supplier_id) REFERENCES businesses (business_id)
      DESTINATION KEY (buyer_id) REFERENCES businesses (business_id)
      LABEL Supplies PROPERTIES (intensity, metres),
    a4i_econ.draws_footfall_from
      KEY (edge_id)
      SOURCE KEY (block_id) REFERENCES employer_blocks (block_id)
      DESTINATION KEY (business_id) REFERENCES businesses (business_id)
      LABEL DrawsFootfall PROPERTIES (worker_share, metres)
  );
