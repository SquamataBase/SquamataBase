CREATE TABLE sb_taxon_reptile AS
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Reptilia'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
    )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_reptile_scientific_name_like ON sb_taxon_reptile(scientific_name);

CREATE TABLE sb_taxon_amphibian AS 
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Amphibia'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
        )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_amphibian_scientific_name_like ON sb_taxon_amphibian(scientific_name);

CREATE TABLE sb_taxon_mammal AS
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Mammalia'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
    )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_mammal_scientific_name_like ON sb_taxon_mammal(scientific_name);

CREATE TABLE sb_taxon_bird AS
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Aves'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
    )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_bird_scientific_name_like ON sb_taxon_bird(scientific_name);

CREATE TABLE sb_taxon_fish AS 
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Actinopterygii' OR t.scientific_name = 'Myxini' OR t.scientific_name = 'Cephalaspidomorphi' OR t.scientific_name = 'Elasmobranchii' OR t.scientific_name = 'Sarcopterygii'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
    )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_fish_scientific_name_like ON sb_taxon_fish(scientific_name);

CREATE TABLE sb_taxon_annelid AS
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Annelida'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
    )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_annelid_scientific_name_like ON sb_taxon_annelid(scientific_name);

CREATE TABLE sb_taxon_mollusk AS
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Mollusca'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
    )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_mollusk_scientific_name_like ON sb_taxon_mollusk(scientific_name);

CREATE TABLE sb_taxon_arthropod AS
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Arthropoda'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
    )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_arthropod_scientific_name_like ON sb_taxon_arthropod(scientific_name);

CREATE TABLE sb_taxon_onychophoran AS
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Onychophora'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
    )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_onychophoran_scientific_name_like ON sb_taxon_onychophoran(scientific_name);

CREATE TABLE sb_taxon_animal AS 
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Animalia'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
    )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_animal_scientific_name_like ON sb_taxon_animal(scientific_name);

CREATE TABLE sb_taxon_fungus AS 
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Fungi'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
    )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_fungus_scientific_name_like ON sb_taxon_fungus(scientific_name);

CREATE TABLE sb_taxon_plant AS
    WITH r AS (
        WITH RECURSIVE q AS (
            SELECT * 
            FROM sb_taxon AS t
            WHERE t.scientific_name = 'Plantae'
            UNION ALL
            SELECT p.*
            FROM sb_taxon AS p
            JOIN q
            ON p.parent_name_id = q.col_taxon_id
        )
        SELECT q.*
        FROM q
        UNION ALL
        SELECT sb_taxon.*
        FROM sb_taxon
        JOIN q
        ON sb_taxon.accepted_name_id = q.col_taxon_id
    )
SELECT * FROM r ORDER BY r.scientific_name;
CREATE INDEX sb_taxon_plant_scientific_name_like ON sb_taxon_plant(scientific_name);
