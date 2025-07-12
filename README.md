
AI-Powered Creative Writing Platform Backend

## Features

- Story idea generation with AI prompts
- Multiple writing tools (plot, character, dialogue, etc.)
- Category-based story suggestions
- Real-time statistics
- RESTful API design
- CORS enabled for frontend integration

## API Endpoints

### Core Endpoints
- `GET /` - Home page with API info
- `GET /api/health` - Health check
- `POST /api/generate-story` - Generate story ideas
- `POST /api/use-tool` - Use writing tools
- `GET /api/stats` - Get platform statistics
- `POST /api/save-story` - Save story ideas

### Utility Endpoints
- `GET /api/categories` - Get story categories
- `GET /api/tools` - Get available tools

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Access the API at `http://localhost:5000`

## Testing

Run tests with:
```bash
python test_app.py
```

## Environment Variables

Create a `.env` file with:
```
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000
```

## File Structure

```
backend/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── run.py             # Alternative run script
├── test_app.py        # Unit tests
└── README.md          # This file
```