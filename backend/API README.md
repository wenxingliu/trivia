## Getting Started

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

## Error Handling
Errors are returned as JSON objects in the following format:

```
{
    "success": False, 
    "status_code": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Unprocessable Entity
500: Internal Error


## Endpoints

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Sample Response
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}
```

### GET '/questions'
- Fetches a list of questions. Each item in the list is a question with its answer, category and difficulty. This GET call is paginated, with 10 questions per page.
- Request Arguments: None
- Sample Response
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    ... ...
  ], 
  "success": true, 
  "total_questions": 18
}
```

### DELETE '/questions/<question_id>'
- Deletes a specific question given its ID.
- Request Arguments: question ID
- Success Response
```
{
	"success": True
}
```

### POST '/questions'
- Creates a question.
- Sample Body
```
{
	"question": "What is your name?",
	"answer": "XX",
	"category": 1,
	"difficulty": 1
}
```
- Success Response
```
{"success": True}
```

### POST '/questions/search'
- Get questions based on a search term, not case sensitive.
- Sample Body
```
{
	"searchTerm": movie
}
```
- Sample Response
```
```

### GET '/categories/<category_id>/questions'
- Get questions based on category
- Request Arguments: category id
- Sample Response
```
{
  "current_category": "3", 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

### POST '/quizzes'
- Get questions to play the quiz. This endpoint should take category and previous question parameters and return a random question within the given category, if provided, and that is not one of the previous questions. 
- Sample Body
```
{
	"previous_questions": [1, 2, 3],
	"quiz_cateogry": {
		"id": 1,
		"type": "Science"
	}
}
```
- Sample Response
```
{
	"success": True,
	"question": {
		"answer": "Agra", 
		"category": 3, 
		"difficulty": 2, 
		"id": 15, 
		"question": "The Taj Mahal is located in which Indian city?"
    }
}
```