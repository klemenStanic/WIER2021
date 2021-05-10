from models import *
from utils import *
import os
import sys

session = Session(engine)


def import_data_item(filename, data_item):
    for word in data_item.keys():
        #  Inserting the word in IndexWord table
        if session.query(IndexWord).filter(IndexWord.word == word).first() is None:
            i_word = IndexWord()
            i_word.word = word
            session.add(i_word)
            session.commit()

        # Inserting new posting
        posting = Posting()
        posting.word = word
        posting.document_name = filename
        posting.frequency = len(data_item[word])
        posting.indexes = ','.join([str(i) for i in data_item[word]])
        session.add(posting)
        session.commit()


def import_data():
    data_dir = '../data/'
    for dir in os.listdir(data_dir):
        if dir == 'nltk_data':
            continue
        site_dir = os.path.join(data_dir, dir)
        for file_name in os.listdir(site_dir):
            file_path = os.path.join(site_dir, file_name)
            print(f'Importing file: {file_path}')
            with open(file_path, 'r') as file:
                file_text = file.read()
                file_text = get_only_text_from_html(file_text)
                indexed_data = preprocess_text(file_text)
                import_data_item(file_path, indexed_data)


if __name__ == '__main__':
    import_data()
    sys.exit()

    time_start = time.time()

    if len(sys.argv) != 2:
        print('Please enter query string.')
        sys.exit()

    queries = list(preprocess_text(sys.argv[1]).keys())
    print(f'Results for a query: {sys.argv[1]}')

    results = []
    for q in queries:
        tmp_rslt = session.query(Posting).filter(Posting.word == q).all()
        if tmp_rslt is not None:
            results.extend(tmp_rslt)

    results.sort(reverse=True, key=lambda x: x.document_name)

    i = 1  # aggregating data
    while i < len(results):
        if results[i-1].document_name == results[i].document_name:
            results[i-1].frequency += results[i].frequency
            results[i - 1].indexes += ',' + results[i].indexes
            results.pop(i)
        else:
            i += 1

    results.sort(reverse=True, key=lambda x: x.frequency)

    for result in results:
        print(f'Document: {result.document_name}')
        print(f'Frequency: {result.frequency}')
        for i in find_surroundings(result.document_name, result.indexes):
            print(f'... {i} ', end='')
        print('...\n---------------------')

    time_end = time.time()
