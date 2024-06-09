import openai
import os
import zipfile
import json

# Set up OpenAI API key
openai.api_key = ''

def get_user_input():
    user_input = input("What application do you want to build/generate? ")
    return user_input

def generate_file_structure(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Generate a file structure for the application."},
            {"role": "user", "content": prompt}
        ]
    )
    file_structure = response['choices'][0]['message']['content']
    return json.loads(file_structure)

def generate_file_contents(file_structure, prompt):
    file_contents = {}
    for filepath, description in file_structure.items():
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Generate the content for the file: {filepath} based on the following requirements: {prompt}"},
                {"role": "user", "content": description}
            ]
        )
        file_contents[filepath] = response['choices'][0]['message']['content']
    return file_contents

def create_files(file_contents):
    for filepath, content in file_contents.items():
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as file:
            file.write(content)

def zip_files(file_contents, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for filepath in file_contents.keys():
            zipf.write(filepath)

def main():
    prompt = get_user_input()
    file_structure = generate_file_structure(prompt)
    
    if len(file_structure) > 20:
        print("The generated file structure exceeds the maximum limit of 20 files.")
        return

    file_contents = generate_file_contents(file_structure, prompt)
    create_files(file_contents)
    zip_filename = "generated_application.zip"
    zip_files(file_contents, zip_filename)
    print(f"Generated application has been zipped into {zip_filename}")

if __name__ == "__main__":
    main()
