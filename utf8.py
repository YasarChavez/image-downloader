def remove_non_utf8(input_file, output_file):
    with open(input_file, 'rb') as file:
        content = file.read()
    
    # Decode the content, ignoring errors
    decoded_content = content.decode('utf-8', errors='ignore')
    
    # Encode back to UTF-8
    cleaned_content = decoded_content.encode('utf-8')
    
    with open(output_file, 'wb') as file:
        file.write(cleaned_content)

# Usage
input_file = 'run.py'  # Replace with your input file name
output_file = 'run.py'  # Replace with your desired output file name

remove_non_utf8(input_file, output_file)
print(f"Cleaned content saved to {output_file}")
