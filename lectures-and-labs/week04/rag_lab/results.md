# RAG Lab - results

**Name:** _[Your name]_
**Date:** _[Date]_

Fill this in as you go. The README says what each section is for.

---

## Part 1: chunking and embeddings (DIY 1 and 2)

- Documents loaded: ___
- Chunks produced at 200 words: ___ (shortest ___ words, longest ___ words)
- Vector dimensionality: ___
- Did the query vector have the same dimensionality as the chunks? ___

_What did the overlap check show?_

---

## Part 2: retrieval (DIY 3 and 4)

**"what is a variable"** - top hit, score and source: ___

**"how can my code remember a number for later"** - top hit, score and source: ___

_Same meaning, different words: did both queries find the same chunk?_

**"how do I bake sourdough"** - what came back, and with what scores: ___

_One sentence on what a retrieval system does when nothing is relevant:_

---

## Part 3: grounding (DIY 5)

**Q:** What is a variable?
**A:** ___
**Source it cited:** ___

**Q:** How do I bake sourdough?
**A:** ___ (did it decline?)

---

## Part 4: chunk size (DIY 6)

| Chunk size | Index chunks | Variable / paraphrase / sourdough: top-3 similarity scores | Right chunk? | Noise in returned context |
|------------|--------------|-------------------------------------------------------------|--------------|---------------------------|
| 50 words   | 66           | 0.58/0.57/0.42; 0.45/0.41/0.41; 0.13/0.12/0.09             | Yes, for both variable questions | Lowest; the variable hits are short and all from the programming document. Sourdough returns unrelated hits, all below 0.20. |
| 200 words  | 14           | 0.42/0.21/0.21; 0.31/0.20/0.13; 0.09/0.09/0.05             | Yes, for both variable questions | More unrelated material in the top three: a functions chunk and database chunks appear with the variable results. Sourdough hits are unrelated and below 0.20. |
| 800 words  | 5            | 0.42/0.21/0.12; 0.31/0.13/0.11; 0.09/0.09/0.04             | Yes, for both variable questions | Highest; each hit is a large section of a document, so relevant passages arrive with more unrelated text. Sourdough hits are unrelated and below 0.20. |

For the variable query, Part 3's assembled top-three context estimate rose
from ~261 tokens at 50 words to ~321 at 200 and ~463 at 800; the
similarity-threshold check kept 3/3, 3/3 and 2/3 hits respectively.

At 50 words, small fragments can lose the surrounding explanation; at 800
words, the answer is buried in a much larger chunk with unrelated material.

---

## Part 5: long context versus retrieval (DIY 7)

```text
Whole corpus size: ................. [approx tokens]
Question asked: .................... [your question]
  RAG answer: ...................... [response]
  Whole-corpus answer: ............. [response]
Which was better? .................. [RAG / long context / no difference]
At what corpus size would this flip? [your reasoning]
```

Repeat for each of the three questions if the answers differed.

### Recorded comparison

Whole corpus: **5 documents, 1,970 words, approximately 2,626 tokens**
(words / 0.75). The RAG index used for this run contained 66 chunks of up
to 50 words each.

**Q: What is a variable?**

- RAG: A variable is like a labeled box that stores information
  `[source: introduction_to_programming.txt]`.
- Whole corpus: A variable is like a labeled box that stores information
  `[source: introduction_to_programming.txt]`.
- Comparison: No difference; both gave the same correct answer and citation.

**Q: How do linked lists work?**

- RAG: A linked list is a linear data structure whose nodes contain data
  and links to the next node; singly linked lists point forward, while
  doubly linked lists point forward and backward
  `[source: data_structures_basics.txt]`.
- Whole corpus: Gave the same explanation, and added that linked lists
  make insertions and deletions efficient because pointers are updated
  instead of shifting array elements
  `[source: data_structures_basics.txt]`.
- Comparison: Whole-corpus context gave a more detailed answer, with the
  same correct source.

**Q: What is HTML?**

- RAG: HTML provides the structure and content of web pages using tags
  such as headings, paragraphs, links and images; it is the skeleton that
  everything else builds on `[source: web_development_intro.txt]`.
- Whole corpus: HTML provides the structure and content of web pages
  `[source: web_development_intro.txt]`.
- Comparison: Both were correct and cited the same source; RAG was more
  detailed.

On this small corpus, neither approach consistently wins: both answered
all three questions correctly with citations, while the amount of detail
varied. This comparison may change once the corpus is large enough that
including all documents exceeds the model's useful context budget or
becomes more costly and noisy than retrieving a small relevant subset.

**The question the corpus cannot answer** (sourdough):

- No context: ___
- Whole corpus: ___
- RAG: ___

_Which of the three declined, and what made the difference?_

---

## Reflection

_When would you build retrieval, and when would you just paste everything?_

_What surprised you?_
