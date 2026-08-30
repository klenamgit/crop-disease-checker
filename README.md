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
   pip install -r requirements.txt
   ```

   `requirements.txt`:
   ```
   streamlit
   transformers>=4.57
   torch
   torchvision
   pillow
   ```

   > **Note:** `transformers` requires a backend such as `torch` or `tensorflow` to run the image-classification pipeline. `torchvision` is included to satisfy optional imports used by some of `transformers`' newer image processors — without it, Streamlit's file watcher logs (harmless but noisy) `ModuleNotFoundError` warnings on startup.

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

## Deploying on Streamlit Community Cloud

This app runs fine on [Streamlit Community Cloud](https://streamlit.io/cloud). A few environment quirks to be aware of if you deploy there:

- **Python version:** Streamlit Cloud may provision a very new Python version (e.g. 3.14) that some ML packages don't yet ship prebuilt wheels for. If you hit build errors, go to your app's **Settings → General** in the Streamlit Cloud dashboard and pick an older, more broadly-supported Python version (e.g. 3.11), then reboot. Note: a `runtime.txt` file is **not** used to set this on Community Cloud — the version is set via the dashboard.
- **Don't pin old exact versions** (e.g. `torch==2.5.1`, `transformers==4.46.3`) unless you also pin a compatible Python version. Older pinned releases often only exist as source distributions for newer Python versions, which can fail to build (e.g. `tokenizers` requiring a Rust toolchain that doesn't yet support very new Python versions). Prefer open-ended, current version ranges (as in `requirements.txt` above) so pip resolves versions with prebuilt wheels.
- After changing `requirements.txt` or Python version, use **Manage app → ⋮ → Reboot app** so the environment is rebuilt from scratch rather than reusing a cached one.

### Troubleshooting

<details>
<summary><code>ValueError: Unrecognized image processor in linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification</code></summary>

This happens when an incompatible or bleeding-edge `transformers` build fails to auto-detect the image processor for this (older) model repo. Fix by loading the processor/model classes explicitly instead of relying on `Auto*` detection:

```python
from transformers import MobileNetV2ImageProcessor, MobileNetV2ForImageClassification, pipeline

@st.cache_resource
def load_model():
    processor = MobileNetV2ImageProcessor.from_pretrained(
        "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
    )
    model = MobileNetV2ForImageClassification.from_pretrained(
        "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
    )
    return pipeline("image-classification", model=model, image_processor=processor)
```
</details>

<details>
<summary><code>Failed building wheel for tokenizers</code> / PyO3 / maturin errors</summary>

Caused by pinning an old `transformers`/`tokenizers` version that has no prebuilt wheel for the Python version in use, forcing a from-source Rust build that fails. Remove the exact version pins and let pip resolve current versions (see `requirements.txt` above), or pin an older Python version via the Streamlit Cloud dashboard.
</details>

<details>
<summary><code>ModuleNotFoundError: No module named 'torchvision'</code> in the logs on startup</summary>

Harmless — Streamlit's file watcher inspects optional `transformers` model modules that reference `torchvision`, even though this app doesn't use them. Add `torchvision` to `requirements.txt` to silence the warnings; the app runs fine either way.
</details>

## Disclaimer

This tool is intended for informational purposes only and should not replace advice from a qualified agricultural expert. Predictions and confidence scores depend on the underlying AI model and may not always be accurate.

## License

Add your preferred license here (e.g., MIT, Apache 2.0).