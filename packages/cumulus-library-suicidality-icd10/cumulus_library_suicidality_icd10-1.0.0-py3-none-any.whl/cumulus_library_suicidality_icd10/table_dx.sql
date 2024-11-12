create TABLE suicide_icd10__dx as
    select distinct
        DX.subtype as dx_subtype,
        DX.system  as dx_system,
        DX.code    as dx_code,
        DX.display as dx_display,
        concat(DX.code, ' : ', DX.display) as dx_code_display,
        S.doc_ed_note,
        S.diff_enc_note_days,
        S.period,
        S.age_group,
        S.age_at_visit,
        S.gender,
        S.race_display,
        S.ethnicity_display,
        S.enc_class_code,
        S.doc_type_code,
        S.doc_type_display,
        C.code as cond_category,
        C.recordeddate_week as cond_week, -- FHIR Condition
        C.recordeddate_month as cond_month,
        C.recordeddate_year as cond_year,
        S.enc_start_date, -- FHIR Encounter
        S.enc_start_week,
        S.enc_start_month,
        S.enc_end_date,
        S.doc_author_date, -- FHIR DocumentReference
        S.doc_author_week,
        S.doc_author_month,
        S.doc_author_year,
        S.subject_ref,
        S.encounter_ref,
        S.documentreference_ref,
        S.status
    from  core__condition C
        ,   suicide_icd10__study_period S
        ,   suicide_icd10__define_dx DX
    where C.code = DX.code
    and   C.encounter_ref = S.encounter_ref
    and   C.subject_ref = S.subject_ref
    order by recordeddate_month desc, subtype, dx_code
;
