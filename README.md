# Plant Disease Detector

A simple Streamlit web app that uses an AI image-classification model to detect plant diseases from a photo of a leaf, and offers basic management tips for the identified condition.

## Features

- Upload a photo of a plant leaf (JPG, JPEG, or PNG)
- Automatic disease classification using a pretrained Hugging Face model
- Displays the predicted disease/condition along with a confidence score
- Suggests basic management strategies for common diseases
- ⚡ Model is cached locally after the first run for faster subsequent loads

## Demo

Upload a leaf image, and the app will:
1. Display the uploaded image
2. Analyze it using an image-classification model
3. Show the predicted label and confidence level
4. Provide a relevant management tip (or a general recommendation if the label isn't in the local database)

## Tech Stack

- [Streamlit](https://streamlit.io/) — web app framework
- [Hugging Face Transformers](https://huggingface.co/docs/transformers) — `pipeline("image-classification")`
- [Pillow (PIL)](https://python-pillow.org/) — image handling
- Model: [`linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification`](https://huggingface.co/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification)

## Installation

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```

2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install streamlit transformers pillow torch
   ```

   > **Note:** `transformers` requires a backend such as `torch` or `tensorflow` to run the image-classification pipeline. `torch` is recommended.

## Usage

Run the app with Streamlit:

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`) in your browser.

1. Click **"Choose a leaf image..."** and upload a photo of a plant leaf.
2. Wait for the spinner to finish analyzing the image.
3. View the predicted disease/condition, confidence score, and suggested management strategy.

## How It Works

1. **Model loading** — The app loads a pretrained MobileNetV2-based image classification model from Hugging Face via `st.cache_resource`, so it only downloads once and is reused across sessions.
2. **Image upload** — The user uploads an image, which is opened with PIL and displayed in the app.
3. **Inference** — The image is passed to the classification pipeline, which returns a ranked list of predicted labels with confidence scores.
4. **Management tips** — The top predicted label is looked up in a local `management_tips` dictionary to surface a relevant care/treatment tip. If the label isn't found, a generic fallback message is shown.

## Extending the App

- **Add more diseases:** Expand the `management_tips` dictionary with additional labels and tips matching the model's output classes.
- **Show multiple predictions:** Modify the results-handling logic to display the top-N predictions (e.g., `results[:3]`) instead of just the top one.
- **Improve UI:** Add columns, expanders, or charts (e.g., a bar chart of confidence scores) to make results more visual.
- **Swap models:** Replace the model string in `load_model()` with another Hugging Face image-classification model suited to your use case.

## Disclaimer

This tool is intended for informational purposes only and should not replace advice from a qualified agricultural expert. Predictions and confidence scores depend on the underlying AI model and may not always be accurate.

## License

Add your preferred license here (e.g., MIT, Apache 2.0).