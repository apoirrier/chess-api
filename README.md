# Chess Opening Trainer API

A small FastAPI application that provides chess opening training support:
- a computer move suggestion endpoint
- player move evaluation feedback

## Project structure

```
backend/ 
├── app/ 
│ ├── main.py                FastAPI app configuration
│ ├── api/ 
│ │ ├── computer.py          /computer/play route
│ │ └── feedback.py          /feedback/evaluate route
│ │ 
│ ├── common/ 
│ │ ├── chess.py             Helper functions for chess
│ │ └── feedback.py          Feedback definitions
│ │ 
│ ├── schemas/ 
│ │ ├── feedback.py          Feedback model and types
│ │ ├── requests.py          Request payload models
│ │ └── responses.py         Response payload models
│ │ 
│ ├── services/ 
│ │ ├── computer_service.py  Computer move logic
│ │ └── feedback_service.py  Player move feedback logic
│ │ 
├── README.md                README file
├── requirements.txt         Dependencies file
└── run.py                   Application endpoint
```

## Requirements

- Python 3.11+ (recommended)
- Pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run locally

```bash
python run.py
```

Then open: `http://127.0.0.1:8000/`

## API Endpoints

### POST `/computer/play`

Request body:

```json
{
  "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
}
```

Response body:

```json
{
  "move": "e4"
}
```

This endpoint returns the computer's next opening move for supported positions.

### POST `/feedback/evaluate`

Request body:

```json
{
  "before": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  "move": "e4"
}
```

Response body:

```json
{
  "feedback": {
    "type": "success",
    "message": null
  }
}
```

This endpoint evaluates the player's move and returns structured feedback.
