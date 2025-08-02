import pdfminer.high_level  # type: ignore
import re
import requests  # type: ignore
from pdfminer.pdfparser import PDFParser  # pyright: ignore[reportMissingImports]
from pdfminer.pdfdocument import PDFDocument  # type: ignore
from pdfminer.pdfpage import PDFPage  # type: ignore
from pdfminer.pdfinterp import resolve1  # type: ignore


knownLangs = ["Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript", "Node.js", "Deno",
    "React", "Vue", "Angular", "Next.js", "Nuxt.js", "Svelte", "jQuery", "Express", 
    "NestJS", "Ember.js", "Backbone.js", "Gatsby", "Meteor", "RxJS", "Vanilla JS",
    "Ruby", "Go", "Rust", "Swift", "Kotlin", "PHP", "R", "MATLAB", "Perl", "Dart", 
    "Scala", "Shell", "Bash", "Assembly", "Objective-C", "SQL", "NoSQL", 
    "HTML", "CSS"]

knownLibraries = [
    "NumPy", "Pandas", "Matplotlib", "Seaborn", "Scikit-learn", "SciPy",
    "TensorFlow", "PyTorch", "Keras", "Theano", "JAX", "MXNet", "CNTK",
    "FastAI", "HuggingFace", "Transformers", "Detectron2", "Albumentations", 
    "OpenCV", "DeepFace", "Ultralytics", "YOLOv5", "YOLOv8",
    "SpaCy", "NLTK", "Gensim", "TextBlob", "Flair", "Stanza", "Polyglot",
    "Pillow", "ImageAI", "SimpleITK", "Mahotas", "scikit-image",
    "Feature-engine", "CategoryEncoders", "Imbalanced-learn", "PyCaret", 
    "LightGBM", "XGBoost", "CatBoost",
    "Auto-sklearn", "TPOT", "H2O", "MLBox", "AutoKeras", "Autogluon",
    "Plotly", "Bokeh", "Dash", "Altair", "Yellowbrick", "Missingno",
    "MLflow", "Weights & Biases", "Optuna", "Hydra", "Comet", "Neptune.ai",
    "Jupyter", "Anaconda", "Streamlit", "Gradio", "Flask", "FastAPI", "Django",
    "Docker", "Kubernetes", "Airflow", "Ray", "DVC", "ONNX", "TorchServe",
    "TensorRT", "NVIDIA Triton", "Triton Inference Server", "Kubeflow",
    "TFLite", "Core ML", "Edge Impulse", "Hugging Face Hub"
]


def extractLangs(textPiece):
    lines = textPiece.splitlines()
    extractedLangs = []
    for i in knownLangs:
        for k in lines:
            if i.casefold() in k.casefold().split():
                extractedLangs.append(i)
            else:
                pass
    return extractedLangs


def libraries(textPiece):
    lines = textPiece.splitlines()
    extractedLibraries = []
    for i in knownLibraries:
        for k in lines:
            if i.casefold() in k.casefold().split():
                extractedLibraries.append(i)
            else:
                pass
    return extractedLibraries


def extractHyperlinks(pdfPath):
    hyperlinks = []

    with open(pdfPath, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)

        for page in PDFPage.create_pages(doc):
            if hasattr(page, 'annots') and page.annots:
                annotations = resolve1(page.annots)
                for annot in annotations:
                    annotObj = resolve1(annot)
                    if 'A' in annotObj:
                        uri = annotObj['A'].get('URI')
                        if uri:
                            if isinstance(uri, bytes):
                                uri = uri.decode('utf-8', errors='ignore')
                            hyperlinks.append(uri)

    return hyperlinks


def getGitHubRepoCount(githubUsername):
    try:
        url = f'https://api.github.com/users/{githubUsername}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('public_repos', 'Not found')
        else:
            return f"GitHub API Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"


def analyzeResume(pdfPath):
    text = pdfminer.high_level.extract_text(pdfPath)
    cleanText = text
    for i in [",", ".", "/", ".js"]:
        cleanText = cleanText.replace(i, " ")  # cleans off punctuations

    langs = extractLangs(cleanText)
    libs = libraries(cleanText)
    links = extractHyperlinks(pdfPath)

    emails = [link.replace("mailto:", "") for link in links if isinstance(link, str) and link.startswith("mailto:")]
    linkedin = [link for link in links if "linkedin.com" in link]
    github = [link for link in links if "github.com" in link]
    leetcode = [link for link in links if "leetcode.com" in link]
    githubUsername = github[0].split('/')[-1] if github else ""
    repoCount = getGitHubRepoCount(githubUsername) if githubUsername else "N/A"

    return {
        "emails": emails,
        "linkedin": linkedin,
        "github": github,
        "leetcode": leetcode,
        "githubRepos": repoCount,
        "languages": langs,
        "libraries": libs
    }
