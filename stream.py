import asyncio
import numpy as np
import requests
import cv2
import websockets
import base64
import json

cap = cv2.VideoCapture(0)

api_key = "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"

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

topLeft = (160, 120)
bottomRight = (480, 360)
threshold = 240
delay = 0.5 # Can even be 60fps if you want -> provided the threshold masks correctly and the API doesn't rate limit

def analyze_image(imageData): 
    with open ('prompt.txt', 'r') as f:
        prompt = f.read()

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{imageData}"
              }
            }
          ]
        }
      ],
      "max_tokens": 1000
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response = response.json()
    print(response)
    response_text = response['choices'][0]['message']['content']

    # Parse out JSON_START and JSON_END
    response_text = response_text.replace('JSON_START', '').replace('JSON_END', '')
    # Parse out JSON
    response_text = response_text.replace('\'', '\"')
    print(response_text)
    response_json = json.loads(response_text)
    print(response_json)
    
    # TODO: avoid crash if not photo of plate -> parse when it is not JSON data and send empty/ignore message
    '''
    # example fix -> do tmrw
    try:
        response_json = json.loads(response_text)
    except:
        response_json = { 'status': 'error' }
    '''

    return response_json

async def send_camera_feed(websocket, path):
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # If  ixel detected in middle rectangle of frame between (160, 120) and (480, 360) thresholded from [200, 200, 200] to [255, 255, 255]
            if np.any(frame[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]] > [threshold] * 3):
                # Send frame as base64 string
                # Encode the frame to JPEG format
                _, buffer = cv2.imencode('.jpg', frame)
                jpg_bytes = base64.b64encode(buffer).decode('UTF-8')

                # Send request to localhost:3000/classify_waste to get JSON object of the waste
                res = analyze_image(jpg_bytes)
                 
                # Send the frame to connected clients
                await websocket.send(json.dumps({ 'image': jpg_bytes, 'data': res }))

                # Wait for 0.5 second before sending the next frame
                await asyncio.sleep(delay)
        else:
            print("Camera disconnected.")
            break

    cap.release()

async def main():
    async with websockets.serve(send_camera_feed, "localhost", 8765):
        print("WebSocket server running...")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())

