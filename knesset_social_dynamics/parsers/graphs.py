import math

import networkx as nx
import pandas as pd

from knesset_social_dynamics.parsers.utils import extract_rolling_windows


def extract_transcript_graph(transcript, g_type='adjust_speaker'):
    if g_type == 'adjust_speaker':
        # TODO: use committee_trans.shift() and not the windows func
        speaker_windows = extract_rolling_windows(transcript['speaker_name'])

        adjust_list = []
        for ed in speaker_windows:
            adjust_list.append(ed[[0, 1]])
            adjust_list.append(ed[[1, 2]])

        df = pd.DataFrame(adjust_list, columns=['source', 'target'])
        df = df.drop_duplicates()
        df = df[df.source != df.target]
        df['source'] = df['source'].apply(lambda x: x[::-1])
        df['target'] = df['target'].apply(lambda x: x[::-1])
        return nx.convert_matrix.from_pandas_edgelist(df)

    if g_type == "direct_indirect":
        sequence_speakers = []
        texts = []
        last_speaker = ''
        for i, row in transcript.iterrows():
            if row['speaker_name'] == '' or (type(row['speaker_name']) == float and math.isnan(row['speaker_name'])):
                continue
            if row['speaker_name'] != last_speaker:
                sequence_speakers.append(row['speaker_name'])
                texts.append(row['text'])
            else:
                texts[-1] += row['text']
            last_speaker = row['speaker_name']

        # check for indirect reference
        indirect_reference = ['אתה', 'לך', 'שאתה', ' שאת ']

        indirect_references = []
        for i, (speaker, text) in enumerate(zip(sequence_speakers, texts)):
            indirect_references += list(set(
                [(speaker, sequence_speakers[i - 1]) for word in indirect_reference if (word in text)]))

        # check for direct reference
        unique_speakers = set(sequence_speakers)
        name_parts = {
            name: name.replace('סגן', ' ').replace('שר', ' ').replace('התקשורת', ' ').replace('החינוך', ' ').replace(
                'הפנים', ' ').replace('התיירות', ' ').replace('האוצר', ' ').replace('הבריאות', ' ').strip().split(' ')
            for
            name in unique_speakers}

        direct_references = []
        for i, (speaker, text) in enumerate(zip(sequence_speakers, texts)):
            direct_references += list(set(
                [(speaker, name) for name in name_parts.keys() for part in name_parts[name] if part in text]))

        df = pd.DataFrame(direct_references + indirect_references, columns=['source', 'target'])
        df = df.drop_duplicates()
        df = df[df.source != df.target]
        df['source'] = df['source'].apply(lambda x: x[::-1])
        df['target'] = df['target'].apply(lambda x: x[::-1])
        return nx.convert_matrix.from_pandas_edgelist(df)

    if g_type == "committee_breaking":
        sequence_speakers = []
        texts = []
        last_speaker = ''
        for i, row in transcript.iterrows():
            if row['speaker_name'] == '' or (type(row['speaker_name']) == float and math.isnan(row['speaker_name'])):
                continue
            if row['speaker_name'] != last_speaker:
                sequence_speakers.append(row['speaker_name'])
                texts.append(row['text'])
            else:
                texts[-1] += row['text']
            last_speaker = row['speaker_name']

        committee_breaking_pairs = []
        for i, (speaker, text) in enumerate(zip(sequence_speakers, texts)):
            if '- - -' in text:
                committee_breaking_pairs.append((sequence_speakers[i + 1], speaker))

        df = pd.DataFrame(committee_breaking_pairs, columns=['source', 'target'])
        df = df.drop_duplicates()
        df = df[df.source != df.target]
        df['source'] = df['source'].apply(lambda x: x[::-1])
        df['target'] = df['target'].apply(lambda x: x[::-1])
        return nx.convert_matrix.from_pandas_edgelist(df)
