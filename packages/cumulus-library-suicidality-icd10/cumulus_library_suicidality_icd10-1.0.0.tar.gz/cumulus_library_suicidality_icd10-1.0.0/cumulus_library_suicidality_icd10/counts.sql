-- noqa: disable=all

CREATE TABLE suicide_icd10__count_dx_month AS (
    WITH powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject,
            count(DISTINCT encounter_ref) AS cnt_encounter,
            "cond_month",
            "dx_subtype",
            "dx_display",
            "gender",
            "race_display",
            "age_at_visit",
            "enc_class_code",
            "doc_ed_note",
            "doc_type_display"
        FROM suicide_icd10__dx
        GROUP BY
            cube(
                "cond_month",
                "dx_subtype",
                "dx_display",
                "gender",
                "race_display",
                "age_at_visit",
                "enc_class_code",
                "doc_ed_note",
                "doc_type_display"
            )
    )

    SELECT
        cnt_encounter AS cnt,
        "cond_month",
        "dx_subtype",
        "dx_display",
        "gender",
        "race_display",
        "age_at_visit",
        "enc_class_code",
        "doc_ed_note",
        "doc_type_display"
    FROM powerset
    WHERE 
        cnt_subject >= 10
);

-- ###########################################################

CREATE TABLE suicide_icd10__count_prevalence_month AS (
    WITH powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject,
            count(DISTINCT encounter_ref) AS cnt_encounter,
            "enc_start_month",
            "dx_suicidality",
            "dx_subtype",
            "period",
            "gender",
            "age_group",
            "doc_ed_note",
            "enc_class_code"
        FROM suicide_icd10__prevalence
        GROUP BY
            cube(
                "enc_start_month",
                "dx_suicidality",
                "dx_subtype",
                "period",
                "gender",
                "age_group",
                "doc_ed_note",
                "enc_class_code"
            )
    )

    SELECT
        cnt_encounter AS cnt,
        "enc_start_month",
        "dx_suicidality",
        "dx_subtype",
        "period",
        "gender",
        "age_group",
        "doc_ed_note",
        "enc_class_code"
    FROM powerset
    WHERE 
        cnt_subject >= 10
);

-- ###########################################################

CREATE TABLE suicide_icd10__count_study_period_month AS (
    WITH powerset AS (
        SELECT
            count(DISTINCT subject_ref) AS cnt_subject,
            count(DISTINCT encounter_ref) AS cnt_encounter,
            "enc_start_month",
            "period",
            "gender",
            "age_group",
            "race_display",
            "doc_ed_note",
            "enc_class_code",
            "doc_type_display"
        FROM suicide_icd10__study_period
        GROUP BY
            cube(
                "enc_start_month",
                "period",
                "gender",
                "age_group",
                "race_display",
                "doc_ed_note",
                "enc_class_code",
                "doc_type_display"
            )
    )

    SELECT
        cnt_encounter AS cnt,
        "enc_start_month",
        "period",
        "gender",
        "age_group",
        "race_display",
        "doc_ed_note",
        "enc_class_code",
        "doc_type_display"
    FROM powerset
    WHERE 
        cnt_subject >= 10
);
