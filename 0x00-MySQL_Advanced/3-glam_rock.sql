-- 3-glam_rock.sql
-- This script lists all bands with Glam rock as their main style, ranked by their longevity.
-- It uses the `formed` and `split` columns to compute the lifespan of each band.

SELECT 
    band_name, 
    (IFNULL(split, 2022) - formed) AS lifespan
FROM 
    metal_bands
WHERE 
    FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
ORDER BY 
    lifespan DESC;