import json
import random
import difflib

# Initialize an empty word database if it doesn't exist
def initialize_word_db():
    word_db = {
        "nouns": [],
        "verbs": [],
        "adjectives": [],
        "adverbs": [],
        "conjunctions": [],
        "sentence_patterns": [],
        "context_history": []
    }
    with open("WDb.json", "w") as file:
        json.dump(word_db, file, indent=4)

def load_word_db():
    try:
        with open("WDb.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        initialize_word_db()
        return load_word_db()

word_db = load_word_db()

# Classify words into categories
def classify_word(word):
    if word.endswith('ing') or word.endswith('ed'):
        return 'verb'
    elif word.endswith('ly'):
        return 'adverb'
    elif word in ['and', 'but', 'or', 'because']:
        return 'conjunction'
    elif word[0].isupper():
        return 'noun'
    else:
        return 'adjective'

# Store new words in the database
def update_word_db(word):
    global word_db
    word_type = classify_word(word)
    if word not in word_db[word_type + 's']:
        word_db[word_type + 's'].append(word)
    with open("WDb.json", "w") as file:
        json.dump(word_db, file, indent=4)

# Identify keywords for improved response matching
def extract_keywords(sentence):
    keywords = []
    for word in sentence.split():
        word_type = classify_word(word)
        if word_type in ['noun', 'verb', 'adjective']:
            keywords.append(word)
    return keywords

# Match the input to the most relevant past conversation
def find_best_match(keywords):
    best_match = None
    highest_score = 0

    for entry in word_db['context_history']:
        context_keywords = entry['context']
        score = len(set(keywords) & set(context_keywords))
        if score > highest_score:
            highest_score = score
            best_match = entry

    return best_match

# Generate a meaningful response based on past patterns
def generate_sentence(input_sentence):
    keywords = extract_keywords(input_sentence)
    match = find_best_match(keywords)

    if match:
        # Generate a response based on the past context
        response = f"I remember we talked about {', '.join(match['context'])}. Could you share more about that?"
    else:
        response = "That's interesting! What else can we talk about?"
    
    # Add randomness to responses for more dynamic interaction
    if random.random() > 0.7:
        response += " How about you tell me a bit more about something else?"

    return response

def classify_and_update_sentence(text):
    keywords = extract_keywords(text)
    sentence_data = {"structure": text, "context": keywords}
    word_db['context_history'].append(sentence_data)

    with open("WDb.json", "w") as file:
        json.dump(word_db, file, indent=4)

def train_model(inp):
    print("Training Model")
    for sentence in inp:
        classify_and_update_sentence(sentence)
    print("Training completed on all", len(inp), "inputs.")

test_list = training_data = [
    "Hello! How are you feeling today? I hope your day has been going well so far.",
    "I'm doing quite well, thank you! I've been working on a few projects lately. How about you?",
    "Not too bad, thanks for asking. I managed to finish some work earlier, so I'm feeling productive.",
    "What's your name? I'd love to know more about you.",
    "My name is Alex. I'm really passionate about technology and creative projects.",
    "Nice to meet you! I always enjoy connecting with people who share similar interests.",
    "What do you like to do in your free time? Any hobbies or special interests?",
    "I enjoy reading mystery novels, experimenting with new recipes in the kitchen, and sometimes I unwind by playing video games.",
    "What kind of music do you like to listen to when you're relaxing?",
    "I love listening to jazz when I'm reading and rock music when I need some energy. How about you?",
    "What's your favorite food? I'm always on the lookout for new recipes to try.",
    "I really enjoy pizza with extra toppings and homemade pasta. It's hard to beat a good comfort meal.",
    "Where are you from? I'd love to hear about your hometown.",
    "I'm from New York. The city never sleeps, but it's full of life and excitement.",
    "What are you planning to do later today? Any exciting plans?",
    "I'm just relaxing at home and might catch up on some reading or start a new movie.",
    "Do you have any pets? I'd love to hear about them!",
    "Yes, I have a cat named Whiskers. She's always curling up on my keyboard when I'm trying to work.",
    "What shows are you currently watching? Any recommendations?",
    "I'm currently watching a fascinating sci-fi series. The characters are so well-developed!",
    "What's your favorite movie genre? I'm always up for a good film.",
    "I love action comedies! They keep me engaged while giving me a good laugh.",
    "How was your day so far? Did anything interesting happen?",
    "It was great! I managed to finish a big project I've been working on for weeks.",
    "What are you currently working on? I'd love to hear about your projects.",
    "I'm writing some code right now. It's part of a larger project I'm building with friends.",
    "Would you like some help with your project? I'm happy to lend a hand.",
    "Sure! I'd appreciate that. I've been struggling with a few tricky bugs.",
    "Can you explain this concept in simpler terms? I'm trying to understand better.",
    "Absolutely! I'd be happy to break it down step by step for you.",
    "What's the weather like today in your area? I'm debating whether to go for a walk.",
    "It's sunny and warm outside, perfect for a relaxing stroll in the park.",
    "Are you feeling hungry right now? I was thinking about grabbing a snack.",
    "Yeah, I could go for something light like a sandwich or some fruit.",
    "Do you want to play a game? I always enjoy some friendly competition.",
    "Sure, sounds fun! What kind of game do you have in mind?",
    "Let's go for a walk and get some fresh air. It might clear our heads.",
    "That's a great idea! I could use a little exercise and some sunshine.",
    "Can you tell me a funny joke? I could use a good laugh right now.",
    "Why don't skeletons fight each other? Because they don't have the guts!",
    "What's your favorite color, and does it remind you of anything special?",
    "I really like the color blue because it reminds me of clear skies and calm ocean waves.",
    "Are you feeling okay? You seem a bit quieter than usual.",
    "I'm feeling a bit tired but otherwise good. Just need some rest, I think.",
    "What's your main goal for today? Any major tasks you're trying to finish?",
    "I want to finish my project by tonight so I can relax over the weekend.",
    "Do you need any help with your work? I'm always happy to pitch in.",
    "Yes, I'd love some guidance on a tricky coding issue I've been stuck on.",
    "How do you usually make your morning coffee? Any special method you prefer?",
    "I like to use a French press with fresh ground coffee. The aroma is amazing!",
    "What time is it right now? I might need to wrap things up soon.",
    "It's about 3:00 PM. There's still plenty of time to get things done.",
    "Did you watch the game last night? I heard it was really intense!",
    "Yes! The final play was incredible, I couldn't believe how close it was.",
    "What's your dream vacation destination? Somewhere you'd love to visit?",
    "I'd love to visit Japan someday. The culture and scenery seem amazing.",
    "Do you like cooking? I'm always looking for new meal ideas.",
    "I enjoy making pasta dishes and experimenting with new sauces.",
    "Are you busy right now or do you have some free time to chat?",
    "Not really, what's up? I'm always happy to catch up.",
    "Do you believe in aliens? I've been watching some interesting documentaries.",
    "I think it's possible! The universe is huge, after all.",
    "Can you help me with this math problem? I'm a little stuck.",
    "Sure! Let's walk through it step by step together.",
    "What's your favorite animal? I've always loved learning about different creatures.",
    "I love dogs! They're so loyal and full of energy.",
    "Have you ever tried skydiving? I hear it's an incredible rush.",
    "Not yet, but it's on my bucket list for sure.",
    "What do you like to do for fun on the weekends?",
    "I enjoy hiking in nature, especially on sunny days.",
    "Do you play any instruments? Music is such a great way to relax.",
    "Yes, I play the guitar. It's my favorite way to unwind.",
    "What's your favorite holiday and why?",
    "I love Halloween! The costumes, decorations, and spooky vibes are so much fun."
]


train_model(test_list)

while True:
    input_sentence = input("You: ")
    classify_and_update_sentence(input_sentence)
    print("AI:", generate_sentence(input_sentence))
