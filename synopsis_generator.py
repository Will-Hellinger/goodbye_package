import json
import pyinflect
import unicodedata
import re
import glob
import os
import sys


if os.name == 'nt':
    subdirectory = '\\'
else:
    subdirectory = '/'

conjugation_chart_key = json.load(open(f'.{subdirectory}data{subdirectory}conjugation_chart_types.json'))
blocks = ('e', 'b', 'c', 'd')

conjugation_names = tuple(conjugation_chart_key.keys())
total_conjugations = tuple(conjugation_chart_key.values())

help_commands = ('-h', '--h', '-help', '--help')


def strip_accents(text):
    return ''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')


def save_file(file: bytes, data: dict):
    file.seek(0)
    json.dump(data, file, indent=4)
    file.truncate()


def generate_synopsis(english_word: str, tense: str, latin_words: list, chart: str = None, question_type: str = 'default'):
    tense_types = glob.glob(f'.{subdirectory}data{subdirectory}english-conjugation-charts{subdirectory}*.json')
    tense = f'.{subdirectory}data{subdirectory}english-conjugation-charts{subdirectory}{tense}.json'

    question_types = glob.glob(f'.{subdirectory}data{subdirectory}question-types{subdirectory}*.json')
    question_type = f'.{subdirectory}data{subdirectory}question-types{subdirectory}{question_type}.json'


    ignore_words = ('dic', 'dac', 'fic', 'fuc') #little rhyme lol
    tense_free = ('PARTICIPLE', 'INFINITIVE', 'IMPERATIVE')


    if tense not in tense_types:
        print('tense not available')
        return None

    if question_type not in question_types:
        print('question type not available')
        return None

    if chart is None:
        chart_found = False
        chart_backup = []

        for conjugation in range(0, len(total_conjugations)):
            temp_chart_found = True
            chart_count = 0

            for specific_conjugation in range(0, len(total_conjugations[conjugation])):
                if latin_words[specific_conjugation].endswith(total_conjugations[conjugation][specific_conjugation]):
                    chart_count += 1
                elif not latin_words[specific_conjugation].endswith(total_conjugations[conjugation][specific_conjugation]):
                    temp_chart_found = False
            
            if temp_chart_found == True:
                chart = conjugation_names[conjugation]
                chart_found = True

            chart_backup.append(chart_count)
        
        if chart_found == False:
            chart = conjugation_names[chart_backup.index(max(chart_backup))] #this is a fallback in case it cant find the chart regularly

    #VB - Verb, Base Form
    #VBD - Verb, Past Tense
    #VBG - Verb, Gerund or Present Participle
    #VBN - Verb, Past Participle
    #VBZ - Verb, 3rd Person Singular Present

    english_words = {"VB": english_word, 
                     "VBG" : pyinflect.getInflection(english_word, 'VBG')[0],
                     "VBN" : pyinflect.getInflection(english_word, 'VBN')[0],
                     "VBZ" : pyinflect.getInflection(english_word, 'VBZ')[0],
                     "VBD" : pyinflect.getInflection(english_word, 'VBD')[0]}

    english_dictionary = json.load(open(tense))
    latin_dictionary = json.load(open(f'.{subdirectory}data{subdirectory}latin-conjugation-charts{subdirectory}{chart}.json'))

    questions = json.load(open(question_type))
    output = {}

    tense = tense.replace('.json', '')
    tense = tense.split(subdirectory)
    tense = str(tense[len(tense) - 1])

    #LATIN CREATION
    for question_type in questions:
        output[question_type] = {}

        for activeness in questions[question_type]:
            output[question_type][activeness] = {}
            
            for question in questions[question_type][activeness]:
                output[question_type][activeness][question] = {}

                data_theme = blocks.index(questions[question_type][activeness][question])
                word = latin_words[data_theme]

                word_ending = conjugation_chart_key[chart][data_theme]
                new_ending = latin_dictionary[question_type][activeness][question]

                if question_type not in tense_free:
                    new_ending = new_ending[tense]
                                
                endless_word = re.sub(f'{strip_accents(word_ending)}$', '', strip_accents(word))

                if new_ending == "" and endless_word not in ignore_words:
                    new_ending = word_ending[0]
                
                answer = re.sub(f'{strip_accents(word_ending)}$', new_ending, strip_accents(word))
                output[question_type][activeness][question]['latin'] = answer
    

    #ENGLISH CREATION
    for question_type in english_dictionary:
        for activeness in english_dictionary[question_type]:
            for question in english_dictionary[question_type][activeness]:
                
                answer = english_dictionary[question_type][activeness]

                if question_type != "IMPERATIVE": #imperative english doesnt have choice about singular, plural, etc
                    answer = answer[question]
                
                for new_word in english_words:
                    answer = answer.replace(f'*{new_word}*', english_words[new_word])
                
                if question_type != "IMPERATIVE":
                    output[question_type][activeness][question]['english'] = answer
                else:
                    output[question_type][activeness]['english'] = answer


    #OUTPUT
    if not os.path.exists(f'.{subdirectory}output{subdirectory}'):
        os.mkdir(f'.{subdirectory}output{subdirectory}')

    with open(f'.{subdirectory}output{subdirectory}{english_word}-output.json', mode='w', encoding='utf-8') as file:
        save_file(file, output)

    print('success')


#for use outside of python, (in terminal)
for help_command in help_commands:
    if help_command in (sys.argv):
        filename = str(__file__).split(subdirectory)
        filename = filename[len(filename) - 1]

        print(f'Example: python3 {filename} "english word" "latin words" "tense" "question type" "chart"\n\nenglish word: singular\nlatin words: 4 latin words split by space \ntense: [1st singular, 1st plural, 2nd singular, 2nd plural, 3rd singular, 3rd plural]\nquestion type: OPTIONAL you can set custom question type usage (defaults to "default"), add more to .{subdirectory}data{subdirectory}question-types{subdirectory}\nchart: OPTIONAL it will already solve for the chart by itself, so not really needed, just an option\n\n!DONT FORGET THE QUATATION MARKS!')

if len(sys.argv) == 4:
    generate_synopsis(str(sys.argv[1]), str(sys.argv[3]), list(str(sys.argv[2]).split(' ')))
elif len(sys.argv) == 5:
    generate_synopsis(str(sys.argv[1]), str(sys.argv[3]), list(str(sys.argv[2]).split(' ')), question_type=str(sys.argv[4]))
elif len(sys.argv) == 6:
    generate_synopsis(str(sys.argv[1]), str(sys.argv[3]), list(str(sys.argv[2]).split(' ')), str(sys.argv[5]), str(sys.argv[4]))