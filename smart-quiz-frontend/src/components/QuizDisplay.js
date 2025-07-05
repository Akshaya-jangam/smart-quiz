import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Radio,
  RadioGroup,
  FormControlLabel,
  TextField,
  Button,
  Box,
  Chip
} from '@mui/material';

export default function QuizDisplay({ quiz }) {
  const [userAnswers, setUserAnswers] = useState({});
  const [score, setScore] = useState(null);
  const [showResults, setShowResults] = useState(false);

  const handleAnswerChange = (questionIndex, answer) => {
    setUserAnswers(prev => ({
      ...prev,
      [questionIndex]: answer
    }));
  };

  const calculateScore = () => {
    let correct = 0;
    quiz.questions.forEach((q, index) => {
      if (userAnswers[index] === q.answer) correct++;
    });
    setScore(Math.round((correct / quiz.questions.length) * 100));
    setShowResults(true);
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 2 }}>
      <Typography variant="h4" gutterBottom>
        {quiz.goal} Quiz
      </Typography>
      
      {quiz.questions.map((question, index) => (
        <Card key={index} sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Q{index + 1}: {question.question}
            </Typography>

            {question.type === 'mcq' ? (
              <RadioGroup
                value={userAnswers[index] || ''}
                onChange={(e) => handleAnswerChange(index, e.target.value)}
              >
                {question.options.map((option, i) => (
                  <FormControlLabel
                    key={i}
                    value={option}
                    control={<Radio />}
                    label={option}
                    disabled={showResults}
                    sx={{
                      color: showResults 
                        ? option === question.answer 
                          ? 'success.main' 
                          : userAnswers[index] === option 
                            ? 'error.main' 
                            : 'text.primary'
                        : 'text.primary'
                    }}
                  />
                ))}
              </RadioGroup>
            ) : (
              <TextField
                fullWidth
                multiline
                value={userAnswers[index] || ''}
                onChange={(e) => handleAnswerChange(index, e.target.value)}
                disabled={showResults}
                sx={{
                  '& .MuiOutlinedInput-root': {
                    bgcolor: showResults && userAnswers[index] === question.answer 
                      ? 'success.light' 
                      : showResults && userAnswers[index] !== question.answer 
                        ? 'error.light' 
                        : 'background.paper'
                  }
                }}
              />
            )}

            {showResults && (
              <Typography variant="body2" sx={{ mt: 1, fontStyle: 'italic' }}>
                Correct answer: {question.answer}
              </Typography>
            )}
          </CardContent>
        </Card>
      ))}

      {!showResults ? (
        <Button
          variant="contained"
          size="large"
          onClick={calculateScore}
          disabled={Object.keys(userAnswers).length < quiz.questions.length}
          sx={{ mt: 2 }}
        >
          Calculate Score
        </Button>
      ) : (
        <Box sx={{ textAlign: 'center', mt: 3 }}>
          <Chip 
            label={`Score: ${score}%`} 
            color={score >= 70 ? 'success' : score >= 50 ? 'warning' : 'error'}
            sx={{ fontSize: '1.2rem', p: 2 }}
          />
          <Box sx={{ textAlign: 'center', mt: 2 }}>
            <Button 
              variant="contained" 
              onClick={() => setShowResults(false)}
              sx={{ fontSize: '1.2rem', p:2 }}
            >
              Review Answers
            </Button>
          </Box>
        </Box>
      )}
    </Box>
  );
}