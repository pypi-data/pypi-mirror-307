create or replace view suicide_icd10__define_note as select * from
(VALUES
        ('BCH', 'NOTE:149798455', 'Emergency MD',                         'http://loinc.org','34878-9', 'Emergency medicine Note')
      , ('BCH', 'NOTE:189094716', 'Psychiatry Evaluation',                'http://loinc.org','97696-9', 'Psychiatry Evaluation note')
      , ('BCH', 'NOTE:262402257', 'Psychiatry Evaluation Consultation',   'http://loinc.org','34788-0', 'Psychiatry Consult note')
      , ('BCH', 'NOTE:3710478',   'Discharge Summary',                   'http://loinc.org','18842-5',  'Discharge summary')
)
as t(from_system, from_code, from_display, system, code, display)
;
