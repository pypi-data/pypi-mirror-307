create or replace view suicide_icd10__define_dx as
with dx_subtypes as
(
    select 'attempt' as subtype, * from suicide_icd10__define_dx_attempt
    UNION
    select 'ideation' as subtype, * from suicide_icd10__define_dx_ideation
    UNION
    select 'self_harm' as subtype, * from suicide_icd10__define_dx_self_harm
)
select * from dx_subtypes order by subtype, code
