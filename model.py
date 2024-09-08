import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('stopwords')
nltk.download('wordnet')

data = {
    'text': [
        "Brush my teeth in the morning",
        "Take a nice bath to feel refresh and clean",
        "Finish the report for work",
        "Buy groceries for the week",
        "Plan the project meeting with the client",
        "Clean the entire house before guests arrive",
        "Call the client to confirm details",
        "Go for a relaxing walk in the park",
        "Prepare presentation slides for the conference",
        "Complete homework daily given by the teachers of each and every subject",
        "Dinner with family at 7 PM",
        "Workout at the gym for at least an hour",
        "Email the project updates to the manager",
        "Book doctor appointment for daily, monthly or yearly check-up",
        "Set up a team meeting for the new project",
        "Meditate in the morning for 10 minutes or however time it will suit me",
        "Write the code for the new feature",
        "Pay the electricity bill of the house",
        "Research the competitors' products",
        "Visit the grocery store for weekly shopping",
        "Review the design documents with the team",
        "Read a book for leisure"
    ],
    'category': [
        'Personal', 'Personal', 'Work', 'Personal', 'Work', 'Personal',
        'Work', 'Personal', 'Work', 'Work', 'Personal', 'Personal', 'Work',
        'Personal', 'Work', 'Personal', 'Work', 'Personal', 'Work', 'Personal',
        'Work', 'Personal'
    ]
}

df = pd.DataFrame(data)


def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z]", "", text)
    text = text.lower()
    words = text.split()

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)


df['text'] = df['text'].apply(preprocess_text)

label_encoder = LabelEncoder()
df['category'] = label_encoder.fit_transform(df['category'])

x_train, x_test, y_train, y_test = train_test_split(df['text'], df['category'], test_size=0.2, random_state=42)

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])

param_grid = {
    'tfidf__max_df': [0.7, 0.8, 0.9],
    'tfidf__min_df': [1, 2, 3],
    'tfidf__ngram_range': [(1, 1), (1, 2)],
    'classifier__alpha': [0.1, 0.5, 1.0]
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(x_train, y_train)

best_model = grid_search.best_estimator_
best_model.fit(x_train, y_train)


predictions = best_model.predict(x_test)
print(f"Model Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")
print(classification_report(y_test, predictions, target_names=label_encoder.classes_))


def categorize_task(task_text):
    processed_text = preprocess_text(task_text)
    prediction = best_model.predict([processed_text])[0]
    return label_encoder.inverse_transform([prediction])[0]


related_words = {
    'report': ['document', 'summary', 'analysis'],
    'buy': ['purchase', 'acquire', 'get'],
    'plan': ['schedule', 'organize', 'arrange'],
    'clean': ['tidy', 'wash', 'sanitize'],
    'call': ['contact', 'ring', 'reach out'],
    'walk': ['stroll', 'jog', 'hike', 'run'],
    'prepare': ['arrange', 'organize', 'get ready'],
    'complete': ['finish', 'accomplish', 'wrap up'],
    'dinner': ['meal', 'supper', 'feast'],
    'workout': ['exercise', 'train', 'practice'],
    'email': ['send', 'message', 'notify'],
    'book': ['reserve', 'schedule', 'arrange'],
    'set': ['arrange', 'prepare', 'organize'],
    'meditate': ['relax', 'focus', 'calm'],
    'write': ['compose', 'draft', 'author'],
    'pay': ['settle', 'discharge', 'clear'],
    'research': ['investigate', 'study', 'explore'],
    'visit': ['go to', 'travel', 'see', 'adventure'],
    'review': ['examine', 'check', 'inspect'],
    'read': ['peruse', 'browse', 'scan']
}


def get_related_words(input_text):
    input_words = input_text.split()
    suggestions = []
    for word in input_words:
        if word in related_words:
            suggestions.extend(related_words[word])

    return suggestions
