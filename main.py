#!/usr/bin/env python3
"""
CC-CEDICT Parser

This script parses CC-CEDICT dictionary files and converts them to JSON format.
CC-CEDICT format: traditional simplified [pinyin] /meaning1/meaning2/.../

Usage:
    python main.py input_dict_path output_path
"""

import json
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from pypinyin import pinyin, Style
except ImportError:
    print("Error: pypinyin library is required. Install it with: pip install pypinyin")
    sys.exit(1)


def get_zhuyin_from_characters(characters: str) -> str:
    """
    Get zhuyin (bopomofo) directly from Chinese characters using pypinyin.
    
    Args:
        characters: Chinese characters (traditional or simplified)
        
    Returns:
        Zhuyin text
    """
    if not characters:
        return ""
    
    # Convert Chinese characters directly to zhuyin using pypinyin
    # Style.BOPOMOFO gives us zhuyin characters
    zhuyin_list = pinyin(characters, style=Style.BOPOMOFO)
    
    # Join the zhuyin characters with spaces
    zhuyin_text = " ".join([item[0] for item in zhuyin_list if item[0]])
    
    return zhuyin_text


def get_pinyin_from_characters(characters: str) -> str:
    """
    Get pinyin directly from Chinese characters using pypinyin.
    
    Args:
        characters: Chinese characters (traditional or simplified)
        
    Returns:
        Pinyin text with tone marks
    """
    if not characters:
        return ""
    
    # Convert Chinese characters directly to pinyin using pypinyin
    # Style.TONE gives us pinyin with tone marks
    pinyin_list = pinyin(characters, style=Style.TONE)
    
    # Join the pinyin characters with spaces
    pinyin_text = " ".join([item[0] for item in pinyin_list if item[0]])
    
    return pinyin_text


def parse_cc_cedict_line(line: str) -> Dict[str, any]:
    """
    Parse a single CC-CEDICT line and return a dictionary with the parsed data.
    
    CC-CEDICT format: traditional simplified [pinyin] /meaning1/meaning2/.../
    
    Args:
        line: A single line from the CC-CEDICT file
        
    Returns:
        Dictionary with keys: traditional, simplified, pinyin, meaning, is_idiom
    """
    # Skip empty lines and comments
    if not line.strip() or line.startswith('#'):
        return None
    
    # Remove trailing whitespace and newlines
    line = line.strip()
    
    # Split by the first space to get traditional and simplified characters
    # The format is: traditional simplified [pinyin] /meaning1/meaning2/.../
    parts = line.split(' ', 2)
    if len(parts) < 3:
        return None
    
    traditional = parts[0]
    simplified = parts[1]
    rest = parts[2]
    
    # Get pinyin directly from traditional Chinese characters using pypinyin
    pinyin = get_pinyin_from_characters(traditional)
    
    # Extract meanings by removing pinyin section and getting the part in slashes
    # The format is: [pinyin] /meaning1/meaning2/.../
    # Remove the pinyin section (enclosed in square brackets)
    meaning_part = re.sub(r'\[.*?\]', '', rest).strip()
    
    # Extract meanings (enclosed in forward slashes)
    meanings = []
    if meaning_part.startswith('/') and meaning_part.endswith('/'):
        # Remove leading and trailing slashes
        meaning_text = meaning_part[1:-1]
        # Split by '/' to get individual meanings
        meanings = [meaning.strip() for meaning in meaning_text.split('/') if meaning.strip()]
    
    # Determine if it's an idiom (typically 4 characters or more in traditional/simplified)
    is_idiom = len(traditional) >= 4 or len(simplified) >= 4
    
    # Get zhuyin directly from traditional Chinese characters
    zhuyin = get_zhuyin_from_characters(traditional)
    
    return {
        "traditional": traditional,
        "simplified": simplified,
        "pinyin": pinyin,
        "zhuyin": zhuyin,
        "meaning": meanings,
        "is_idiom": is_idiom
    }


def parse_cc_cedict_file(input_path: str) -> List[Dict[str, any]]:
    """
    Parse the entire CC-CEDICT file and return a list of dictionaries.
    
    Args:
        input_path: Path to the CC-CEDICT file
        
    Returns:
        List of dictionaries containing parsed entries
    """
    entries = []
    
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                try:
                    parsed_entry = parse_cc_cedict_line(line)
                    if parsed_entry:
                        entries.append(parsed_entry)
                except Exception as e:
                    print(f"Warning: Error parsing line {line_num}: {e}")
                    continue
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    return entries


def save_to_json(entries: List[Dict[str, any]], output_path: str):
    """
    Save the parsed entries to a JSON file.
    
    Args:
        entries: List of dictionaries containing parsed entries
        output_path: Path to the output JSON file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(entries, file, ensure_ascii=False, indent=2)
        print(f"Successfully saved {len(entries)} entries to '{output_path}'")
    except Exception as e:
        print(f"Error writing to output file: {e}")
        sys.exit(1)


def main():
    """Main function to handle command line arguments and execute the parser."""
    parser = argparse.ArgumentParser(
        description="Parse CC-CEDICT dictionary files and convert to JSON format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py cedict_ts.u8 output.json
  python main.py /path/to/cedict.txt /path/to/output.json
        """
    )
    
    parser.add_argument(
        'input_dict_path',
        help='Path to the input CC-CEDICT file'
    )
    
    parser.add_argument(
        'output_path',
        help='Path to the output JSON file'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not Path(args.input_dict_path).exists():
        print(f"Error: Input file '{args.input_dict_path}' does not exist.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    output_dir = Path(args.output_path).parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Parsing CC-CEDICT file: {args.input_dict_path}")
    
    # Parse the file
    entries = parse_cc_cedict_file(args.input_dict_path)
    
    if not entries:
        print("Warning: No valid entries found in the input file.")
        sys.exit(1)
    
    print(f"Found {len(entries)} entries")
    
    # Save to JSON
    save_to_json(entries, args.output_path)


if __name__ == "__main__":
    main()
