# AI Video Agent

AI Video Agent is a Python-based video intelligence application that turns YouTube videos or local audio/video files into structured knowledge. It transcribes content, summarizes key talking points, extracts action items and decisions, and allows users to ask questions about the video using a retrieval-based chat flow.

## Project Purpose

This project helps users quickly understand long-form video content without watching the entire recording. It is designed for meetings, lectures, tutorials, and video-based knowledge work where users need summaries, action tracking, and contextual Q&A from the content.

## Tools and Libraries Used

- Whisper — Converts audio to text accurately for English transcription locally.
- Sarvam — Converts audio to text accurately for Hinglish transcription locally.
- PyDub — Splits and normalizes audio chunks for easier processing reliably.
- yt-dlp — Downloads YouTube audio efficiently for video-based processing.
- LangChain + Mistral — Orchestrates prompts, summaries, and AI-based reasoning workflows.
- ChromaDB — Stores transcript embeddings for fast semantic question answering later.
- Python-dotenv — Loads environment variables securely from local configuration files.
- FFmpeg — Processes audio and video formats required across the pipeline.
- Streamlit — Builds the interactive web interface for uploading videos and viewing results.

## Core Blocks and Features

### 1. Input Processing
- Accepts either a YouTube URL or a local file path.
- Downloads or converts media into audio format.
- Splits large audio files into manageable chunks for transcription.

### 2. Transcription Pipeline
- Uses Whisper for English transcription.
- Supports Hinglish transcription through Sarvam AI translation-based transcription.
- Joins all chunk transcripts into a complete conversation transcript.

### 3. AI Summary and Extraction Engine
- Generates a professional title from the transcript.
- Summarizes the full content in a concise and structured format.
- Extracts:
  - action items
  - key decisions
  - open questions and follow-ups

### 4. Retrieval-Augmented Chat (RAG)
- Builds a vector store from the transcript.
- Retrieves relevant transcript chunks for a user question.
- Uses an LLM to answer questions strictly from the provided video content.

### 5. Streamlit Interface
- Provides a simple UI for:
  - entering video URL or file path
  - choosing language
  - processing the video
  - viewing summary, decisions, action items, and transcript
  - chatting with the processed content

## How It Works

1. User enters a YouTube URL or local media file.
2. The system downloads or converts the media into WAV format.
3. Audio is split into chunks for efficient processing.
4. Speech is transcribed using Whisper or Sarvam based on chosen language.
5. The transcript is sent through the AI analysis pipeline.
6. The system generates:
   - title
   - summary
   - action items
   - key decisions
   - open questions
7. The transcript is embedded into a vector database.
8. The user can ask questions and get answers grounded in the video context.

## How to Use the Application

### Prerequisites
- Python 3.9+
- FFmpeg installed and added to your system PATH
- A valid Mistral API key
- Optional: Sarvam API key for Hinglish transcription

### 1. Clone the Repository
```bash
git clone https://github.com/Thivikram-Thummala/AI-Video-Agent.git
cd AI-Video-Agent
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root and add:

```env
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key
```

### 5. Run the Application
```bash
streamlit run app.py
```

### 6. Use the Interface
- Paste a YouTube URL or provide a local file path
- Select the language (`english` or `hinglish`)
- Click the Process Video button
- View the generated:
  - title
  - summary
  - action items
  - key decisions
  - open questions
  - transcript
- Ask questions in the chat panel to interact with the processed video content

## Project Structure

```text
AI-Video-Agent/
├── app.py
├── main.py
├── requirements.txt
├── .env
├── core/
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── summarizer.py
│   ├── transcriber.py
│   └── vector_store.py
├── utils/
│   └── audio_processor.py
├── downloaders/
└── README.md
```

## Notes

- This project is useful for educational content, meetings, and research videos.
- The RAG chat answers questions only from the transcript context.
- English transcription uses a local Whisper model, while Hinglish uses Sarvam-based transcription.

## License

This project is currently for personal or educational use unless otherwise specified by the owner.
