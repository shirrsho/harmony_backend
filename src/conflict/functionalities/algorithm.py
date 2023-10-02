from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer()

def calculateCosSimilarity(r1:str, r2:str):
    if r1.__len__()==0 or r2.__len__()==0:
        return 0.0
    # Tokenize and preprocess the sentences
    sentences = [r1, r2]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

    # Calculate the cosine similarity
    cos_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1]).__float__()

    return round(cos_score, 3)

def determine(conflicts):
    for i in range(len(conflicts)):
        if conflicts[i]["cos"]>=0.5:
            conflicts[i]["decision"] = "Yes"
        else: conflicts[i]["decision"] = "No"

    return conflicts

def findConflicts(requirements:any):
    conflicts = []
    
    for i in range(len(requirements)):
        for j in range(i + 1, len(requirements)):
            req1 = requirements[i]
            req2 = requirements[j]
            
            conflict = {
                "req1_document_id": str(req1["document_id"]),
                "req2_document_id": str(req2["document_id"]),
                "project_id": str(req1["project_id"]),
                "req1_id": str(req1["id"]),
                "req2_id": str(req2["id"]),
                "req1_content": str(req1["content"]),
                "req2_content": str(req2["content"]),
                'cos':calculateCosSimilarity(req1["content"], req2["content"]),
            }

            conflicts.append(conflict)
    
    conflicts = determine(conflicts)
    return conflicts