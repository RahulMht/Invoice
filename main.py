from dotenv import load_dotenv
load_dotenv()
import ast
import os
import PIL.Image
from time import sleep
import google.generativeai as genai
import pandas as pd


genai.configure(api_key=os.environ.get("google_api_key"))

model = genai.GenerativeModel('gemini-pro-vision')

# Create an empty DataFrame to store the results
columns = ["पूरा नाम", "लिंग", "उमेर", "जन्ममिति", "वैवाहिक स्थिति", "ठेगाना", "वडा नं.", "अभिभावकको नाम", "व्यवसाय", "रक्त समूह", "EMAIL ADDRESS"]
df = pd.DataFrame(columns=columns)

# Path to the dataset folder containing images
dataset_folder = "dataset"

# get the path/directory
folder_dir = r"dataset"
a = []
for images in os.listdir(folder_dir):
    # check if the image ends with jpg
    if (images.endswith(".jpg")):
      path ="dataset/" + str(images)
      img = PIL.Image.open(path)
      response = model.generate_content(['You are a professional Nepali government officer , your task is to OCR the document and change into key value pair , where the Keys are "पूरा नाम", "लिंग", "उमेर", "जन्ममिति", "वैवाहिक स्थिति", "ठेगाना", "वडा नं.", "अभिभावकको नाम", "व्यवसाय", "रक्त समूह", "EMAIL ADDRESS" only , like this : {"पूरा नाम": answer, "लिंग": answer, "उमेर": answer, "जन्ममिति": answer, "वैवाहिक स्थिति": answer, "ठेगाना": answer, "वडा नं.": answer, "अभिभावकको नाम": answer, "व्यवसाय": answer, "रक्त समूह": answer, "EMAIL ADDRESS": answer} Write the only {....} dont write other unnecessary things ', img], stream=False,generation_config=genai.types.GenerationConfig(temperature=0.1))
      response.resolve()
      start_index = response.text.find("{")
      end_index = response.text.rfind("}")

      # Check if both "{" and "}" are present in the string
      if start_index != 0 or end_index != -1:
          # Extract the content between "{" and "}"
          result_string = response.text[start_index: end_index +1].strip()
      dictionary = ast.literal_eval(result_string)
      # Append dictionary as a new row to the DataFrame
      dictionary = ast.literal_eval(result_string)
      a.append(dictionary)
    #   sleep(0.5)
df = pd.DataFrame(a)  

print(df)

df.to_csv('output.csv', index=False)