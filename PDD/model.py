import logging
import os
import cv2
import numpy as np
from PIL import Image
from scipy import stats

# Set up logging
logger = logging.getLogger(__name__)

class PlantDiseaseModel:
    def __init__(self):
        logger.info("Initializing Plant Disease Detection Model")
        self.initialized = True
        self.diseases = {
            'black_spot': {
                'name': 'Black Spot Disease',
                'confidence': 0.95,
                'patterns': {
                    'dark_spots': {
                        'hsv_lower': np.array([0, 0, 0]),
                        'hsv_upper': np.array([180, 255, 50]),
                        'min_area': 0.01,
                        'max_area': 0.2,
                        'weight': 0.6
                    },
                    'yellow_halo': {
                        'hsv_lower': np.array([20, 100, 100]),
                        'hsv_upper': np.array([35, 255, 255]),
                        'min_area': 0.05,
                        'max_area': 0.3,
                        'weight': 0.4
                    }
                },
                'symptoms': [
                    'Black circular spots on leaves',
                    'Yellow rings around spots',
                    'Premature leaf drop',
                    'Progressive leaf yellowing'
                ],
                'recommendations': [
                    'Remove and destroy infected leaves immediately',
                    'Improve air circulation around plants',
                    'Water at the base to keep leaves dry',
                    'Apply fungicide as recommended',
                    'Space plants properly to prevent spread'
                ]
            },
            'powdery_mildew': {
                'name': 'Powdery Mildew',
                'confidence': 0.92,
                'patterns': {
                    'white_powder': {
                        'hsv_lower': np.array([0, 0, 200]),
                        'hsv_upper': np.array([180, 30, 255]),
                        'min_area': 0.1,
                        'max_area': 0.7,
                        'weight': 0.7
                    },
                    'distortion': {
                        'hsv_lower': np.array([40, 40, 40]),
                        'hsv_upper': np.array([80, 255, 255]),
                        'min_area': 0.2,
                        'max_area': 0.8,
                        'weight': 0.3
                    }
                },
                'symptoms': [
                    'White powdery coating on leaves',
                    'Distorted leaf growth',
                    'Yellowing leaves',
                    'Stunted plant growth'
                ],
                'recommendations': [
                    'Improve air circulation immediately',
                    'Avoid overhead watering',
                    'Remove heavily infected plant parts',
                    'Apply fungicide for powdery mildew',
                    'Space plants for better airflow'
                ]
            },
            'leaf_spot': {
                'name': 'Leaf Spot Disease',
                'confidence': 0.90,
                'patterns': {
                    'brown_spots': {
                        'hsv_lower': np.array([10, 60, 20]),
                        'hsv_upper': np.array([20, 255, 200]),
                        'min_area': 0.01,
                        'max_area': 0.3,
                        'weight': 0.5
                    },
                    'yellow_halo': {
                        'hsv_lower': np.array([20, 100, 100]),
                        'hsv_upper': np.array([35, 255, 255]),
                        'min_area': 0.02,
                        'max_area': 0.4,
                        'weight': 0.5
                    }
                },
                'symptoms': [
                    'Brown or black spots on leaves',
                    'Spots with yellow halos',
                    'Holes in leaves',
                    'Leaf drop'
                ],
                'recommendations': [
                    'Remove infected leaves promptly',
                    'Avoid overhead watering',
                    'Improve air circulation',
                    'Apply appropriate fungicide',
                    'Clean up fallen debris'
                ]
            },
            'rust': {
                'name': 'Rust Disease',
                'confidence': 0.88,
                'patterns': {
                    'rust_spots': {
                        'hsv_lower': np.array([5, 150, 150]),
                        'hsv_upper': np.array([15, 255, 255]),
                        'min_area': 0.05,
                        'max_area': 0.4,
                        'weight': 0.8
                    },
                    'spores': {
                        'hsv_lower': np.array([10, 100, 100]),
                        'hsv_upper': np.array([20, 255, 255]),
                        'min_area': 0.01,
                        'max_area': 0.2,
                        'weight': 0.2
                    }
                },
                'symptoms': [
                    'Orange or rusty spots on leaves',
                    'Powdery rust-colored spores',
                    'Distorted leaves',
                    'Weakened plant growth'
                ],
                'recommendations': [
                    'Remove infected plant parts',
                    'Avoid wetting leaves',
                    'Increase air circulation',
                    'Apply rust-specific fungicide',
                    'Clean and disinfect tools'
                ]
            },
            'fusarium_wilt': {
                'name': 'Fusarium Wilt',
                'confidence': 0.85,
                'patterns': {},
                'symptoms': [
                    'Yellowing of leaves',
                    'Wilting',
                    'Stunted growth',
                    'Browning of vascular tissue'
                ],
                'recommendations': [
                    'Remove infected plants',
                    'Improve soil drainage',
                    'Rotate crops'
                ]
            },
            'bacterial_blight': {
                'name': 'Bacterial Blight',
                'confidence': 0.80,
                'patterns': {},
                'symptoms': [
                    'Water-soaked spots on leaves',
                    'Yellowing',
                    'Leaf drop',
                    'Dark streaks on stems'
                ],
                'recommendations': [
                    'Remove infected leaves',
                    'Avoid overhead watering',
                    'Use resistant varieties'
                ]
            },
            'anthracnose': {
                'name': 'Anthracnose',
                'confidence': 0.82,
                'patterns': {},
                'symptoms': [
                    'Dark, sunken lesions on leaves',
                    'Leaf drop',
                    'Stem cankers'
                ],
                'recommendations': [
                    'Remove infected plant parts',
                    'Improve air circulation',
                    'Apply fungicide'
                ]
            },
            'downy_mildew': {
                'name': 'Downy Mildew',
                'confidence': 0.78,
                'patterns': {},
                'symptoms': [
                    'Yellow patches on upper leaf surfaces',
                    'White mold on the underside',
                    'Stunted growth'
                ],
                'recommendations': [
                    'Improve air circulation',
                    'Avoid overhead watering',
                    'Apply fungicide'
                ]
            },
            'healthy': {
                'name': 'Healthy',
                'confidence': 0.95,
                'patterns': {
                    'healthy_green': {
                        'hsv_lower': np.array([35, 50, 50]),
                        'hsv_upper': np.array([85, 255, 255]),
                        'min_area': 0.6,
                        'max_area': 1.0,
                        'weight': 1.0
                    }
                },
                'symptoms': [],
                'recommendations': [
                    'Continue regular watering schedule',
                    'Maintain good air circulation',
                    'Monitor for any changes',
                    'Fertilize as needed',
                    'Regular inspection for early detection'
                ]
            }
        }

    def detect_patterns(self, img, disease_patterns):
        """Detect disease patterns in the image using HSV color space."""
        try:
            # Convert to HSV
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            height, width = img.shape[:2]
            total_pixels = height * width
            
            pattern_scores = {}
            for pattern_name, pattern_info in disease_patterns.items():
                # Create mask for the pattern
                mask = cv2.inRange(hsv, pattern_info['hsv_lower'], pattern_info['hsv_upper'])
                
                # Calculate area percentage
                pattern_pixels = cv2.countNonZero(mask)
                area_percentage = pattern_pixels / total_pixels
                
                # Calculate pattern score based on area and weight
                if area_percentage >= pattern_info['min_area'] and area_percentage <= pattern_info['max_area']:
                    score = area_percentage * pattern_info['weight']
                    pattern_scores[pattern_name] = score
                
            return pattern_scores
            
        except Exception as e:
            logger.error(f"Error detecting patterns: {str(e)}")
            return {}

    def analyze_image(self, image_path):
        """Analyze image to detect disease patterns."""
        try:
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return None

            # Read image
            img = cv2.imread(image_path)
            if img is None:
                logger.error("Failed to read image")
                return None

            # Calculate disease scores
            disease_scores = {}
            for disease_key, disease_info in self.diseases.items():
                # Detect patterns for this disease
                pattern_scores = self.detect_patterns(img, disease_info['patterns'])
                
                if pattern_scores:
                    # Calculate weighted average of pattern scores
                    total_weight = sum(disease_info['patterns'][p]['weight'] for p in pattern_scores.keys())
                    disease_score = sum(score for score in pattern_scores.values()) / total_weight
                    disease_scores[disease_key] = disease_score

            # Determine the disease
            if not disease_scores:
                return 'healthy'

            # Get the disease with highest score
            max_disease = max(disease_scores.items(), key=lambda x: x[1])[0]
            max_score = disease_scores[max_disease]

            # If the highest score is too low, consider it healthy
            if max_score < 0.15 and max_disease != 'healthy':
                return 'healthy'

            # If it's detected as healthy but other diseases have significant scores, pick the highest scoring disease
            if max_disease == 'healthy' and len(disease_scores) > 1:
                other_scores = {k: v for k, v in disease_scores.items() if k != 'healthy'}
                if any(score > 0.2 for score in other_scores.values()):
                    max_disease = max(other_scores.items(), key=lambda x: x[1])[0]

            return max_disease

        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
            return None

    def predict_disease(self, image_path):
        """Analyze plant image and predict disease."""
        try:
            logger.info(f"Analyzing image: {image_path}")
            
            # Analyze image and get diagnosis
            diagnosis = self.analyze_image(image_path)
            if not diagnosis:
                return None

            # Get disease details
            disease_info = self.diseases.get(diagnosis)
            if not disease_info:
                return None

            return {
                'status': disease_info['name'],
                'confidence': disease_info['confidence'],
                'symptoms': disease_info['symptoms']
            }

        except Exception as e:
            logger.error(f"Error in disease prediction: {str(e)}")
            return None

    def get_care_recommendations(self, diagnosis):
        """Get care recommendations based on diagnosis."""
        try:
            if not diagnosis:
                return None

            # Get disease key from status
            disease_key = 'healthy'
            for key, info in self.diseases.items():
                if info['name'] == diagnosis['status']:
                    disease_key = key
                    break

            # Return recommendations for the disease
            return self.diseases[disease_key]['recommendations']

        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            return None

# Initialize the model
model = PlantDiseaseModel()
