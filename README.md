# Chess Opening Trainer API

A small FastAPI application that provides chess opening training support:
- a computer move suggestion endpoint
- player move evaluation feedback

## Project structure

```
backend/ 
├── app/ 
│ ├── main.py                    FastAPI app configuration
│ ├── api/ 
│ │ ├── computer.py              /computer/play route
│ │ ├── deps.py                  dependencies, used for authentication
│ │ ├── feedback.py              /feedback/evaluate route
│ │ ├── opening_name.py          /opening-name route
│ │ └── pgn.py                   /pgn route
│ │
│ ├── db/ 
│ │ ├── base.py                  Base class for DB models
│ │ ├── session.py               Connection to database
│ │ └── db/ 
│ │   ├── __init__.py            Export models
│ │   ├── computer_move.py       DB model for computer moves
│ │   ├── feedback.py            DB model for feedbacks
│ │   └── position.py            DB model for positions
│ │
│ ├── schemas/ 
│ │ ├── feedback_type.py         Feedback type type
│ │ ├── feedback.py              Feedback schema
│ │ ├── requests.py              Requests schemas
│ │ └── responses.py             Responses schemas
│ │ 
│ └── services/ 
│   ├── auth_service.py          Authentication verification
│   ├── chess.py                 Chess helper functions
│   ├── computer_service.py      Computer move logic
│   ├── feedback_service.py      Player move feedback logic
│   ├── opening_name_service.py  Opening name logic
│   └── pgn_service.py           Import PGN logic
│
├── opening_names/               Folder for adding opening names to database 
├── README.md                    README file
├── requirements.txt             Dependencies file
└── run.py                       Application endpoint
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

## Type checking and Linting

```bash
ruff check .
ruff format .
pyright
```

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
