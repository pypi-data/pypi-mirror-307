# Available models mapping
AVAILABLE_MODELS = {
    "swinv2-v3": "SmilingWolf/wd-swinv2-tagger-v3",
    "convnext-v3": "SmilingWolf/wd-convnext-tagger-v3",
    "vit-v3": "SmilingWolf/wd-vit-tagger-v3",
    "vit-large-v3": "SmilingWolf/wd-vit-large-tagger-v3",
    "eva02-large-v3": "SmilingWolf/wd-eva02-large-tagger-v3",
    "moat-v2": "SmilingWolf/wd-v1-4-moat-tagger-v2",
    "swinv2-v2": "SmilingWolf/wd-v1-4-swinv2-tagger-v2",
    "convnext-v2": "SmilingWolf/wd-v1-4-convnext-tagger-v2",
    "convnextv2-v2": "SmilingWolf/wd-v1-4-convnextv2-tagger-v2",
    "vit-v2": "SmilingWolf/wd-v1-4-vit-tagger-v2"
}


KAOMOJI = [
    "0_0", "(o)_(o)", "+_+", "+_-", "._.", "<o>_<o>",
    "<|>_<|>", "=_=", ">_<", "3_3", "6_9", ">_o",
    "@_@", "^_^", "o_o", "u_u", "x_x", "|_|", "||_||"
]

# Model files
MODEL_FILENAME = "model.onnx"
LABEL_FILENAME = "selected_tags.csv"

# Default thresholds
DEFAULT_GENERAL_THRESHOLD = 0.35
DEFAULT_CHARACTER_THRESHOLD = 0.85

# Category mappings
CATEGORY_MAPPING = {
    'rating': 9,
    'general': 0,
    'character': 4
}