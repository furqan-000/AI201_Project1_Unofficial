## Domain
I picked UIC Computer Science professor reviews. I chose this because when I was trying to pick classes I had no idea which professors were good or bad. The university website just gives you a name and a course number, it doesn't tell you anything useful. Students share the real info on Rate My Professors but you can't search across multiple professors at once easily. I wanted to make something that lets you just ask a question and get an answer based on what students actually said.

## Documents
1. documents/prof_ayala_cs.txt - reviews for Daniel Ayala from Rate My Professors
2. documents/prof_bello_cs.txt - reviews for Gonzalo Bello Lander from Rate My Professors
3. documents/prof_gu_cs.txt - reviews for Zhaochen Gu from Rate My Professors
4. documents/prof_katok_cs.txt - reviews for Zoa Katok from Rate My Professors
5. documents/prof_kshemkalyani_cs.txt - reviews for Ajay Kshemkalyani from Rate My Professors
6. documents/prof_maratos_cs.txt - reviews for George Maratos from Rate My Professors
7. documents/prof_raizi_cs.txt - reviews for Sara Raizi from Rate My Professors
8. documents/prof_tang_cs.txt - reviews for Wei Tang from Rate My Professors
9. documents/prof_theys_cs.txt - reviews for Mitchell Theys from Rate My Professors
10. documents/prof_verschelde_cs.txt - reviews for Jan Verschelde from Rate My Professors

## Chunking Strategy
Chunk size: 300 words
Overlap: 50 words

I went with 300 words because the reviews are pretty short, like a few sentences each. I wanted each chunk to have at least one or two full reviews in it so the meaning doesn't get cut off. If I made chunks too small like 50 words it would just be fragments that don't make sense on their own. The 50 word overlap is so that if a review gets split between two chunks, the important part still shows up in one of them. I tested it and got 13 chunks total across 10 documents which felt reasonable.

## Retrieval Approach
I used all-MiniLM-L6-v2 from sentence-transformers because the project recommended it and it runs locally without needing an API key. I retrieve the top 4 chunks per query. The way it works is it turns the question and all the chunks into vectors and finds the ones that are most similar. So even if the question uses different words than the review it can still find the right one.

If I was doing this for real users I would think about using something like OpenAIs embedding model because it might be more accurate, but it costs money per request. I would also think about how long the text is and whether it supports other languages if the users speak different languages.

## Evaluation Plan
1. Which professor is the easiest to approach? Expected answer: Daniel Ayala based on reviews saying he is very chill and easy to talk to.
2. Which professor should I avoid? Expected answer: Mitchell Theys or Zhaochen Gu based on the really negative reviews.
3. Does Professor Maratos curve his exams? Expected answer: Yes based on a review that mentions curved challenging aspects.
4. Which professor is better for CS 151? Expected answer: Zoa Katok based on a review that says she is the better CS 151 professor.
5. What do students think about Professor Bello's lectures? Expected answer: Students say lectures are really clear and detailed, multiple people gave 5 stars.

## Anticipated Challenges
1. Some reviews are really short like one sentence and might get grouped with a different professors review in the same chunk which could confuse the answer.
2. If someone asks about a professor using a nickname or spells the name wrong the system probably won't find the right reviews.

## AI Tool Plan
1. ingest.py: I gave Claude my chunking strategy and document list and asked it to write the code to load and chunk the files.
2. embed.py: I gave Claude the retrieval section and asked it to write the embedding and ChromaDB storage code.
3. query.py: I told Claude I needed grounded answers only from the documents with source citations and it wrote the prompt and retrieval function.
4. app.py: I gave Claude the Gradio example from the spec and asked it to connect it to my query function.

## Architecture
Document Ingestion (load .txt files)
        ↓
Chunking (300 words, 50 word overlap)
        ↓
Embedding (all-MiniLM-L6-v2)
        ↓
Vector Store (ChromaDB)
        ↓
Retrieval (top 4 chunks)
        ↓
Generation (Groq llama-3.3-70b-versatile)
        ↓
Gradio UI
