import openai
import yaml
import requests


# OpenAI API key
openai.api_key = "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"




def input_type():
    #select local file path or Git URL
    choice = input("Choose how to provide source code (1: local file, 2: Git URL): ")
    if choice not in ('1', '2'):
        print("Invalid choice. Please enter 1 or 2.")
        return input_type()
    return choice

def read_code(choice):
    
    if choice == '1':
        file_path = input("Enter the path to your local Python code file: ")

        #used for testing path(optional)
        #file_path = "C:\\Users\\HP\\Desktop\\openapi\\Code_summrization\\test.py"

        try:
            with open(file_path, 'r') as f:
                code = f.read()
            return code
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return read_code(choice)
    else:
        url = input("Enter the Git repository URL: ")
        #used for testing pat
        #url = "https://github.com/psf/requests"
        
        response = requests.get(url+ "/archive/master.zip")  
        if response.status_code == 200:
            print("Warning")
            return None  
        else:
            print(f"Error retrieving code: {response.status_code}")
            return read_code(choice)

def summarizer(code):
   
    prompt = f"Provide a concise summary of the following Python code:\n{code}"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    summary = response.choices[0].text.strip()
    return summary

if __name__ == "__main__":
    choice = input_type()
    code = read_code(choice)
    if code:  
        summary = summarizer(code)
        print("Summary of the code:")
        print(summary)
    else:
        print("Error: Could not retrieve code.")

