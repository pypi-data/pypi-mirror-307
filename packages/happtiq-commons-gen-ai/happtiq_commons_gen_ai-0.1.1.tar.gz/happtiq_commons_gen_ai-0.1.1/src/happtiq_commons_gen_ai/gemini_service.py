import logging
import vertexai
from vertexai.generative_models import GenerativeModel, Part

class GeminiService:
    def __init__(self, project_id: str, location: str, model_id: str):
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel(model_name=model_id)
        self.logger = logging.getLogger(__name__)
    
    def send_single_data_prompt_to_api(self, prompt: str, data_file_gcs_uri: str, mime_type: str) -> str:
        return self.send_data_prompt_to_api([prompt], [data_file_gcs_uri], [mime_type])
    
    def send_data_prompt_to_api(self, prompts: list, data_file_gcs_uris: list, mime_types: list) -> str:
        self.logger.info(f"Sending prompts to vertex ai:\n {prompts} with {len(data_file_gcs_uris)} files")

        # Create Part objects for each data file with the corresponding MIME type
        data_files = [Part.from_uri(uri, mime_type=mime_type) for uri, mime_type in zip(data_file_gcs_uris, mime_types)]
        contents = data_files + prompts

        response = self.model.generate_content(contents)
        return response.text
    
    def send_prompt_to_api(self, prompt: str) -> str:
        self.logger.info(f"Sending prompt to vertex ai:\n {prompt}")
    
        try:
            response = self.model.generate_content(prompt)
            reply_text = response.text
            
            return reply_text
        except Exception as e:
            self.logger.error(f"Error occurred while generating from gemini: {e}")
            raise
        
