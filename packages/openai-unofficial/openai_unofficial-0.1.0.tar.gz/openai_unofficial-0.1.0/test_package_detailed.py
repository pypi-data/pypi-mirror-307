import json
import base64
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))
from openai_unofficial import OpenAIUnofficial

def test_list_models():
    """Test listing available models"""
    client = OpenAIUnofficial()
    models = client.list_models()
    print("\n=== Available Models ===")
    for model in models['data']:
        print(f"- {model['id']}")

def test_chat_completion_basic():
    """Test basic chat completion"""
    client = OpenAIUnofficial()
    
    print("\n=== Basic Chat Completion ===")
    response = client.chat.create(
        messages=[{"role": "user", "content": "Say hello!"}],
        model="gpt-4o-mini-2024-07-18"
    )
    print("Response:", response['choices'][0]['message']['content'])

def test_chat_completion_streaming():
    """Test streaming chat completion"""
    client = OpenAIUnofficial()
    
    print("\n=== Streaming Chat Completion ===")
    stream_response = client.chat.create(
        messages=[
            {"role": "user", "content": "Write a short story about a robot."}
        ],
        model="gpt-4o-mini-2024-07-18",
        stream=True
    )
    
    print("Streaming response:")
    for chunk in stream_response.iter_lines():
        if chunk:
            chunk_data = chunk.decode('utf-8').strip()
            if chunk_data != "[DONE]":
                try:
                    chunk_data = json.loads(chunk_data.replace('data: ', ''))
                    if 'choices' in chunk_data and chunk_data['choices']:
                        content = chunk_data['choices'][0].get('delta', {}).get('content', '')
                        if content:
                            print(content, end='', flush=True)
                except json.JSONDecodeError:
                    continue
    print()  # New line after streaming complete

def test_audio_preview_model():
    """Test GPT-4O Audio Preview model"""
    client = OpenAIUnofficial()
    
    print("\n=== Audio Preview Model Test ===")
    response = client.chat.create(
        messages=[
            {"role": "user", "content": "Tell me about the importance of coding."}
        ],
        model="gpt-4o-audio-preview-2024-10-01",
        modalities=["text", "audio"],
        audio={"voice": "fable", "format": "wav"}
    )
    
    # Handle text response
    if 'choices' in response and response['choices']:
        message = response['choices'][0].get('message', {})
        if 'content' in message:
            print("Text Response:", message['content'])
        
        # Handle audio response
        if 'audio' in message and 'data' in message['audio']:
            wav_bytes = base64.b64decode(message['audio']['data'])
            output_file = "audio_preview_test.wav"
            with open(output_file, "wb") as f:
                f.write(wav_bytes)
            print(f"Audio saved to {output_file}")
            print("Audio Transcript:", message['audio']['transcript'])

def test_audio_speech():
    """Test standard audio speech generation"""
    client = OpenAIUnofficial()
    
    print("\n=== Audio Speech Generation ===")
    # Test different voices
    voices = ["nova", "echo", "fable", "onyx", "shimmer", "alloy"]
    
    for voice in voices:
        print(f"Testing voice: {voice}")
        audio_data = client.audio.create(
            input_text=f"This is a test of the {voice} voice.",
            model="tts-1-hd-1106",
            voice=voice
        )
        
        output_file = f"test_audio_{voice}.mp3"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        print(f"Audio file saved as {output_file}")

def test_image_generation():
    """Test image generation with different parameters"""
    client = OpenAIUnofficial()
    
    print("\n=== Image Generation ===")
    
    # Test DALL-E 3 with different sizes
    sizes = ["1024x1024", "1792x1024", "1024x1792"]
    for size in sizes:
        print(f"\nTesting DALL-E 3 with size {size}")
        response = client.images.create(
            prompt="A beautiful sunset over mountains",
            model="dall-e-3",
            size=size,
            quality="hd"
        )
        print(f"Image URL ({size}):", response['data'][0]['url'])
    
    # Test DALL-E 2 with different parameters
    print("\nTesting DALL-E 2")
    response = client.images.create(
        prompt="A futuristic city",
        model="dall-e-2",
        n=2,  # Generate multiple images
        size="512x512"
    )
    for idx, image in enumerate(response['data']):
        print(f"Image {idx + 1} URL:", image['url'])

def test_realtime_model():
    """Test GPT-4O Realtime model"""
    client = OpenAIUnofficial()
    
    print("\n=== Realtime Model Test ===")
    try:
        response = client.chat.create(
            messages=[
                {"role": "user", "content": "What's the current time?"}
            ],
            model="gpt-4o-realtime-preview-2024-10-01"
        )
        print("Realtime Response:", response['choices'][0]['message']['content'])
    except Exception as e:
        print("Note: Realtime model testing may require specific implementation details")
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== Starting Comprehensive API Tests ===")
    
    # Run all tests
    test_list_models()
    test_chat_completion_basic()
    test_chat_completion_streaming()
    test_audio_preview_model()
    test_audio_speech()
    test_image_generation()
    test_realtime_model()
    
    print("\n=== All Tests Completed ===")