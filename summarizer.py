from groq import Groq
import dotenv
import os

class Summarizer:
    def __init__(self, env_file="key.env", model=None):
        """
        Initializes the Summarizer class with a specific model and configures the Groq API client.

        Args:
            env_file (str): The env file containing the API keys. Default: "key.env".
            model (str): The model to use for summarization.
        Attributes:
            model (str): The specified model for Groq.
            client (Groq): Instance of the Groq client for API requests.
        """
        dotenv.load_dotenv(env_file, override=True)
        self.model = os.getenv("GROQ_MODEL_NAME")
        self.client = Groq()
        
        if model:
            self.model = model
        

    def summarize(self, text, max_tokens=1024, temperature=0.5, stop=None):
        """
        Generates a summary of the given text using the Groq API.

        Args:
            text (str): The text to summarize.
            max_tokens (int): The maximum number of tokens for the completion. Default: 1024.
            temperature (float): Controls randomness. Default: 0.5.
            stop (str or None): Optional sequence indicating where the model should stop. Default: None.

        Returns:
            str: The summary generated by the model.
        """
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "you are a summarizer"},
                    {"role": "user", "content": text}
                ],
                model=self.model,
                temperature=temperature,
                max_completion_tokens=max_tokens,
                stop=stop
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating summary: {e}")
            return None

    def summarize_texts(self, texts, max_tokens=1024, temperature=0.5, stop=None):
        """
        Generates summaries for a list of texts.

        Args:
            texts (list): List of strings to summarize.
            max_tokens (int): Maximum number of tokens for each completion. Default: 1024.
            temperature (float): Controls randomness. Default: 0.5.
            stop (str or None): Optional sequence indicating where the model should stop. Default: None.

        Returns:
            list: A list of generated summaries.
        """
        summaries = []

        for index, text in enumerate(texts):
            print(f"Summarizing text {index + 1}/{len(texts)}...")
            summary = self.summarize(text, max_tokens=max_tokens, temperature=temperature, stop=stop)

            if summary:
                summaries.append(summary)
                print(f"Text {index + 1} summarized successfully.")
            else:
                print(f"Error summarizing text {index + 1}.")

        return summaries
