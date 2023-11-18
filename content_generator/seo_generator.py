from openai import OpenAI

from dotenv import dotenv_values

# Load environment variables from the .env file
env_variables = dotenv_values('.env')

# Access the variables
api_key = env_variables['OPENAI_API_KEY']

client = OpenAI(
   api_key=api_key
)


completion = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
]
)

print(completion.choices[0].message)