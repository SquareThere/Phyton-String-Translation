from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import os
import html

# Set the path to your service account key file
key_path = r'C:\Users\user.MEW\Documents\1\key.json'  # Replace with the actual path to your key file

# Define the language you want to translate to (Swedish)
target_language = 'sv'  # Change to 'sv' for Swedish

# Function to translate a text
def translate_text(text):
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = translate.Client(credentials=credentials)
    translation = client.translate(text, target_language=target_language)
    translated_text = translation['translatedText']
    decoded_translated_text = html.unescape(translated_text)  # Decode HTML entities
    return translation['input'], decoded_translated_text

# Directory where your translation files are located
translation_dir = r'C:\Users\user.MEW\Downloads\trl'

# Prompt the user for the directory to save translated files
output_dir = r'C:\Users\user.MEW\Documents\1'

for filename in os.listdir(translation_dir):
    if filename.endswith('.php'):
        with open(os.path.join(translation_dir, filename), 'r') as file:
            data = file.read()

        # Split the data into lines and process each line
        lines = data.split('\n')
        for i, line in enumerate(lines):
            if "=>" in line:
                parts = line.split("=>")
                key = parts[0].strip()
                value = parts[1].strip()
                if key and value:
                    original_value, translated_value = translate_text(value)
                    print(f"Original Value: {original_value}")
                    print(f"Translated Value: {translated_value}")
                    lines[i] = f"{key} => '{translated_value}',"

        # Join the lines back together
        data = '\n'.join(lines)

        # Save the translated file in the specified output directory
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w') as file:
            file.write(data)

print('Translations updated and saved successfully.')
