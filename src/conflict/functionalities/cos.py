from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer()


def insertin(conflictings, toinsert):
    # Check if any of the numbers in the new_set exist in any of the sets in the array
    combined_sets = []
    for existing_set in conflictings:
        if any(num in existing_set for num in toinsert):
            combined_sets.append(existing_set)
    
    # If there are two or more sets to combine, create a union of them
    if len(combined_sets) >= 1:
        combined_union = set(toinsert)
        for existing_set in combined_sets:
            combined_union |= existing_set
        
        # Remove the combined sets from the array
        conflictings = [s for s in conflictings if s not in combined_sets]
        
        # Append the combined union set to the array
        conflictings.append(combined_union)
    else:
        conflictings.append(set(toinsert))

    print("Hi",toinsert,conflictings)
    return conflictings

def findstatus_intrasrs(srsdf):
    srs_count = len(srsdf)
    tfidf_matrix = tfidf.fit_transform(srsdf)
    cosine_sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    conflictings = []

    for i in range(srs_count):
        for j in range(srs_count):
            if(cosine_sim_matrix[i][j]>0.5):
                if(i!=j):
                    conflictings = insertin(conflictings, set((i,j)))
    # print(cosine_sim_matrix)
    # print(conflictings)

    ret = [[]]
    
    for c in conflictings:
        c = list(c)
        ret.append(c)
    return ret