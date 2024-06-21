import requests
import json
import base64
from models import ObservableFeatures

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def analyze_image(image_path: str) -> ObservableFeatures:
    try:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        payload = {
            "model": "llava:34b",
            "prompt": "Analyze this image and provide the following details about the animal: species, breed, size, coat length, and coat color. Format the response as a JSON object.",
            "images": [image_data]
        }
        
        print("Sending request to Ollama API...")
        response = requests.post(OLLAMA_API_URL, json=payload)
        
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        print("\nAPI Response Content (raw):")
        print(response.text)
        
        if response.status_code == 200:
            full_response = response.text
            json_objects = [json.loads(line) for line in full_response.split('\n') if line.strip()]
            
            # Combine all response fragments
            combined_response = ''.join(obj['response'] for obj in json_objects if 'response' in obj)
            
            print("\nCombined Response:")
            print(combined_response)
            
            # Extract JSON object
            json_start = combined_response.find('{')
            json_end = combined_response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = combined_response[json_start:json_end]
                print("\nExtracted JSON:")
                print(json_str)
                
                features_dict = json.loads(json_str)
                features = ObservableFeatures(
                    species=features_dict.get('species'),
                    breed=features_dict.get('breed'),
                    size=features_dict.get('size'),
                    coat_length=features_dict.get('coat length') or features_dict.get('coat_length'),
                    coat_color=features_dict.get('coat color') or features_dict.get('coat_color')
                )
                
                # Normalize species
                if features.species and features.species.lower() == 'canine':
                    features.species = 'Dog'
                elif features.species and features.species.lower() == 'feline':
                    features.species = 'Cat'
                
                print("\nExtracted features:")
                print(f"Species: {features.species}")
                print(f"Breed: {features.breed}")
                print(f"Size: {features.size}")
                print(f"Coat Length: {features.coat_length}")
                print(f"Coat Color: {features.coat_color}")
                
                return features
            else:
                print("No JSON object found in the response")
                return None
        else:
            print(f"API request failed with status code: {response.status_code}")
            print(f"Error message: {response.text}")
            return None
    
    except Exception as e:
        print(f"An error occurred during image analysis: {str(e)}")
        return None