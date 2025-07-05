// src/components/QuizForm.js
import React, { useState } from 'react';
import { TextField, Button, Select, MenuItem, FormControl, InputLabel, Box } from '@mui/material';

export default function QuizForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    goal: '',
    num_questions: '',
    difficulty: ''
  });

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
  };

  return (
    <Box component="form" onSubmit={(e) => { e.preventDefault(); onSubmit(formData); }}>
      <FormControl fullWidth margin="normal">
       <InputLabel>Goal</InputLabel>
        <Select
          name="goal"
          value={formData.goal}
          onChange={handleChange}
          label="Goal"
        >
          <MenuItem value="CAT">CAT</MenuItem>
          
          
        </Select>
      </FormControl>
      
      
      <TextField
        fullWidth
        type="number"
        label="Number of Questions"
        name="num_questions"
        value={formData.num_questions}
        onChange={handleChange}
        margin="normal"
        inputProps={{ min: 5, max: 10 }}
      />
      
      <FormControl fullWidth margin="normal">
        <InputLabel>Difficulty</InputLabel>
        <Select
          name="difficulty"
          value={formData.difficulty}
          onChange={handleChange}
          label="Difficulty"
        >
          <MenuItem value="beginner">Beginner</MenuItem>
          <MenuItem value="intermediate">Intermediate</MenuItem>
          <MenuItem value="advanced">Advanced</MenuItem>
        </Select>
      </FormControl>
      
      <Button type="submit" variant="contained" fullWidth>
        Generate Quiz
      </Button>
    </Box>
  );
}