drop table if exists suicide_icd10__prevalence;

create TABLE suicide_icd10__prevalence AS
    select distinct
        case when DX.dx_subtype is not null then TRUE else FALSE end as dx_suicidality,
        coalesce(DX.dx_subtype, 'None') as dx_subtype,
        coalesce(DX.dx_code, 'None') as dx_code,
        coalesce(DX.dx_display, 'None') as dx_display,
        coalesce(DX.dx_code_display, 'None') as dx_code_display,
        S.*
    from suicide_icd10__study_period as S
    left join suicide_icd10__dx as DX on S.encounter_ref = DX.encounter_ref;
