from openai import OpenAI
import os
import base64

client = OpenAI()

def open_file (file_path):
    with open(file_path, 'rb') as image_file:
        base64_encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        # add data:image/jpeg;base64,
        base64_encoded_image = "data:image/jpeg;base64," + base64_encoded_image
        return base64_encoded_image

def open_images_base64(folder_path): 
    # go through all images in the folder and return a list of base64 encoded images
    images = []
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if os.path.isfile(image_path):
            images.append(open_file(image_path))
    return images

def analyze_image(images, question, is_url): 
    request_content = [{ "type": "text", "text": question }]

    for image in images:
        if is_url: 
            request_content.append({ "type": "image_url", "image_url": { "url": image }})
        else: 
            request_content.append({ "type": "image_url", "image_url": { "url": image }})

    response = client.chat.completions.create(
        model="gpt-4-vision-preview", 
        messages=[
            {
                "role": "user", 
                "content": request_content
            }
        ],
        max_tokens=1000,
    )

    return response.choices[0].message.content



if __name__ == "__main__": 
    # image_url_1 = "https://the-bin-project-plates.s3.ap-southeast-1.amazonaws.com/img.jpg"
    # image_url_2 = "https://the-bin-project-plates.s3.ap-southeast-1.amazonaws.com/frame_20124.jpg"
    # image_urls = [image_url_1, image_url_2]

    # image_base64_1 = open_file("frame_4233.jpg")
    # image_base64_2 = open_file("frame_7512.jpg")
    # images_base64 = [image_base64_1, image_base64_2]

    images_base64 = open_images_base64("images")
    print (images_base64)

    with open ('prompt.txt', 'r') as f:
        PROMPT = f.read()

    # # result1 = analyze_image(image_urls, PROMPT, True)
    result2 = analyze_image(images_base64, PROMPT, False)

    # # print ("RESULT 1:")
    # # print (result1)
    # # print ()
    print ("RESULT 2:")
    print (result2)
