CREATE OR REPLACE VIEW skill_pairs AS
SELECT
    a.skill AS skill_1,
    b.skill AS skill_2,
    COUNT(*) AS pair_count
FROM posting_skills a
JOIN posting_skills b
    ON a.posting_id = b.posting_id
    AND a.skill < b.skill
GROUP BY a.skill, b.skill;