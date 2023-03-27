SELECT DISTINCT 
    pu.username AS USERNAME,
    TO_CHAR(pu.person_id) AS AGENT_ID,
    ppf.display_name AS DISPLAY_NAME
FROM 
    per_users pu,
    per_person_names_f_v ppf
WHERE 
    ppf.person_id = pu.person_id
ORDER BY 
    pu.username

