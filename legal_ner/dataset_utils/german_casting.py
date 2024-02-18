import json
from uuid import uuid4

from datasets import load_dataset


def find_contiguous_tags(tags):

    indices = []
    start_index = 0

    for i in range(1, len(tags)):
        if tags[i] != tags[start_index]:
            indices.append((start_index, i))
            start_index = i

    indices.append((start_index, len(tags)))
    return indices


def main():

    ner_tags = ['B-AN',
                'B-EUN',
                'B-GRT',
                'B-GS',
                'B-INN',
                'B-LD',
                'B-LDS',
                'B-LIT',
                'B-MRK',
                'B-ORG',
                'B-PER',
                'B-RR',
                'B-RS',
                'B-ST',
                'B-STR',
                'B-UN',
                'B-VO',
                'B-VS',
                'B-VT',
                'I-AN',
                'I-EUN',
                'I-GRT',
                'I-GS',
                'I-INN',
                'I-LD',
                'I-LDS',
                'I-LIT',
                'I-MRK',
                'I-ORG',
                'I-PER',
                'I-RR',
                'I-RS',
                'I-ST',
                'I-STR',
                'I-UN',
                'I-VO',
                'I-VS',
                'I-VT',
                'O']

    ner_coarse_tags = ['B-LIT',
                       'B-LOC',
                       'B-NRM',
                       'B-ORG',
                       'B-PER',
                       'B-REG',
                       'B-RS',
                       'I-LIT',
                       'I-LOC',
                       'I-NRM',
                       'I-ORG',
                       'I-PER',
                       'I-REG',
                       'I-RS',
                       'O']

    dataset = load_dataset("elenanereiss/german-ler")

    for env, dataset in dataset.items():

        env_list = []

        for token in dataset:

            token['len_tokens'] = list(map(lambda x: len(x), token['tokens']))

            tags_indices = find_contiguous_tags(token['ner_coarse_tags'])

            new_dict = {
                'id': str(uuid4()),
                'data': {'text': ' '.join(token['tokens'])}
            }

            new_dict['annotations'] = []
            new_dict['annotations'].append({})
            new_dict['annotations'][0]['result'] = []

            for f, t in tags_indices:

                # We are using coarse tags since they align better with the Spanish dataset
                # Drop the O tags since they don't convey legal information and are absent in the other dataset
                if ner_coarse_tags[token['ner_coarse_tags'][f]] != 'O':

                    new_dict['annotations'][0]['result'].append({
                        'value': {
                            'start': sum(token['len_tokens'][0:f], f),
                            # -1 to remove the trailing space
                            'end': sum(token['len_tokens'][0:t], t) - 1,
                            'text': ' '.join(token['tokens'][f:t]),
                            'labels': [ner_coarse_tags[token['ner_coarse_tags'][f]][2:]]
                        },
                        'id': str(uuid4()),
                        'from_name': 'label',
                        'to_name': 'text',
                        'type': 'labels',
                    })

            env_list.append(new_dict)

        with open(f'de_{env}.json', 'w') as fp:
            json.dump(env_list, fp)


if __name__ == "__main__":
    main()
