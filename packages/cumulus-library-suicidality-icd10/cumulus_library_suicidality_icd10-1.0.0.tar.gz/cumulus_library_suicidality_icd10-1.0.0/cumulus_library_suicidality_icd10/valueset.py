import os
from typing import List
from fhirclient.models.coding import Coding

from cumulus_library.helper import load_json
from cumulus_library.schema.typesystem import Vocab

# https://github.com/smart-on-fhir/cumulus-library-template/issues/3
STUDY_PREFIX = 'suicide_icd10'

def get_path(filename=None):
    if filename:
        return os.path.join(os.path.dirname(__file__), filename)
    else:
        return os.path.dirname(__file__)

def escape(sql: str) -> str:
    """
    :param sql: SQL potentially containing special chars
    :return: special chars removed like tic(') and semi(;).
    """
    return sql.replace("'", "").replace(";", ".")

def coding2view(view_name: str, concept_list: List[Coding]) -> str:
    """
    :param view_name: like define_type
    :param concept_list: list of concepts to include in definition
    :return: SQL command
    """
    header = f"create or replace view {STUDY_PREFIX}__{view_name} as select * from (values"
    footer = ") AS t (system, code, display) ;"
    content = list()
    for concept in concept_list:
        safe_display = escape(concept.display)
        content.append(f"('{concept.system}', '{concept.code}', '{safe_display}')")
    content = '\n,'.join(content)
    return header + '\n' + content + '\n' + footer

def save(view_name: str, view_sql: str, outfile=None) -> str:
    """
    :param view_name: create view as
    :param view_sql: SQL commands
    :param outfile: default view_name.sql
    :return: outfile path
    """
    if not outfile:
        outfile = get_path(f'{view_name}.sql')
    print(f'\nsave({view_name})')
    print(f'{outfile}\n')
    with open(outfile, 'w') as fp:
        fp.write(view_sql)
    return outfile

def valueset2coding(valueset_json) -> List[Coding]:
    """
    Obtain a list of Coding "concepts" from a ValueSet.
    This method currently supports only "include" of "concept" defined fields.
    Not supported: recursive fetching of contained ValueSets, which requires UMLS API Key and Wget, etc.

    examples
    https://vsac.nlm.nih.gov/valueset/2.16.840.1.113762.1.4.1146.1629/expansion/Latest
    https://cts.nlm.nih.gov/fhir/res/ValueSet/2.16.840.1.113762.1.4.1146.1629?_format=json

    :param valueset_json: ValueSet file, expecially those provided by NLM/ONC/VSAC
    :return: list of codeable concepts (system, code, display) to include
    """
    filepath = get_path(valueset_json)
    print(f'\nvalueset:{filepath}')

    valueset = load_json(get_path(valueset_json))
    parsed = list()

    for include in valueset['compose']['include']:
        if 'concept' in include.keys():
            for concept in include['concept']:
                concept['system'] = include['system']
                parsed.append(Coding(concept))
    return parsed

def define_dx_icd10():
    """
    Curated by CHIP team collaboratively, downloaded as TSV file.
    https://docs.google.com/spreadsheets/d/1AE4jBWGZF0Anfh7y4mx-T4nhNFNXlZgVJnHj3i-hv70/edit#gid=2147019001
    """
    filepath = get_path('valueset_dx_icd10_chip.tsv')
    attempt = list()
    self_harm = list()
    ideation = list()

    with open(filepath, 'r') as fp:
        for line in fp.readlines():
            subtype, code, display, comment = line.split('\t')

            if len(code) < 3:
                print(f'CODE not recognized= "{code}" in {line}')
            else:
                coding = Coding({'system': Vocab.ICD10.value, 'code': code, 'display': display})

                if subtype == 'SUBTYPE':
                    pass
                elif subtype == 'attempt':
                    attempt.append(coding)
                elif subtype == 'self_harm':
                    self_harm.append(coding)
                elif subtype == 'ideation':
                    ideation.append(coding)
                else:
                    print(f'SUBTYPE not recognized= "{subtype}" in {line}')

        view_name = 'define_dx_attempt'
        save(view_name, coding2view(view_name, attempt))

        view_name = 'define_dx_self_harm'
        save(view_name, coding2view(view_name, self_harm))

        view_name = 'define_dx_ideation'
        save(view_name, coding2view(view_name, ideation))

def define_dx_snomed():

    view_name = 'define_dx_attempt_snomed'
    save(view_name, coding2view(view_name,
                                valueset2coding('valueset_dx_snomed_cste.json')))


if __name__ == "__main__":
    define_dx_icd10()
    define_dx_snomed()
