import pandas as pd

from knesset_social_dynamics.parsers.text_extractor import extract_raw_protocol
from knesset_social_dynamics.parsers.utils import parse_speaker


def extract_committee_new_transcript(committe_file_path):
    """
    DataFrame columns

    interaction_type, speaker, subject, text
    :param plenum_file_path:
    :return:
    """

    raw_text = extract_raw_protocol(committe_file_path)

    # remove empty lines
    no_empty_lines = [line for line in raw_text if len(line.strip()) > 0]

    text = []
    subject = ""
    interaction = ""
    speaker_name = ""
    speaker_party = ""
    # start_talking = no_empty_lines.index('רישום פרלמנטרי:')
    parlimant_writing = ['רישום פרלמנטרי:', 'קצרנית פרלמנטרית:']
    start_talking = [i for i, line in enumerate(no_empty_lines) for word in parlimant_writing if word in line][0]
    for line in no_empty_lines[start_talking + 2:]:
        if "<< נושא >>" in line:
            subject = line.split("<< נושא >>")[1]
            continue
        if "<< הצח >>" in line:
            subject = line.split("<< הצח >>")[1]
            continue
        if "<< דובר >>" in line:
            speaker = line.split("<< דובר >>")[1]
            interaction = "<< דובר >>"
            speaker_name, speaker_party = parse_speaker(speaker)
            continue
        if "<< דובר_המשך >>" in line:
            speaker = line.split("<< דובר_המשך >>")[1]
            interaction = "<< דובר_המשך >>"
            speaker_name, speaker_party = parse_speaker(speaker)
            continue
        if "<< יור >>" in line:
            speaker = line.split("<< יור >>")[1]
            interaction = "<< יור >>"
            speaker_name, speaker_party = parse_speaker(speaker)
            continue
        if "<< קריאה >>" in line:
            speaker = line.split("<< קריאה >>")[1]
            if speaker in ["קריאות", "קריאה"]:
                speaker_name, speaker_party = "unkown", "unkown"
            interaction = "<< קריאה >>"
            continue
        if "<< סיום >>" in line:
            continue
        if speaker_name == "":
            continue
        text.append([interaction, speaker_name, speaker_party, subject, line])

    return pd.DataFrame(text, columns=['interaction', 'speaker_name', 'speaker_party', 'subject', 'text'])
