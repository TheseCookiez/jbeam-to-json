'''
Inspired by OliverF's C# Jbeam-to-Json original code' ["https://gist.github.com/OliverF"]

Python3 implementation for converting BeamNG .JBEAM to .JSON

Also, feel free to use the JBeamToJSON method in your own code for further automating of modding
'''
import regex as re
import argparse

def JBeamToJSON(jbeamtext):
    jbeamtext = re.sub(r'//.*\r?\n', '', jbeamtext)

    # Remove C-style code comments
    jbeamtext = re.sub(r'/\*[^\*]*\*/', '', jbeamtext)

    # Replace any letter or number, or closing array (]) or dictionary (}), 
    # with 0 or more spaces between it (\s*?) and the newline (\n\r) with ITSELF, plus a comma, plus a newline
    jbeamtext = re.sub(r'[a-zA-Z0-9\]\}]\s*?\r?\n', lambda match: match.group(0)[0] + ",\n", jbeamtext)

    # This fixes the case where we have 2 numbers next to each other { ([0-9])[\s]+([\-0-9]) } outside of a quote { (""[^""]*?""|\Z) } and separated by AT LEAST ONE SPACE { [\s]+ }
    jbeamtext = re.sub(r'((?:[^"]*?([0-9])[\s]+([\-0-9])[^"]*?)*)(""[^"]*?""|\Z)', 
                       lambda match: re.sub(r'([0-9])[\s]+([\-0-9])', r'\1,\2',
                                            re.sub(r'([0-9])[\s]+([\-0-9])', r'\1,\2', match.group(1))) + match.group(4), jbeamtext)

    # Fix ,] and ,}
    jbeamtext = re.sub(r',[\s\r\n]*?\]', ']', jbeamtext)
    jbeamtext = re.sub(r',[\s\r\n]*?\}', '}', jbeamtext)

    # Lazy hack, remove the trailing comma after the last brace if there is one
    jbeamtext = re.sub(r',[\r\n\s]*\Z', '', jbeamtext)

    # Fix errors made by the authors...
    # These fix the errors where the author did something silly like }"
    jbeamtext = re.sub(r'\}[\r\n\s]*?"', '},\"', jbeamtext)
    jbeamtext = re.sub(r'\][\r\n\s]*?"', '],\"', jbeamtext)

    # This fixes the errors where we have something like "foo" "bar" in an array, where it should be "foo", "bar"
    jbeamtext = re.sub(r'((?<!\s*:\s*)"")[\s]*"', r'\1,\"', jbeamtext)
    # Add missing trailing commas
    jbeamtext = re.sub(r'("[^"]+":\s*"[^"]+")(\s*\n)', r'\1,\2', jbeamtext)
    # Fix places where tariling comma is added when one already exists
    jbeamtext = re.sub(r',+', ',', jbeamtext )

    return jbeamtext

def main():
    parser = argparse.ArgumentParser(description='Parser for converting BeamNG .jbeam files to valid .json')
    parser.add_argument('-s','--source', help='Source .jbeam file', required=True)
    parser.add_argument('-o','--output', help='output name .json', required=True)
    args = parser.parse_args()

    # Read the contents of the source file
    source_file_path = args.source
    with open(source_file_path, 'r') as file:
        jbeam_text = file.read()

    # Convert JBeam to JSON
    json_text = JBeamToJSON(jbeam_text)

    # Save the JSON to output file
    output_file_path = args.output
    with open(output_file_path, 'w') as file:
        file.write(json_text)

    print(f"Conversion completed. Input {args.source} parsed successfully and saved to {args.output}")

if __name__ == "__main__":
    main()

