from sambanova_unofficial_api import Sambanova_Unofficial_API

if __name__ == "__main__":
    api = Sambanova_Unofficial_API('_zitok=4XXXXXXXXXXXg')
    print(f"\nResponse: {api.chat('Hi, who are you?')}")
    image_path = r'C:\Users\Sujal Rajpoot\Pictures\Saved Pictures\bug in chattebot.png'
    print(f"\nResponse: {api.vision('Please provide a detailed description of the image, including its contents, colors, and any notable features.', image_path=image_path)}")