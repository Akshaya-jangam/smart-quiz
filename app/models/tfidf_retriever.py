from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TFIDFRetriever:
    def __init__(self, question_bank):
        self.question_bank = question_bank
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self._fit_vectorizer()
        
    def _fit_vectorizer(self):
        texts = [f"{q['question']} {q.get('topic','')}" for q in self.question_bank]
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        
    def retrieve_questions(self, goal, num_questions, difficulty):
        try:
            filtered = [
                q for q in self.question_bank 
                if q["goal"] == goal 
                and q["difficulty"] == difficulty
            ]
            
            if not filtered:
                return []
                
            goal_vec = self.vectorizer.transform([goal])
            similarities = cosine_similarity(goal_vec, self.tfidf_matrix).flatten()
            
            filtered_indices = [i for i, q in enumerate(self.question_bank) 
                              if q in filtered]
            filtered_similarities = similarities[filtered_indices]
            
            top_indices = np.argsort(filtered_similarities)[-num_questions:][::-1]
            return [filtered[i] for i in top_indices]
            
        except Exception as e:
            print(f"Retrieval error: {str(e)}")
            return []