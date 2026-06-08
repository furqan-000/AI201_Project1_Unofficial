# UIC Unofficial Professor Guide

A RAG system that lets you ask plain language questions about UIC Computer Science professors and get answers based on real student reviews.

## Domain

I chose UIC Computer Science professor reviews as my domain. When I was trying to pick classes I had no idea which professors were actually good. The university website just gives you a name and a course number, nothing useful. Students post the real stuff on Rate My Professors but you cant search across multiple professors at once. I wanted to build something where you just type a question and get an answer pulled from what students actually wrote.

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Daniel Ayala reviews | Rate My Professors | documents/prof_ayala_cs.txt |
| 2 | Gonzalo Bello Lander reviews | Rate My Professors | documents/prof_bello_cs.txt |
| 3 | Zhaochen Gu reviews | Rate My Professors | documents/prof_gu_cs.txt |
| 4 | Zoa Katok reviews | Rate My Professors | documents/prof_katok_cs.txt |
| 5 | Ajay Kshemkalyani reviews | Rate My Professors | documents/prof_kshemkalyani_cs.txt |
| 6 | George Maratos reviews | Rate My Professors | documents/prof_maratos_cs.txt |
| 7 | Sara Raizi reviews | Rate My Professors | documents/prof_raizi_cs.txt |
| 8 | Wei Tang reviews | Rate My Professors | documents/prof_tang_cs.txt |
| 9 | Mitchell Theys reviews | Rate My Professors | documents/prof_theys_cs.txt |
| 10 | Jan Verschelde reviews | Rate My Professors | documents/prof_verschelde_cs.txt |

## Chunking Strategy

Chunk size: 300 words
Overlap: 50 words
Final chunk count: 13

I decided on 300 words after reading through the documents first. The reviews are short, usually just a few sentences each, so I needed chunks big enough to hold at least one or two complete reviews so the meaning doesnt get cut off. I tried thinking about what would happen if I went smaller like 50 words and realized it would just be random fragments that dont make sense on their own. The 50 word overlap is there so if a review happens to fall right on a chunk boundary the important part still shows up fully in one of them.

## Sample Chunks

Chunk 1 (prof_ayala_cs.txt):
"Professor: Daniel Ayala Department: Computer Science University: University of Illinois Chicago Review 1: I took this class twice, I find his project assignment method difficult. It feels unreasonably difficult. Rating: 2/5 Review 2: 251 was a challenging class, but it never was an unfair class..."

Chunk 2 (prof_bello_cs.txt):
"Professor: Gonzalo Bello Lander Department: Computer Science University: University of Illinois Chicago Review 1: Professor Bello is top tier. Run don't walk to enroll in his lectures, seats fill up quickly!..."

Chunk 3 (prof_theys_cs.txt):
"Professor: Mitchell Theys Department: Computer Science University: University of Illinois Chicago Review 1: Some people age into wisdom. Others age into HR training opportunities. Rating: 1/5..."

Chunk 4 (prof_maratos_cs.txt):
"Professor: George Maratos Department: Computer Science University: University of Illinois Chicago Review 1: Genuinely the best professor I've ever had by miles. Probably the best at UIC. Rating: 5/5..."

Chunk 5 (prof_katok_cs.txt):
"Professor: Zoa Katok Department: Computer Science University: University of Illinois Chicago Review 1: Chill Professor, Lecture and Test Heavy Rating: 4/5 Review 2: This professor was very nice and ensured students understood the material..."

## Embedding Model

Model used: all-MiniLM-L6-v2 via sentence-transformers

I picked this one because it runs completely locally, no API key needed and no rate limits. It turns text into vectors so the system can match a question to relevant chunks even when the exact words are different.

If I was building this for real users I would think about a few tradeoffs. Something like OpenAIs embedding model would probably be more accurate but it costs money for every request. I would also think about whether the model handles non English text if the users speak different languages, and how fast it responds if a lot of people are using it at the same time.

## Grounded Generation

The system prompt I wrote tells the model to only answer from the documents provided and to say it doesnt have enough information if the answer isnt there. I specifically wrote it this way so the model cant just make something up from its general knowledge. Every response also shows which source files it pulled from so you can see exactly where the answer came from.

## Retrieval Test Results

Query 1: "Which professor is the easiest to approach?"
Top chunks retrieved from: prof_ayala_cs.txt, prof_katok_cs.txt, prof_bello_cs.txt, prof_theys_cs.txt
The ayala and katok chunks came back because multiple reviews in those files specifically mention approachability and being easy to talk to. Those are the most relevant files for this question.

Query 2: "Which professor should I avoid?"
Top chunks retrieved from: prof_gu_cs.txt, prof_theys_cs.txt, prof_kshemkalyani_cs.txt, prof_verschelde_cs.txt
These came back because they have the most negative reviews. Theys and Gu in particular have reviews that directly say to avoid them.

