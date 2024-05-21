import os, sys, csv

def load_tsv_file(filename):

    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f, delimiter='\t') # 17 columns
        data = list(reader)
        for i, d in enumerate(data):
            if len(d) != 17:
                print(f"Error in row {i} of file {filename}")
                print(len(d))
                print('--'*5)
                for e in d:
                    print(e)
                    print('--'*5)
                sys.exit(1)
    return data

def load_tsv_file_2(filename):
    rows = []
    with open(filename, 'r', encoding='utf-8-sig') as f:
        for i, line in enumerate(f):
            row = line.strip().split('\t')
            rows.append(row)
            if len(row) != 17:
                print(f"Error in row {i} of file {filename}")
                print(len(row))
                print('--'*5)
                for e in row:
                    print(e)
                    print('--'*5)
                sys.exit(1)
    return rows

def write_csv_file(filename, data):
        with open(filename, 'w', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerows(data)

def extract_lang_data(data, header = True):
    lang_to_data = {}
    if header:
        data = data[1:]
    
    for row in data:
        lang = row[0]
        if lang not in lang_to_data:
            lang_to_data[lang] = []
        lang_to_data[lang].append(row)
    
    return lang_to_data

if __name__ == "__main__":

    data_dir = sys.argv[1]
    filenames = ['dev.all.tsv', 'ood.tsv', 'test.all.tsv', 'train.all.tsv', 'zeroshot.tsv']

    subset_names = ['dev', 'ood', 'test', 'train', 'zeroshot']

    lang_to_subset = {}
    header = load_tsv_file_2(os.path.join(data_dir, "train.all.tsv"))[0]
    print("header is ")
    print(header)
    lang_to_subset['all_languages'] = {}
    for i, file in enumerate(filenames):
        subset = subset_names[i]
        data = load_tsv_file_2(os.path.join(data_dir, file))
        lang_to_subset['all_languages'][subset] = data[1:]
        print(f'Total number of rows in file {file}: {len(data)}')
        lang_to_data = extract_lang_data(data)
        for lang, rows in lang_to_data.items():
            if lang not in lang_to_subset:
                lang_to_subset[lang] = {}
            if subset not in lang_to_subset[lang]:
                lang_to_subset[lang][subset] = []
            lang_to_subset[lang][subset].extend(rows)
    

    for lang in lang_to_subset:
        for subset in lang_to_subset[lang]:
            print(f"Language: {lang}, Subset: {subset}, Num Examples: {len(lang_to_subset[lang][subset])}")
    

    for lang in lang_to_subset:
        # create lang directory
        lang_dir = os.path.join(data_dir, lang)
        os.makedirs(lang_dir, exist_ok=True)
        lang_data = lang_to_subset[lang]
        for subset in lang_data:
            subset_data = [header]
            subset_data.extend(lang_data[subset])
            write_csv_file(os.path.join(lang_dir, f"{subset}-00000-of-00001.csv"), subset_data)
