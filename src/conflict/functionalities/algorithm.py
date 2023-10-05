from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

nlp = spacy.load("en_core_web_sm")
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

def extractPosTokens(sentence):
    doc = nlp(sentence)
    # Initialize empty dictionaries for each part of speech
    word_objects = {"noun": [], "verb": [], "adjective": []}
    # Iterate through the tokens in the sentence and categorize them
    for token in doc:
        if token.pos_ == "NOUN":
            word_objects["noun"].append(token.text)
        elif token.pos_ == "VERB":
            word_objects["verb"].append(token.text)
        elif token.pos_ == "ADJ":
            word_objects["adjective"].append(token.text)
    # Print the word objects
    print(word_objects)
    return word_objects

def calculatePosOverlapRatio(r1:str, r2:str):
    r1_pos = extractPosTokens(r1)
    r2_pos = extractPosTokens(r2)
    overlap_counts = {}
    maxPosOR = 0.00
    for pos in ["noun", "verb", "adjective"]:
        print(r1_pos[pos], r2_pos[pos])
        overlap_counts[pos] = len(set(r1_pos[pos]) & set(r2_pos[pos])) / (1e-20+max(r1_pos[pos].__len__(), r2_pos[pos].__len__()))
        maxPosOR = max(maxPosOR, overlap_counts[pos])
    print(overlap_counts)
    print(maxPosOR)
    return round(maxPosOR, 3)

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

            cosr1r2 = calculateCosSimilarity(req1["content"], req2["content"])
            posOR = 0.0
            if cosr1r2 >= 0.5:
                posOR = calculatePosOverlapRatio(req1["content"], req2["content"])
            
            conflict = {
                "req1_document_id": str(req1["document_id"]),
                "req2_document_id": str(req2["document_id"]),
                "project_id": str(req1["project_id"]),
                "req1_id": str(req1["id"]),
                "req2_id": str(req2["id"]),
                "req1_content": str(req1["content"]),
                "req2_content": str(req2["content"]),
                'cos': cosr1r2,
                'pos_overlap_ratio': posOR
            }

            conflicts.append(conflict)
    
    conflicts = determine(conflicts)
    return conflicts