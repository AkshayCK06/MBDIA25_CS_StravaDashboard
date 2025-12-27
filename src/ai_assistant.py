"""
Strava AI Assistant (Ollama Powered)
====================================

This module connects to a local Ollama instance to provide intelligent
insights about Strava data using the 'mistral-nemo:latest' model.

It prioritizes privacy by keeping all data on the local machine.
"""

import requests
import json
import pandas as pd
from datetime import datetime

class AIAssistant:
    def __init__(self, df, model="mistral-nemo:latest"):
        """
        Initialize the AI with the athlete's activity data.
        
        Args:
            df (pd.DataFrame): The dataframe containing activity data.
            model (str): The name of the local Ollama model to use.
        """
        self.df = df
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"
        self._context_cache = None

    def _build_context(self):
        """Creates a data summary to feed into the LLM."""
        if self._context_cache:
            return self._context_cache

        # Basic Stats
        total_dist = self.df['distance'].sum() / 1000
        total_activities = len(self.df)
        total_elev = self.df['total_elevation_gain'].sum()
        
        # Recent Activity
        if 'start_date_local' in self.df.columns:
            recent = self.df.sort_values('start_date_local', ascending=False).iloc[0]
            last_date = pd.to_datetime(recent['start_date_local']).strftime("%Y-%m-%d")
            last_type = recent['type']
            last_dist = recent['distance'] / 1000
        else:
            last_date = "Unknown"
            last_type = "Unknown"
            last_dist = 0

        # Activity Types
        types = self.df['type'].value_counts().to_dict()

        # Records
        max_dist = self.df['distance'].max() / 1000
        
        context = (
            f"You are a helpful, encouraging fitness coach and data analyst. "
            f"Here is the athlete's data summary:\n"
            f"- Total Activities: {total_activities}\n"
            f"- Total Distance: {total_dist:.1f} km\n"
            f"- Total Elevation Gain: {total_elev:.0f} m\n"
            f"- Activity Types: {types}\n"
            f"- Last Activity: {last_date} ({last_type}, {last_dist:.1f} km)\n"
            f"- Longest Single Activity: {max_dist:.1f} km\n"
            f"Current Date: {datetime.now().strftime('%Y-%m-%d')}\n"
            f"Answer the user's question based on this data. Keep answers concise and motivating."
        )
        
        self._context_cache = context
        return context

    def ask(self, question):
        """
        Sends the question + context to the local Ollama API.
        Returns the generated text.
        """
        context = self._build_context()
        prompt = f"{context}\n\nUser Question: {question}\nAnswer:"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            return response.json()['response']
        except requests.exceptions.ConnectionError:
            return "⚠️ Error: Could not connect to Ollama. Is it running? (Run `ollama serve` in a terminal)."
        except Exception as e:
            return f"⚠️ Error generating response: {e}"

