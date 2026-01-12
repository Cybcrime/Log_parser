from argparse import ArgumentParser
from zipfile import ZipFile
from re import search, IGNORECASE
from os import listdir
from os import path


def get_args():
    print('Reading args\n')
    parser = ArgumentParser()
    parser.add_argument('-w', '--wordlist_file_path', default='wordlist.txt') # txt file with client keywords, one per line
    parser.add_argument('-e', '--extracted_folder_path', default='extracted') # folder name where we store extractions
    parser.add_argument('-o', '--output_file_path', default='output.txt') # output file to store results
    args = parser.parse_args()
    return args

def get_keywords(wordlist_path):
    print('Reading keywords from {}'.format(wordlist_path))
    keywords = list()
    with open(wordlist_path, 'r') as file:
        for line in file.readlines():
            if line.strip() != '':
                keywords.append(line.strip())
    return keywords

def match_bloc(keyword, bloc):
    m = search('{}'.format(keyword), bloc, IGNORECASE)
    return m

def write_bloc(bloc, output_file):
    print('Writing bloc \n\n{} \n\nto output file {}\n'.format(bloc, output_file))
    with open(output_file, 'a+') as file:
        file.write('{}\n\n'.format(bloc))

def check_output(output_file):
    if output_file in listdir():
        print('Output file "{}" already exists. Exiting'.format(output_file))
        exit()

def get_passwords_file_blocs(location):
    print('Reading passwords from {}'.format(location))
    if path.isfile('{}/Passwords.txt'.format(location)):
        password_path = '{}/Passwords.txt'.format(location)
    else:
        password_path = '{}/passwords.txt'.format(location)
    with open(password_path, 'r') as f:
        return f.read().split('\n\n')

def extract_packs(extraction_folder):
    directory_list = listdir()
    if extraction_folder in directory_list:
        print('Extraction folder "{}" already exists. Exiting'.format(extraction_folder))
        exit()

    for element in directory_list:
        if element.lower().startswith('logid') and element.lower().endswith('.zip'):
            in_current_folder = True
            with ZipFile(element, 'r') as zipped_pack:
                zipped_pack.extractall('{}/{}'.format(extraction_folder, element.split('.zip')[0]))
                print('Extracted {}'.format(element))

    if not in_current_folder:
        print('Not in current folder, no logid archive found. Exiting')
        exit()

def clean_extractions():
    pass

def main():
    args = get_args()
    check_output(args.output_file_path)
    extract_packs(args.extracted_folder_path)
    keywords = get_keywords(args.wordlist_file_path)
    for element in listdir(args.extracted_folder_path):
        write_bloc(element, args.output_file_path)
        passwords_blocs = get_passwords_file_blocs('{}/{}'.format(args.extracted_folder_path, element))
        for bloc in passwords_blocs:
            bloc_written = False
            for keyword in keywords:
                if match_bloc(keyword, bloc) and not bloc_written:
                    write_bloc(bloc, args.output_file_path)
                    bloc_written = True
    
if __name__ == '__main__':
    main()
