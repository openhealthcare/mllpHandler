from collections import defaultdict

import pytds

from gloss.conf import settings
from gloss import message_type

TABLE_NAME = "something"


class InvalidAssumption(Exception):
    pass


def cast_row_to_patient(row):
    sex_abbreviation = row.get("SEX")

    if sex_abbreviation == "M":
        sex = "Male"
    else:
        sex = "Female"

    return message_type.PatientMessage(
        surname=row.get("Surname"),
        first_name=row.get("Firstname"),
        sex=sex,
        title=row.get("title"),
        date_of_birth=row.get("date_of_birth")
    )


def cast_row_to_observation(row):
    status_abbr = row.get("OBX_Status")

    if status_abbr == 'F':
        status = "Final"
    else:
        status = "Interim"
    return message_type.ObservationMessage(
        test_code=row.get("OBX_exam_code_ID"),
        test_name=row.get("OBX_exam_code_Text"),
        observation_value=row.get("Result_Value"),
        units=row.get("Result_Units"),
        result_status=status,
        reference_range=row.get("Result_Range"),
        external_identifier=str(row.get("OBX_id")),
    )


def cast_rows_to_result_message(grouped_rows):
    observations = [
        cast_row_to_observation(row) for row in grouped_rows
    ]
    last_row = grouped_rows[-1]
    status_abbr = row.get("OBR_Status")

    if status_abbr == 'F':
        status = "Final"
    else:
        status = "Interim"

    return message_type.ResultMessage(
        lab_number=get_unique_result_identifier(last_row),
        profile_code=last_row.get("OBR_exam_code_ID"),
        profile_description=last_row.get("OBR_exam_code_Text"),
        request_datetime=last_row.get("Request_Date"),
        # there's Date of observation and observation datetime
        # and they're different TODO check this
        observation_datetime=last_row.get("Date_of_the_Observation"),
        last_edited=last_row.get("last_updated"),
        observations=observations,
        result_status=status
    )


def get_unique_result_identifier(row):
    return "{0}_{1}".format(row["Result_ID"], row["OBR_Sequence_ID"])

def get_results_and_observations(rows):
    # going through the result_id seems to be the set id of the OBR
    # the set id is not unique as there can be multiple OBRs, even of the
    # same type, but we can use the set id and the sequence id to create a unique
    # reference...
    # TODO double check this is correct and not just a feature of the
    # test data

    grouped = defaultdict(list)
    for row in rows:
        grouped[get_unique_result_identifier(row)].append(row)

    for rows in grouped.values():
        only_one_test = {i["OBR_exam_code_ID"] for i in rows}
        if(not len(only_one_test) == 1):
            err_message = "we expected only one type of test for a result id"
            err_message += "for {} we received multiple".format(row["Result_ID"])
            raise InvalidAssumption(err_message)

    messages = []

    for grouped_rows in grouped.values():
        messages.append(cast_rows_to_result_message(grouped_rows))

    return messages


def get_rows(hospital_number):
    username = settings.db_username
    password = settings.db_password
    server = settings.server
    database = settings.database
    query = """
    select * from tQuest_Pathology_Result_View where Patient_Number='{}' ORDER BY Event_Date
    """.format(hospital_number)

    with pytds.connect(server, database, username, password) as conn:
        with conn.cursor() as cur:
            cur.execute(query.strip())
            result = cur.fetch_many()

    return result

# def get_rows(hospital_number):
#     # temporary cover so you don't need to set up a database
#     from sites.rfh.test_database_constructor.pathology_data import PATHOLOGY_DATA
#     return [y for y in PATHOLOGY_DATA if y["Patient_Number"] == hospital_number]

def patient_information(hospital_number):
    # TODO this assumes an RFH identifier, the data also has
    # an NHS number so we should allow both
    rows = get_rows(hospital_number)
    if len(rows):
        messages = get_results_and_observations(rows)
        messages.append(cast_row_to_patient(rows[-1]))
    return message_type.MessageContainer(
        hospital_number=hospital_number,
        issuing_source="rfh",
        messages=messages
    )
