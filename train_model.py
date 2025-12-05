from ml_model import MLModel
import pandas as pd

# Create sample training data
data = {
    'text': [
        'python java sql data analysis machine learning',
        'leadership team management project management communication',
        'creative design photoshop illustrator ui ux',
        'accounting finance excel budget analysis',
        'sales marketing customer service communication'
    ],
    'personality': ['Analytical', 'Leadership', 'Creative', 'Detail-oriented', 'Outgoing']
}

df = pd.DataFrame(data)

# Train model
ml = MLModel()
ml.train_model(df)
print("Model trained and saved!")