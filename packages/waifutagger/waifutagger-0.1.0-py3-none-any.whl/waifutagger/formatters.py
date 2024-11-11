from typing import Dict, List, Optional
import json

def format_tags(
    results: Dict,
    include_scores: bool = False,
    exclude_rating: bool = False
) -> str:
    """
    Format prediction results as a comma-separated string.
    
    Args:
        results: Prediction results dictionary
        include_scores: Whether to include confidence scores
        exclude_rating: Whether to exclude rating tag
        
    Returns:
        Formatted string of tags
    """
    tags = []
    
    # Add rating
    if not exclude_rating:
        rating_tag = results['rating'][0]
        if include_scores:
            rating_tag = f"{rating_tag} ({results['rating'][1]:.2%})"
        tags.append(rating_tag)
    
    # Add general tags
    for tag, score in results['general_tags'].items():
        if include_scores:
            tags.append(f"{tag} ({score:.2%})")
        else:
            tags.append(tag)
    
    # Add character tags
    for tag, score in results['character_tags'].items():
        if include_scores:
            tags.append(f"{tag} ({score:.2%})")
        else:
            tags.append(tag)
    
    return ", ".join(tags)

def format_as_json(results: Dict, indent: Optional[int] = None) -> str:
    """Format results as JSON string."""
    return json.dumps(results, indent=indent)

def format_as_sd_prompt(
    results: Dict,
    include_scores: bool = True,
    exclude_rating: bool = True
) -> str:
    """
    Format results as Stable Diffusion prompt.
    
    Args:
        results: Prediction results dictionary
        include_scores: Whether to include weight values
        exclude_rating: Whether to exclude rating tag
    
    Returns:
        Formatted prompt string
    """
    tags = []
    
    # Add rating
    if not exclude_rating:
        rating_tag = results['rating'][0]
        if include_scores:
            rating_tag = f"({rating_tag}:{results['rating'][1]:.2f})"
        tags.append(rating_tag)
    
    # Add general tags
    for tag, score in results['general_tags'].items():
        if include_scores:
            tags.append(f"({tag}:{score:.2f})")
        else:
            tags.append(tag)
    
    # Add character tags
    for tag, score in results['character_tags'].items():
        if include_scores:
            tags.append(f"({tag}:{score:.2f})")
        else:
            tags.append(tag)
    
    return ", ".join(tags)