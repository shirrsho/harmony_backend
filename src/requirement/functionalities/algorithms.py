import nltk

def extractPosTokens(sentence):
    # Tokenize the sentence into words
    words = nltk.word_tokenize(sentence)

    # Use nltk.pos_tag to get the part of speech for each word
    pos_tags = nltk.pos_tag(words)

    word_objects = {"noun": [], "verb": [], "adjective": []}

    # Categorize words based on their part of speech
    for word, pos in pos_tags:
        if pos.startswith('N'):  # Nouns
            word_objects["noun"].append(word)
        elif pos.startswith('V'):  # Verbs
            word_objects["verb"].append(word)
        elif pos.startswith('J'):  # Adjectives
            word_objects["adjective"].append(word)
    return word_objects