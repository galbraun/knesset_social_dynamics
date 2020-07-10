import pandas as pd

from knesset_social_dynamics.parsers.text_extractor import extract_raw_protocol
from knesset_social_dynamics.parsers.utils import parse_speaker


def extract_plenum_new_transcript(plenum_file_path):
    """
    DataFrame columns

    interaction_type, speaker, subject, text
    :param plenum_file_path:
    :return:
    """

    raw_text = extract_raw_protocol(plenum_file_path)

    # remove empty lines
    no_empty_lines = [line for line in raw_text if len(line.strip()) > 0]

    text = []
    subject = ""
    interaction = ""
    speaker_name = ""
    speaker_party = ""
    start_talking = [i for i, line in enumerate(no_empty_lines) if 'תוכן העניינים' in line][0]
    status_changed = 1
    for line in no_empty_lines[start_talking + 1:]:
        if "<< הלסי >>" in line:
            subject = line.split("<< הלסי >>")[1]
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
                speaker = "unkown"
            interaction = "<< קריאה >>"
            continue
        if "<< סיום >>" in line:
            continue
        text.append([interaction, speaker_name, speaker_party, subject, line])

    df = pd.DataFrame(text, columns=['interaction', 'speaker_name', 'speaker_party', 'subject', 'text'])
    return df
