import spacy
from fuzzywuzzy import process
from faq_dataset import faq_data

nlp = spacy.load('en_core_web_md')

# Function to filter FAQs by category
def get_faqs_by_category(category):
    return [item for item in faq_data if item["category"].lower() == category.lower()]

# Preprocessing FAQ questions for NLP similarity
def get_best_match(user_query, faqs):
    faq_questions = [item["question"] for item in faqs]
    faq_docs = [nlp(question) for question in faq_questions]
    user_doc = nlp(user_query)
    similarities = [user_doc.similarity(faq_doc) for faq_doc in faq_docs]
    best_match_index = similarities.index(max(similarities))
    return faqs[best_match_index], max(similarities)

# Chatbot function
def chatbot():
    print("Chatbot: Hi! Welcome to the FAQ Bot!")
    print("\nHere are the available categories:\n")
    
    # Display all categories
    categories = set(item["category"] for item in faq_data)
    for category in categories:
        print(f"- {category}")
    
    # Ask the user to select a category
    while True:
        selected_category = input("\nSelect a category or type 'exit' to quit: ").strip()
        
        if selected_category.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        
        # Validate the selected category
        if selected_category.lower() not in [cat.lower() for cat in categories]:
            print("Chatbot: Invalid category. Please select a valid category.")
            continue
        
        # Fetch FAQs for the selected category
        faqs = get_faqs_by_category(selected_category)
        print(f"\nChatbot: You selected the '{selected_category}' category.")
        print("Ask your question, or type 'back' to choose another category.")
        
        # Handle questions within the category
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == "back":
                print("\nChatbot: Returning to category selection.")
                break
            
            if user_input.lower() == "exit":
                print("Chatbot: Goodbye!")
                return
            
            # Match user query to FAQs in the selected category
            best_match, confidence = get_best_match(user_input, faqs)
            
            if confidence > 0.7:
                response = f"{best_match['answer']}"
                print(f"\nChatbot: {response}")
            else:
                print("Chatbot: I'm sorry, I couldn't understand your question. Could you rephrase it?")

# Start the chatbot
if __name__ == "__main__":
    chatbot()
