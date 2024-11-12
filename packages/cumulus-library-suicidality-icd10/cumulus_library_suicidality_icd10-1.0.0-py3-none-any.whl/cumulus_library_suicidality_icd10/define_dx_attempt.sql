create or replace view suicide_icd10__define_dx_attempt as select * from (values
('http://hl7.org/fhir/sid/icd-10-cm', 'T14.91', 'Suicide attempt')
,('http://hl7.org/fhir/sid/icd-10-cm', 'T14.91XA', 'Suicide attempt, initial encounter')
,('http://hl7.org/fhir/sid/icd-10-cm', 'T14.91XD', 'Suicide attempt, subsequent encounter')
,('http://hl7.org/fhir/sid/icd-10-cm', 'T14.91XS', 'Suicide attempt, sequela')
) AS t (system, code, display) ;