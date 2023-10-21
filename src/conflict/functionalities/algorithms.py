from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
# import spacy
import nltk
from nltk.corpus import wordnet
import ast

# nlp = spacy.load("en_core_web_sm")
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

# def extractPosTokens(sentence):
#     # Tokenize the sentence into words
#     words = nltk.word_tokenize(sentence)

#     # Use nltk.pos_tag to get the part of speech for each word
#     pos_tags = nltk.pos_tag(words)

#     word_objects = {"noun": [], "verb": [], "adjective": []}

#     # Categorize words based on their part of speech
#     for word, pos in pos_tags:
#         if pos.startswith('N'):  # Nouns
#             word_objects["noun"].append(word)
#         elif pos.startswith('V'):  # Verbs
#             word_objects["verb"].append(word)
#         elif pos.startswith('J'):  # Adjectives
#             word_objects["adjective"].append(word)
#     return word_objects

def calculatePosOverlapRatio(r1_pos, r2_pos):
    overlap_counts = {}
    maxPosOR = 0.00
    for pos in ["noun", "verb", "adjective"]:
        # print(r1_pos[pos], r2_pos[pos])
        overlap_counts[pos] = len(set(r1_pos[pos]) & set(r2_pos[pos])) / (1e-20+max(r1_pos[pos].__len__(), r2_pos[pos].__len__()))
        maxPosOR = max(maxPosOR, overlap_counts[pos])
    # print(overlap_counts)
    # print(maxPosOR)
    return round(maxPosOR, 3)

def calculateOppositeOverlapCount(r1:str, r2:str):
    # Tokenize the sentences into words
    words1 = nltk.word_tokenize(r1)
    words2 = nltk.word_tokenize(r2)

    # Create sets of words from the sentences
    word_set1 = set(words1)
    word_set2 = set(words2)

    # Find antonyms for each word in the first sentence
    antonyms = []

    for word in word_set1:
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.antonyms():
                    antonyms.append(lemma.antonyms()[0].name())

    # Find common antonyms between the two sentences
    common_antonyms = word_set2.intersection(set(antonyms))
    print(common_antonyms)
    return len(common_antonyms)

def determine(conflicts):
    for i in range(len(conflicts)):
        if conflicts[i]["cos"]>=0.3:
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
            oppositeOC = 0
            if cosr1r2 >= 0.3:
                posOR = calculatePosOverlapRatio(ast.literal_eval(req1["word_objects"]), ast.literal_eval(req2["word_objects"]))
                oppositeOC = calculateOppositeOverlapCount(req1["content"], req2["content"])
            
            conflict = {
                "req1_document_id": str(req1["document_id"]),
                "req2_document_id": str(req2["document_id"]),
                "project_id": str(req1["project_id"]),
                "req1_id": str(req1["id"]),
                "req2_id": str(req2["id"]),
                "req1_content": str(req1["content"]),
                "req2_content": str(req2["content"]),
                'cos': cosr1r2,
                'pos_overlap_ratio': posOR,
                'opposite_overlap_count': oppositeOC
            }

            conflicts.append(conflict)
    
    conflicts = determine(conflicts)
    return conflicts