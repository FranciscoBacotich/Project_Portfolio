# Analysis

## Layer 2, Head 5 Analysis:  "We turned down a narrow lane and passed through a small [MASK]."

It appears that in this layer, the model is focusing on words surrounding the token. The attention scores are higher for previous words. This may suggest that the model is capturing syntactic structure or relationships between words. Lets try with different sentences.

1. **Sentence 1:**
   - "The detective carefully examined the [MASK] for any potential clues."
     - Observation: The model shows a focus on words surrounding the [MASK] token and the beginning of the sentence. This aligns with a potential syntactic or contextual understanding.

2. **Sentence 2:**
   - "A delicious smell wafted from the [MASK]."
     - Observation: Attention scores are elevated for the first three words, and as the sentence advances, the focus on the previous word becomes more noticeable. This indicates that the attention head is sensitive to the initial context of the sentence.


## Layer 3, Head 2 : "The professor carefully reviewed the [MASK]."

In this layer, a notable connection is observed between the words "carefully" and "reviewed," suggesting a relationship between an adverb and the verb it modifies. For this particular attention head, the model places more emphasis on the words that precede the token being masked.

### Example Sentences:

1. **Sentence 1:**
   - "She quickly completed the [MASK]."
     - Observation: The attention head underscores the relationship between the adverb "quickly" and the verb "completed."

2. **Sentence 2:**
   - "He silently entered the [MASK]."
     - Observation: The attention scores show a slight connection between the adverb "silently" and the verb "entered". Additionally, there's small but noticeable attention on the first word "He" and its relation with "silently". It suggests that the model is paying attention to the manner or way in which the subject performs the action

