# todo 尝试找到语料中最为合适的token
# todo BPE 算法的实现过程
import collections
import pandas as pd
import re

text = "There is an 80% chance of rainfall today. We are pretty sure it is going to rain."
words = text.strip().split(" ")
print(f"Vocabulary size: {len(words)}")

# get the word frequency and add the end of word (</w>) token ## at the end of each word
word_freq_dict = collections.defaultdict(int)
for word in words:
    word_freq_dict[' '.join(word) + ' </w>'] += 1

# Split the word into characters and then calculate the character frequency.
char_freq_dict = collections.defaultdict(int)
for word, freq in word_freq_dict.items():
    chars = word.split()
    for char in chars:
        char_freq_dict[char] += freq

df = pd.DataFrame(char_freq_dict, index=[0]).T
df = df.rename(columns={0: 'Count'})

# create all possible consecutive pairs
pairs = collections.defaultdict(int)
for word, freq in word_freq_dict.items():
    chars = word.split()
    for i in range(len(chars) - 1):
        pairs[chars[i], chars[i + 1]] += freq

max(pairs, key=pairs.get)

word_freq_dict = collections.defaultdict(int)
for word in words:
    word_freq_dict[' '.join(word) + ' </w>'] += 1


#  find the best pair
def get_pairs(word_freq_dict):
    pairs = collections.defaultdict(int)
    for word, freq in word_freq_dict.items():
        chars = word.split()
        for i in range(len(chars) - 1):
            pairs[chars[i], chars[i + 1]] += freq
    return pairs


def merge_byte_pairs(best_pair, word_freq_dict):
    print(best_pair)
    merged_dict = {}
    bigram = re.escape(' '.join(best_pair))
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in word_freq_dict:
        # print(word)
        w_out = p.sub(''.join(best_pair), word)
        merged_dict[w_out] = word_freq_dict[word]
    return merged_dict


def get_subword_tokens(word_freq_dict):
    char_freq_dict = collections.defaultdict(int)
    for word, freq in word_freq_dict.items():
        chars = word.split()
        for char in chars:
            char_freq_dict[char] += freq
    return char_freq_dict


for i in range(100):
    pairs = get_pairs(word_freq_dict)
    best_pair = max(pairs, key=pairs.get)
    print(f"Iteration {i}: ")
    word_freq_dict = merge_byte_pairs(best_pair, word_freq_dict)
    # print(word_freq_dict)
    subword_tokens = get_subword_tokens(word_freq_dict)
    print(subword_tokens)
    print(len(subword_tokens))
    print("--------")
