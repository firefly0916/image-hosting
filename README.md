# Telegram Image Hosting

Telegram Image Hosting is a web application that allows users to upload images and host them via Telegram. The application uses FastAPI for the backend, SQLite for database storage, and a modern frontend for user interaction.

## Features

- **Image Upload**: Users can upload images through the web interface.
- **Telegram Integration**: Uploaded images are sent to a Telegram bot, which provides a hosted URL.
- **Database Storage**: Metadata of uploaded images is stored in a SQLite database.
- **Modern UI**: A clean and user-friendly interface for seamless interaction.

## Project Structure

```
image-hosting/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application setup
│   ├── db/
│   │   ├── database.py        # SQLite database initialization and operations
│   ├── utils/
│   │   ├── telegram_utils.py  # Telegram bot utilities
├── public/
│   ├── index.html             # Frontend HTML
│   ├── style.css              # Frontend CSS
│   ├── app.js                 # Frontend JavaScript
├── main.py                    # Entry point for the application
├── README.md                  # Project documentation
├── pyproject.toml             # Python project configuration
├── uv.lock                    # Dependency lock file
├── .env                       # Environment variables
├── LICENSE                    # License file
```

## Installation

### Prerequisites

- Python 3.13
- Telegram Bot Token (create a bot via [BotFather](https://core.telegram.org/bots#botfather))

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/firefly0916/image-hosting
   cd image-hosting
   ```

2. Install Python dependencies:
   ```bash
   pip install uv
   uv venv
   uv sync
   ```

3. Set up environment variables:
   Copy `.env.example` file to `.env` in the root directory with the following content:
   ```
   TG_BOT_TOKEN=your_telegram_bot_token
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Open the application in your browser:
   ```
   http://127.0.0.1:8000
   ```

## Usage

1. Open the web interface.
2. Select an image file to upload.
3. Click the "Upload" button.
4. The uploaded image will be sent to the Telegram bot, and a hosted URL will be displayed.

## Technical Details

### Backend

- **Framework**: FastAPI
- **Database**: SQLite
- **Telegram Integration**: Uses Telegram Bot API for file uploads.

### Frontend

- **HTML/CSS/JavaScript**: A modern and responsive design for user interaction.

### Database

The SQLite database stores metadata of uploaded files, including:
- `id`: Auto-incremented primary key.
- `filename`: Name of the uploaded file.
- `url`: Hosted URL of the file.
- `upload_time`: Timestamp of the upload.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLite](https://www.sqlite.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)