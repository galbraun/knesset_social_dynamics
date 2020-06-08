import numpy as np


def parse_speaker(speaker_string):
    if 'היו"ר' in speaker_string:
        return speaker_string.replace('היו"ר', "").replace(":", "").strip(), 'יו"ר'
    else:
        party = speaker_string[speaker_string.find("(") + 1: speaker_string.find(")")].replace(":", "").strip()
        name = speaker_string[:speaker_string.find("(")].strip().replace(":", "")
        return name, party


def extract_rolling_windows(series, window_size=3):
    return np.lib.stride_tricks.as_strided(series, (len(series) - (window_size - 1), window_size),
                                           (series.values.strides * 2))
