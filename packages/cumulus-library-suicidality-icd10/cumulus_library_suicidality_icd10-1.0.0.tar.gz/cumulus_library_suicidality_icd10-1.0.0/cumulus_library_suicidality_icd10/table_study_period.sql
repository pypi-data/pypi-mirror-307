drop table if exists suicide_icd10__study_period;
create TABLE suicide_icd10__study_period AS
WITH documented_encounter AS (
    SELECT DISTINCT
        ce.period_start_day,
        ce.period_start_week,
        ce.period_start_month,
        ce.period_end_day,
        ce.age_at_visit,
        cdr.author_day,
        cdr.author_week,
        cdr.author_month,
        cdr.author_year,
        cp.gender,
        cp.race_display,
        cp.ethnicity_display,
        cp.subject_ref,
        ce.encounter_ref,
        ce.status,
        cdr.documentreference_ref,
        date_diff(
            'day', ce.period_start_day, date(cdr.author_day)
        ) AS diff_enc_note_days,
        coalesce(ce.class_code, 'None') AS enc_class_code,
        coalesce(ce.class_display, 'None') AS enc_class_display,
        coalesce(cdr.type_code, 'None') AS doc_type_code,
        coalesce(cdr.type_display, 'None') AS doc_type_display
    FROM
        core__patient AS cp,
        core__encounter AS ce,
        core__documentreference AS cdr
    WHERE
        (cp.subject_ref = ce.subject_ref)
        AND (ce.encounter_ref = cdr.encounter_ref)
        AND (cdr.author_day BETWEEN date('2016-06-01') AND current_date)
        AND (ce.period_start_day BETWEEN date('2016-06-01') AND current_date)
        AND (ce.period_end_day BETWEEN date('2016-06-01') AND current_date)
),
encounter_with_note AS (
    SELECT
        de.period_start_day,
        de.period_start_week,
        de.period_start_month,
        de.period_end_day,
        de.age_at_visit,
        de.author_day,
        de.author_week,
        de.author_month,
        de.author_year,
        de.gender,
        de.race_display,
        de.ethnicity_display,
        de.subject_ref,
        de.encounter_ref,
        de.status,
        de.documentreference_ref,
        de.diff_enc_note_days,
        de.enc_class_code,
        de.enc_class_display,
        de.doc_type_code,
        de.doc_type_display,
        coalesce(ed.code IS NOT NULL, FALSE) AS ed_note
    FROM documented_encounter AS de
    LEFT JOIN core__ed_note AS ed
        ON de.doc_type_code = ed.from_code
)

    select distinct P.period, A.age_group,
        S.ed_note as doc_ed_note,
        S.diff_enc_note_days,
        S.age_at_visit,
        S.gender,
        S.race_display,
        S.ethnicity_display,
        S.enc_class_code,
        S.enc_class_display,
        S.doc_type_code,
        S.doc_type_display,
        S.period_start_day as enc_start_date, -- FHIR Encounter
        S.period_start_week as enc_start_week,
        S.period_start_month as enc_start_month,
        S.period_end_day as enc_end_date,
        S.author_day as doc_author_date, -- FHIR DocumentReference
        S.author_week as doc_author_week,
        S.author_month as doc_author_month,
        S.author_year as doc_author_year,
        S.subject_ref,
        S.encounter_ref,
        e.status,
        S.documentreference_ref
    from encounter_with_note AS S,
        suicide_icd10__define_age AS A,
        suicide_icd10__define_study_period AS P,
        core__encounter AS e
    where S.age_at_visit = A.age
      and (S.author_day between P.period_start and P.period_end)
      and e.encounter_ref = S.encounter_ref
;
