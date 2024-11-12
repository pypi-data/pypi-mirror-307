create or replace view suicide_icd10__define_dx_ideation as select * from (values
('http://hl7.org/fhir/sid/icd-10-cm', 'R45.851', 'Suicidal ideations')
) AS t (system, code, display) ;