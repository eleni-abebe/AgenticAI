# social_media_agent.py

# Step 1: Import packages
import asyncio
import os
from agents import Agent, Runner, function_tool  # Removed WebSearchTool, ItemHelpers
from openai import OpenAI
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import List
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

# Step 2: Get OpenAI key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Step 3: Define tools
@function_tool
def generate_social_media_content(video_transcript: str, social_media_platform: str):
    """Generate platform-specific humorous post from transcript."""
    print(f"Generating content for {social_media_platform}...")
    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        model="gpt-4o",  # ✅ Changed to gpt-4o (supports function-like tools)
        messages=[
            {"role": "system", "content": "You are a creative and humorous social media content generator."},
            {"role": "user", "content": f"Generate engaging, humorous content for {social_media_platform} based on this video transcript:"},
            {"role": "assistant", "content": video_transcript},
            {"role": "user", "content": f"Now write a catchy, funny post suitable for {social_media_platform}."}
        ],
        max_tokens=300,
        temperature=0.8,
        top_p=1.0
    )
    # ✅ Fixed key access (modern API returns dict-like object)
    return response.choices[0].message["content"]

# Step 4: Define dataclass
@dataclass
class Post:
    platform: str
    content: str

# Step 5: Define the agent
content_writer_agent = Agent(
    name="Content Writer Agent",
    instructions=(
        "You are a witty and engaging social media writer. "
        "Based on a video transcript, generate humorous posts for various platforms. "
        "Avoid copying text verbatim."
    ),
    model="gpt-4o",  # ✅ supports tools
    tools=[generate_social_media_content],
    output_type=List[Post],
)

# Step 6: Fetch YouTube transcript safely
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

def fetch_video_transcript(video_id: str) -> str:
    print(f"Fetching transcript for video ID: {video_id}")
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try to find manually created English transcript first
        try:
            transcript = transcript_list.find_transcript(['en'])
        except NoTranscriptFound:
            # If not found, use auto-generated
            transcript = transcript_list.find_generated_transcript(['en'])

        # Fetch and join text parts
        text = " ".join([entry['text'] for entry in transcript.fetch()])
        print("✅ Transcript fetched successfully.")
        return text

    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        print(f"❌ Transcript not available for this video: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error fetching transcript: {e}")
    return ""

# Step 7: Main async function
async def main(video_id: str, platforms: List[str]):
    video_transcript = fetch_video_transcript(video_id)

    if not video_transcript:
        print("❌ No transcript available. Exiting.")
        return

    runner = Runner()
    tasks = [
        runner.run(content_writer_agent, platform)
        for platform in platforms
    ]

    results = await asyncio.gather(*tasks)

    # ✅ Clean printing
    for platform, result in zip(platforms, results):
        post = result[0]
        print(f"\n=== Content for {platform} ===\n{post.content}\n")

# Step 8: Entry point
if __name__ == "__main__":
    video_id = "arj7oStGLkU"

    platforms = ["Twitter", "Instagram", "Facebook"]
    asyncio.run(main(video_id, platforms))
