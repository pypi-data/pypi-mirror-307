create or replace view suicide_icd10__define_study_period as select * from (VALUES
  ('before-covid', date('2016-06-01'), date('2020-03-01'))
 ,('before-delta', date('2020-03-01'), date('2021-06-20'))
 ,('delta',     date('2021-06-21'), date('2021-12-19'))
 ,('omicron',   date('2021-12-20'), date('2023-06-01')))
AS t (period, period_start, period_end)
;
