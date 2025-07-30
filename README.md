# CC-CEDICT Parser

A Python script to parse CC-CEDICT dictionary files and convert them to JSON format.

## What is CC-CEDICT?

CC-CEDICT is a Chinese-English dictionary that contains traditional and simplified Chinese characters, pinyin romanization, and English definitions. The format follows this pattern:

```
traditional simplified [pinyin] /meaning1/meaning2/.../
```

## Features

- Parses CC-CEDICT format files
- Extracts traditional and simplified characters
- Extracts pinyin romanization from traditional Chinese characters
- Extracts zhuyin (bopomofo) from traditional Chinese characters
- Extracts English meanings
- Identifies idioms based on "(idiom)" marker in meanings
- Outputs clean JSON format
- Handles UTF-8 encoding
- Robust error handling

## Usage

```bash
python main.py input_dict_path output_path
```

### Arguments

- `input_dict_path`: Path to the input CC-CEDICT file
- `output_path`: Path to the output JSON file

### Examples

```bash
# Parse a CC-CEDICT file and save to JSON
python main.py cedict_ts.u8 output.json

# Parse with full paths
python main.py /path/to/cedict.txt /path/to/output.json
```

## Output Format

The script generates a JSON file containing an array of objects with the following structure:

```json
[
  {
    "traditional": "繁體字",
    "simplified": "简体字", 
    "pinyin": "jiǎn tǐ zì",
    "zhuyin": "ㄐㄧㄢˇ ㄊㄧˇ ㄗˋ",
    "meaning": ["simplified character", "simplified characters"],
    "is_idiom": false
  },
  {
    "traditional": "成語",
    "simplified": "成语",
    "pinyin": "chéng yǔ", 
    "zhuyin": "ㄔㄥˊ ㄩˇ",
    "meaning": ["idiom", "proverb", "set phrase"],
    "is_idiom": true
  }
]
```

### Field Descriptions

- `traditional`: Traditional Chinese characters
- `simplified`: Simplified Chinese characters  
- `pinyin`: Pinyin romanization (with tone marks) derived from traditional characters
- `zhuyin`: Zhuyin (bopomofo) phonetic notation derived from traditional characters
- `meaning`: Array of English definitions
- `is_idiom`: Boolean indicating if the entry is an idiom (based on "(idiom)" marker in meanings)

## Requirements

- Python 3.6+
- pypinyin library (for zhuyin conversion)

## Installation

```bash
pip install -r requirements.txt
```

## Error Handling

The script includes robust error handling:
- Validates input file existence
- Creates output directories if needed
- Skips malformed lines with warnings
- Handles encoding issues gracefully
- Provides clear error messages

## License

This project is open source and available under the MIT License.
