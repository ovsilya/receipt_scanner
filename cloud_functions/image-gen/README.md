# OpenAI Image Generation Function on GCP

This is a Google Cloud Function (GCF) that uses the OpenAI's image generation API to generate images based on the prompts it receives.

## Summary
Upon deploying, this function listens to HTTP requests and expects to get a JSON payload with a specific structure. This payload contains the prompt based on which OpenAI generates an image.

The URL of the generated image is then returned in the HTTP response.

## How does it work?

This function is designed to work on Google Cloud Platform, particularly with Google's Functions Framework. It's written in Python and utilizes OpenAI's Python library to interact with OpenAI's API.

The function named `image_gen` is the entry point of this program.

This function retrieves the JSON payload from the HTTP request body and expects to find a field called `prompt_image`. The value of this field is an image prompt that user provides.

The function then calls OpenAI's Image.create() method, which takes a few arguments:
 - `prompt`: The image prompt that the user fed to the function through the HTTP request.
 - `n`: The number of images to generate. Here it's set to 1.
 - `size`: The size of the generated image(s). Here it's set to 1024x1024.

After generating the image, the function fetches the URL where the image is hosted and returns it in the HTTP response as JSON. 

## Environment Variables

This function depends on a few environment variables:

- `OPENAI_ORGANIZATION`: The ID of the organization in OpenAI
- `OPENAI_API`: The key to use OpenAI's APIs

You need to make sure these environment variables are correctly set in your GCF environment.

## Sample Request and Response

Given a request as follows:

```JSON
{
  "input": {
    "body": {
      "prompt_image": "Image of a sunset over mountains"
    }
  }
}
```

The function will return a response similar to this:

```JSON
{
  "image_url": "https://images.openai.com/v1/images/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```
The `image_url` is the URL where the generated image is hosted.