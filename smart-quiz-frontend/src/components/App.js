// src/components/App.js
import React, { useState } from 'react';
import QuizForm from './QuizForm';
import QuizDisplay from './QuizDisplay';
import { generateQuiz } from '../services/api';



export default function App() {
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (formData) => {
    setLoading(true);
    try {
      const response = await generateQuiz(formData);
      setQuiz(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Smart Quiz Generator</h1>
      {!quiz ? (
        <QuizForm onSubmit={handleSubmit} />
      ) : (
        <QuizDisplay quiz={quiz} />
      )}
    </div>
  );
}