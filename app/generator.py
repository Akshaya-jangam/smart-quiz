import json
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models.tfidf_retriever import TFIDFRetriever
from .models.template_generator import TemplateGenerator
from .schemas import QuizResponse

class QuizGenerator:
    def __init__(self, config):
        self.config = config
        self.question_bank = self._load_question_bank()
        self.tfidf_retriever = TFIDFRetriever(self.question_bank)
        self.template_generator = TemplateGenerator()
        
    def _load_question_bank(self):
        try:
            with open('data/question_bank.json', 'r', encoding='utf-8') as f:
                questions = json.load(f)
                return [q for q in questions if self._validate_question(q)]
        except Exception as e:
            print(f"Error loading question bank: {str(e)}")
            return []
    
    def _validate_question(self, question):
        required = ['type', 'question', 'answer', 'difficulty', 'goal']
        return all(field in question for field in required)
    
    def generate_quiz(self, quiz_request):
        questions = []
        
        # Retrieval-based questions
        retrieval_count = int(quiz_request.num_questions * self.config["retrieval_weight"])
        retrieved = self.tfidf_retriever.retrieve_questions(
            quiz_request.goal, 
            retrieval_count,
            quiz_request.difficulty
        )
        questions.extend(retrieved)
        
        # Template-based questions
        template_count = int(quiz_request.num_questions * self.config["template_weight"])
        templated = self.template_generator.generate_questions(
            quiz_request.goal,
            template_count,
            quiz_request.difficulty
        )
        questions.extend(templated)
        
        # Fill remaining with random questions
        remaining = quiz_request.num_questions - len(questions)
        if remaining > 0:
            filtered = [
                q for q in self.question_bank 
                if q["goal"] == quiz_request.goal 
                and q["difficulty"] == quiz_request.difficulty
            ]
            questions.extend(random.sample(filtered, min(remaining, len(filtered))))
        
        return QuizResponse(
            quiz_id=f"quiz_{random.randint(1000,9999)}",
            goal=quiz_request.goal,
            questions=questions[:quiz_request.num_questions]
        )