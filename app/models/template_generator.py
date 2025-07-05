import random
from typing import List, Dict
import json

class TemplateGenerator:
    def __init__(self):
        self.templates = self._load_templates()
        self.concept_bank = self._load_concept_bank()
        self.goal_categories = {
            "CAT": ["quantitative", "verbal", "logical"],
            "GATE": ["technical", "quantitative", "aptitude"],
            "UPSC": ["general_knowledge", "current_affairs", "essay"]
        }
        
    def _load_templates(self) -> Dict:
        return {
            "quantitative": [
                {
                    "template": "What is {operation} of {numbers}?",
                    "params": {
                        "operation": ["sum", "product", "difference"],
                        "numbers": ["two numbers", "three numbers"]
                    },
                    "logic": {
                        "sum": lambda nums: sum(nums),
                        "product": lambda nums: nums[0] * nums[1]
                    }
                }
            ],
            "verbal": [
                {
                    "template": "Synonym of '{word}':",
                    "type": "synonym"
                },
                {
                    "template": "Antonym of '{word}':",
                    "type": "antonym"
                }
            ]
        }
    
    def _load_concept_bank(self) -> Dict:
        try:
            with open('data/concepts.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading concepts: {str(e)}")
            return {"synonyms": [], "antonyms": []}
    
    def _get_categories_by_goal(self, goal: str) -> List[str]:
        return self.goal_categories.get(goal, ["general"])
    
    def generate_questions(self, goal: str, num_questions: int, difficulty: str) -> List[Dict]:
        questions = []
        categories = self._get_categories_by_goal(goal)
        
        for _ in range(num_questions):
            category = random.choice(categories)
            template_group = self.templates.get(category, [])
            
            if not template_group:
                continue
                
            template = random.choice(template_group)
            question = self._fill_template(template, difficulty)
            
            if question:
                question.update({
                    "type": "mcq",
                    "difficulty": difficulty,
                    "goal": goal,
                    "topic": category
                })
                questions.append(question)
        
        return questions
    
    def _fill_template(self, template: Dict, difficulty: str) -> Dict:
        try:
            if template.get("type") == "synonym":
                word = random.choice(self.concept_bank.get("synonyms", []))
                return {
                    "question": template["template"].format(word=word["term"]),
                    "options": word["options"],
                    "answer": word["answer"]
                }
            elif template.get("type") == "antonym":
                word = random.choice(self.concept_bank.get("antonyms", []))
                return {
                    "question": template["template"].format(word=word["term"]),
                    "options": word["options"],
                    "answer": word["answer"]
                }
            # Add other template types as needed
            return None
            
        except Exception as e:
            print(f"Template filling error: {str(e)}")
            return None