# Social Media Agent

This project generates humorous and engaging social media posts from YouTube video transcripts using OpenAI's GPT models.

## Features

- Fetches YouTube video transcripts automatically
- Generates platform-specific social media content (Twitter, Instagram, Facebook, etc.)
- Uses OpenAI GPT-4o for creative post generation
- Easy to extend for other platforms or content styles

## Setup

1. **Clone the repository**  
   ```
   git clone <your-repo-url>
   cd mini_project_3
   ```

2. **Create and activate a virtual environment**  
   ```
   python -m venv venv
   # On Windows (cmd):
   venv\Scripts\activate
   # On Git Bash:
   source venv/Scripts/activate
   ```

3. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```
   If you don't have a `requirements.txt`, install manually:
   ```
   pip install openai youtube_transcript_api python-dotenv
   ```

4. **Add your OpenAI API key**  
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the agent with a YouTube video ID:
```
python social_media_agent.py
```
You can change the `video_id` and platforms in the script as needed.

## Example Output

```
Fetching transcript for video ID: arj7oStGLkU
✅ Transcript fetched successfully.

=== Content for Twitter ===
[Generated humorous post]

=== Content for Instagram ===
[Generated humorous post]

=== Content for Facebook ===
[Generated humorous post]
```

## Notes

- Not all YouTube videos have transcripts available. Use videos with English subtitles for best results.
- The `agents.py` file must define `Agent`, `Runner`, and `function_tool` as used in the script.

## License

MIT License