Query 3: "Does Professor Maratos curve his exams?"
Top chunks retrieved from: prof_maratos_cs.txt, prof_raizi_cs.txt, prof_theys_cs.txt, prof_ayala_cs.txt
The maratos chunk was the most relevant and had a direct answer about curving.

## Example Responses

Response 1 - Question: "Which professor is better for CS 151?"
Answer: According to the reviews, Professor Zoa Katok (Source: prof_katok_cs.txt) is considered better for CS 151. Review 4 states "By far the better CS 151 professor between the two." Her lectures are described as clear, organized, and easy to follow.
Sources: prof_katok_cs.txt, prof_maratos_cs.txt, prof_verschelde_cs.txt, prof_theys_cs.txt

Response 2 - Question: "What do students think about Professor Bello's lectures?"
Answer: Students think highly of Professor Bello's lectures. His lectures are thoroughly detailed and he is always available to help students. Reviews describe lectures as clear, engaging, and well-organized.
Sources: prof_bello_cs.txt, prof_gu_cs.txt, prof_kshemkalyani_cs.txt, prof_verschelde_cs.txt

Out-of-scope query: "What is the best restaurant near UIC?"
Answer: I don't have enough information on that. The provided documents only contain reviews of UIC professors and do not mention restaurants near UIC.

## Query Interface

I built the interface using Gradio. You run it with python app.py and go to http://localhost:7860. There is a text box where you type your question, an Ask button, an Answer box that shows the response with source citations, and a Retrieved from box that shows which files were used to generate the answer.

Sample interaction:
Input: "Which professor is the easiest to approach?"
Answer: "According to the reviews, Professor Daniel Ayala (Source: prof_ayala_cs.txt) and Professor Zoa Katok (Source: prof_katok_cs.txt) are both described as easy to approach and supportive during office hours. However, Professor Ayala is consistently described as very chill, very sweet, and easy to talk to in multiple reviews, making him the easiest to approach."
Retrieved from: prof_ayala_cs.txt, prof_katok_cs.txt, prof_bello_cs.txt, prof_theys_cs.txt

## Evaluation Report

| # | Question | Expected Answer | System Response | Retrieval Quality | Response Accuracy |
|---|----------|----------------|-----------------|-------------------|-------------------|
| 1 | Which professor is the easiest to approach? | Daniel Ayala or Zoa Katok | Identified both, concluded Ayala is easiest based on multiple reviews | Relevant | Accurate |
| 2 | Which professor should I avoid? | Mitchell Theys or Zhaochen Gu | Correctly identified Theys and Gu with specific quotes | Relevant | Accurate |
| 3 | Does Professor Maratos curve his exams? | Yes | Yes, cited Review 2 from prof_maratos_cs.txt | Relevant | Accurate |
| 4 | Which professor is better for CS 151? | Zoa Katok | Correctly identified Katok and cited the specific review | Relevant | Accurate |
| 5 | What do students think about Professor Bello's lectures? | Very positive | Correctly summarized with citations but pulled in off-topic chunks | Partially relevant | Accurate |

## Failure Case Analysis

Question that failed: "What do students think about Professor Bello's lectures?"

What the system returned: The answer was correct but the retrieved chunks included files from Gu, Kshemkalyani, and Verschelde which have nothing to do with Bello.

Root cause: All the documents use similar language like professor, lectures, students, class. Because of this the embedding model cant always tell the difference between chunks from different professors. The chunks are large enough that they all look somewhat similar in vector space, so unrelated professor files get pulled in alongside the right one.

What I would change: I would add professor name as a metadata filter so queries about a specific professor only pull chunks from that professors file. That would fix this retrieval problem completely.

## Spec Reflection

One way the spec helped: Writing the chunking strategy in planning.md before I wrote any code forced me to actually think about chunk size instead of just picking something random. Because I read the documents first I knew the reviews were short and made a better decision about chunk size.

One way implementation diverged from the spec: The spec talked about cleaning HTML and navigation text from scraped pages. Since I collected the documents manually as plain text there was no HTML to clean so that whole step ended up being unnecessary for my pipeline.

## AI Usage

Instance 1:
I was stuck on how the ChromaDB storage was supposed to work so I looked it up and asked Claude to explain how the add method works and what the metadatas parameter does. It explained it and I used that understanding to write the storage part of embed.py myself.

Instance 2:
I wasnt sure what a good system prompt for grounding looks like so I asked Claude for an example of a prompt that forces a model to only answer from provided documents. It gave me a few options and I picked the one that made the most sense and rewrote it in my own words for my query.py file.
