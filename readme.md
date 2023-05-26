# Synopsis Generator

This script is designed to generates synopses for English and Latin words. It takes an English word, a list of Latin words, a tense, and an optional question type and chart as input and produces an output file containing the conjugation synopses.

## Prerequisites

- Python 3.x

## Installation

1. Clone the repository or download the script file.

2. Install the required dependencies by running the following command:

    ```shell
    pip3 install -r requirements.txt
    ```

    OR

    ```shell
    pip install -r requirements.txt
    ```
3. Place the necessary data files in the appropriate directories:
   * Place question type files within the `data/question-types` subdirectory. (you can create new ones by copying the default json file and modifying it, it will recognize it automatically and can be used as soon as the file is added to the subdirectory)

## Usage
Run the script with the following command:

```shell
python3 conjugation_synopsis.py "english word" "latin words" "tense" "question type" "chart"
```

OR

```shell
python3
from synopsis_generator import *
generate_synopsis(english_word, tense, latin_words, chart = None,  question_type = 'default')
```

* `english word`: The singular form of the English word.

* `latin words`: Four Latin words separated by spaces.

* `tense`: The tense to generate conjugation synopses for. Use the following  format: [1st singular, 1st plural, 2nd singular, 2nd plural, 3rd singular, 3rd plural].

* `question type (optional)`: The type of question to generate. If not provided, the default question type will be used. Additional question types can be added to the data/question-types directory.

* `chart (optional)`: The specific conjugation chart to use. If not provided, the script will automatically determine the appropriate chart based on the given Latin words.

<b>Note</b>: Ensure that you enclose the arguments in quotation marks.

## Examples
* Generate conjugation synopses for the word "free" in the 1st singular with Latin words "līberō līberāre līberāvī līberātus":
```shell
python3 synopsis_generator.py "free" "līberō līberāre līberāvī līberātus" "1st singular"
```

* Generate conjugation synopses with a custom question type:
```shell
python3 synopsis_generator.py "free" "līberō līberāre līberāvī līberātus" "1st singular" "custom question chart" 
```

* Generate conjugation synopses with a specific chart:
```shell
python3 synopsis_generator.py "free" "līberō līberāre līberāvī līberātus" "1st singular" "default" "chart type"
```

## Help
To display the help message, use one of the following commands:

```shell
python3 conjugation_synopsis.py -h
python3 conjugation_synopsis.py --h
python3 conjugation_synopsis.py -help
python3 conjugation_synopsis.py --help
```

The help message provides information on the command usage and arguments.

<b>Note:</b> The script assumes a Unix-like operating system by default. If you're using a different operating system, modify the `subdirectory `variable in the script accordingly.