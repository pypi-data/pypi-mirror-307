import pathlib

import cumulus_library

class SuicideICD10CountsBuilder(cumulus_library.CountsBuilder):
    display_text = "Creating Suicide ICD10 counts..."

    def count_dx(self, duration='month'):
        """
        Encounter Diagnosis, not exactly 'incidence' because DX may not be "new".

        Stratify variables for "documented encounter"

        :return: str suicide_icd10__count_dx_month
        """
        view_name = self.get_table_name('count_dx', duration)
        from_table = self.get_table_name('dx')
        cols = [f'cond_{duration}',
                'dx_subtype',
                'dx_display',
                'gender',
                'race_display',
                'age_at_visit',
                'enc_class_code',
                'doc_ed_note',
                'doc_type_display']
        return self.count_encounter(view_name, from_table, cols)

    def count_prevalence(self, duration='month'):
        """
        Percentage of patients with a suicidality diagnosis

        :return: str suicide_icd10__count_prevalence_month
        """
        view_name = self.get_table_name('count_prevalence', duration)
        from_table = self.get_table_name('prevalence')
        cols = [f'enc_start_{duration}',
                'dx_suicidality',
                'dx_subtype',
                'period',
                'gender',
                'age_group',
                'doc_ed_note',
                'enc_class_code']

        return self.count_encounter(view_name, from_table, cols)

    def count_study_period(self, duration='month'):
        """
        Frequency of documented encounters.
        This is just the *study period* BEFORE selecting for suicidality DX

        :return: str suicide_icd10__count_study_period_month
        """
        view_name = self.get_table_name('count_study_period', duration)
        from_table = self.get_table_name('study_period')
        cols = [f'enc_start_{duration}',
                'period',
                'gender',
                'age_group',
                'race_display',
                'doc_ed_note',
                'enc_class_code',
                'doc_type_display']

        return self.count_encounter(view_name, from_table, cols)


    def prepare_queries(self, *args,**kwargs):
        self.queries=[
            self.count_dx(),
            self.count_prevalence(),
            self.count_study_period()
        ]

if __name__ == "__main__":
    builder = SuicideICD10CountsBuilder()
    builder.write_counts(f"{pathlib.Path(__file__).resolve().parent}/counts.sql")