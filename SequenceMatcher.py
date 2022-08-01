#Sequence Matcher in Python

#If you need more advanced matching use Fuzzy Matching algorithm

from difflib import SequenceMatcher

#text1 = input("Enter 1st Sentence: ")
#text2 = input("Enter 2nd Sentence: ")

text1 ="INV4567890"
text2 ="INV4-67890"
sequenceScore = SequenceMatcher(None, text1, text2).ratio()
print(f"Both are {sequenceScore * 100} % similar")

