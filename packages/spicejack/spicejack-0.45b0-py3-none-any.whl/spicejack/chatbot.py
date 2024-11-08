"""
Basic implementation of a chatbot with history.

Copyright (C) 2024 LIZARD-OFFICIAL-77

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import openai
import g4f
import os


from dotenv import load_dotenv;load_dotenv()


class APIKeyError(Exception):pass
class MessageOrderError(Exception):pass
class InstructionError(Exception):pass

class BaseChatbot:
    def __init__(self,model):"""Should set the model and initialize history."""
    def instructions(self,instruction):"""Should add instructions to the history, raising InstructionError if an instruction already exists, or MessageOrderError if conversation has already started"""
    def message(self,content):"""Should add the message with the role "user" to the history, save the result in a variable, add it to the history and return it."""
    
class G4FChatbot(BaseChatbot):
    def __init__(self,model):
        """Free LLM using gpt4free by xtekky

        Args:
            model (g4f.models.Model): AI model to use for conversion from text to json.
        """
        self.model = model
        self.history = []
    def instructions(self,content):
        """Give the chatbot instructions.

        Args:
            content (str): Instructions. e.g. You are a mathematician.

        Raises:
            InstructionError: Raises when called twice on the same object.
            MessageOrderError: Raises when called after the conversation is already started.
        """
        if len(self.history) > 0:
            if self.history[0]["role"] == "system":
                raise InstructionError("Instructions already exist for this Chatbot object.")
            else:
                raise MessageOrderError("Conversation already started.")
        self.history.append({"role":"system","content":content})
    def message(self,content):
        self.history.append({"role":"user","content":content})
        assistant = g4f.ChatCompletion.create(self.model,self.history)
        self.history.append({"role":"assistant","content":assistant})
        return assistant


class OpenAIChatbot(BaseChatbot):
    def __init__(self,model):
        """Paid chatbot using OpenAI. Not recommended for small projects, use for important projects where speed is important.

        Args:
            model : AI model to use for conversion from text to json.
        """
        
        try:
            os.environ["OPENAI_API_KEY"]
        except:
            raise APIKeyError("Please create a file named \".env\" and type OPENAI_API_KEY = \"YOUR API KEY\"")
        
        self.client = openai.Client()
        self.model = model
        self.history = []
    def instructions(self,content):
        """Give the chatbot instructions.

        Args:
            content (str): Instructions. e.g. You are a mathematician.

        Raises:
            InstructionError: Raises when called twice on the same object.
            MessageOrderError: Raises when called after the conversation is already started.
        """
        if len(self.history) > 0:
            if self.history[0]["role"] == "system":
                raise InstructionError("Instructions already exist for this Chatbot object.")
            else:
                raise MessageOrderError("Conversation already started.")
        self.history.append({"role":"system","content":content})
    def message(self,content):
        """_summary_

        Args:
            content (str): Input to LLM

        Returns:
            str: response from LLM
        """
        self.history.append({"role":"user","content":content})
        assistant = self.client.chat.completions.create(messages=self.history,model=self.model)
        self.history.append({"role":"assistant","content":assistant})
        return assistant
