import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from transformers import AutoTokenizer, BertForSequenceClassification, AutoModelForTokenClassification, BertTokenizerFast, pipeline
from transformers import BartForConditionalGeneration, BartTokenizer
from colorama import Fore, Back, Style, init
import time
import random
import re
import pyttsx3
import torch
import os

os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

init(autoreset=True)

class CustomerServiceBot:
    """
    A sophisticated customer service chatbot that utilizes various NLP models for sentiment analysis,
    question classification, named entity recognition, order processing, and text summarization.

    This bot is designed to handle customer inquiries about order status, process order numbers,
    confirm order contents, and provide summarized shipping information. It uses pre-trained BERT models
    for various NLP tasks and a BART model for text summarization.

    Attributes:
        sentiment_model_name (str): Name of the pre-trained sentiment analysis model.
        question_model_name (str): Name of the pre-trained question classification model.
        ner_model_name (str): Name of the pre-trained named entity recognition model.
        summarizer_model_name (str): Name of the pre-trained BART summarization model.
        sentiment_tokenizer (AutoTokenizer): Tokenizer for the sentiment analysis model.
        sentiment_model (BertForSequenceClassification): BERT model for sentiment analysis.
        question_tokenizer (AutoTokenizer): Tokenizer for the question classification model.
        question_model (BertForSequenceClassification): BERT model for question classification.
        ner_tokenizer (BertTokenizerFast): Tokenizer for the NER model.
        ner_model (AutoModelForTokenClassification): BERT model for named entity recognition.
        summarizer_tokenizer (BartTokenizer): Tokenizer for the BART summarization model.
        summarizer_model (BartForConditionalGeneration): BART model for text summarization.
        nlp_ner (pipeline): Hugging Face pipeline for named entity recognition.
        label_map (dict): Mapping of NER labels to their meanings.
        shipping_info (dict): Dictionary containing detailed shipping information for products.
        bot_voice (pyttsx3.Engine): Text-to-speech engine for the bot's voice.
        user_voice (pyttsx3.Engine): Text-to-speech engine for the user's voice.
        device (torch.device): The device (CPU or GPU) to run the models on.
    """

    def __init__(self):
        """
        Initializes the CustomerServiceBot by loading all necessary models and tokenizers.
        Prints a message when models are successfully loaded.
        """
        print("Loading models...")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        self.sentiment_model_name = "phanerozoic/BERT-Sentiment-Classifier"
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained(self.sentiment_model_name)
        self.sentiment_model = BertForSequenceClassification.from_pretrained(self.sentiment_model_name).to(self.device)

        self.question_model_name = "phanerozoic/BERT-Question-Classifier"
        self.question_tokenizer = AutoTokenizer.from_pretrained(self.question_model_name)
        self.question_model = BertForSequenceClassification.from_pretrained(self.question_model_name).to(self.device)

        self.ner_model_name = "phanerozoic/BERT-NER-Classifier"
        self.ner_tokenizer = BertTokenizerFast.from_pretrained(self.ner_model_name)
        self.ner_model = AutoModelForTokenClassification.from_pretrained(self.ner_model_name).to(self.device)
        self.nlp_ner = pipeline("ner", model=self.ner_model, tokenizer=self.ner_tokenizer, device=0 if self.device.type == "cuda" else -1)

        print("BERT models loaded successfully.")

        print("Loading BART summarizer...")
        self.summarizer_model_name = "phanerozoic/BART-Large-CNN-Enhanced"
        self.summarizer_tokenizer = BartTokenizer.from_pretrained(self.summarizer_model_name)
        self.summarizer_model = BartForConditionalGeneration.from_pretrained(self.summarizer_model_name).to(self.device)
        print("BART summarizer loaded successfully.\n")

        self.label_map = {
            "LABEL_0": "O",
            "LABEL_1": "B-PER", "LABEL_2": "I-PER",
            "LABEL_3": "B-ORG", "LABEL_4": "I-ORG",
            "LABEL_5": "B-LOC", "LABEL_6": "I-LOC",
            "LABEL_7": "B-MISC", "LABEL_8": "I-MISC"
        }

        self.shipping_info = {
            "GizmoTron": """
            The shipping process for the GizmoTron is a comprehensive and meticulously planned operation designed to ensure that our cutting-edge product reaches customers in perfect condition and in a timely manner. Our process begins the moment an order is placed, triggering a sophisticated chain of events within our state-of-the-art fulfillment centers.

            Initially, each GizmoTron order undergoes a rigorous processing phase. This involves verifying the order details, checking inventory availability, and assigning the order to the most suitable fulfillment center based on the customer's location and current stock levels. This initial stage typically takes 1-2 business days, during which our quality control team also performs a final inspection on each unit to ensure it meets our exacting standards.

            Once the order is processed and the product is cleared for shipping, it enters our advanced logistics network. For domestic orders within the continental United States, we employ a multi-tiered shipping strategy. This includes utilizing our own dedicated delivery fleet for nearby locations and partnering with leading courier services for wider distribution. Under normal circumstances, our standard shipping time for domestic orders is 5-7 business days from the date of shipment.

            However, it's important to note that due to the overwhelming popularity of the GizmoTron, we are currently experiencing higher than usual demand. This increased volume may result in extended shipping times, potentially ranging from 14 to 21 business days from the date of order placement to final delivery. We are continuously working to optimize our processes and increase our capacity to mitigate these delays.

            For customers who require their GizmoTron sooner, we offer an express shipping option. These orders receive priority handling in our fulfillment centers and are shipped via premium logistics partners. Express shipments typically arrive within 3-5 business days, although even these expedited services may experience slight delays during peak periods or in cases of unforeseen logistical challenges.

            International shipping for the GizmoTron is available to a select group of countries, chosen based on demand and our ability to ensure reliable delivery. The international shipping process is more complex, involving additional steps such as customs clearance, compliance with varying international regulations, and navigating different regional logistics networks. As a result, shipping times for international orders can range from 10 to 30 business days, depending on the destination country.

            Customers opting for international shipping should be aware that additional fees may apply. These can include import duties, taxes, and customs clearance charges, which are the responsibility of the recipient and are not included in the initial shipping cost. We provide detailed information about potential additional charges at checkout to ensure transparency.

            To enhance the customer experience, we offer real-time tracking for all GizmoTron shipments. Customers receive a unique tracking number once their order is dispatched, allowing them to monitor the progress of their delivery through our website or mobile app. Our customer service team is also available to provide updates and address any concerns throughout the shipping process.

            We understand that waiting for a GizmoTron can be exciting, and we appreciate our customers' patience. Rest assured that from the moment an order is placed to the final delivery, every step is carefully managed to ensure that each GizmoTron arrives safely and ready to transform your technological experience.
            """,
            "Thingamajig": """
            The shipping process for the Thingamajig represents the pinnacle of our commitment to customer satisfaction and operational excellence. We have developed a sophisticated, global logistics network to ensure that every Thingamajig reaches its new owner swiftly and in pristine condition, regardless of their location around the world.

            Our journey begins the moment a customer places an order for a Thingamajig. Our advanced order management system immediately springs into action, analyzing the order details and determining the optimal fulfillment strategy. We have strategically positioned fulfillment centers across different regions, each stocked with Thingamajigs and staffed by highly trained personnel. This distributed approach allows us to minimize shipping times and reduce the carbon footprint of our deliveries.

            For domestic orders within the United States, we offer a range of shipping options to cater to different customer needs. Our standard shipping service, which is the most popular choice, typically delivers the Thingamajig within 3-5 business days. This service includes comprehensive tracking capabilities, allowing customers to monitor their package's journey in real-time through our website or mobile app. Additionally, all domestic shipments are fully insured, providing peace of mind to our customers.

            Recognizing that some customers may need their Thingamajig even sooner, we also offer an expedited shipping option. This premium service guarantees delivery within 2 business days for most locations within the continental United States. Expedited orders receive priority handling at our fulfillment centers, are processed within hours of being placed, and are shipped via our network of premium courier partners. This service is ideal for customers who need their Thingamajig for time-sensitive projects or those who simply can't wait to start using their new device.

            The Thingamajig has garnered a global following, and we're proud to offer international shipping to over 100 countries. Our international shipping process is a testament to our logistical expertise, navigating the complexities of global commerce to bring the Thingamajig to customers worldwide. For most major international cities, customers can expect their Thingamajig to arrive within 7-14 business days when using our standard international shipping service. This timeframe includes processing at our fulfillment center, international transit, and local delivery.

            However, we acknowledge that shipping to more remote locations or countries with complex customs procedures can take longer. In these cases, delivery times may extend to 21-30 business days. We work closely with local customs authorities and international shipping partners to streamline the process as much as possible, but some factors remain outside our control.

            It's crucial to note that all shipping times provided are estimates based on typical conditions. Various factors can influence actual delivery times, including weather conditions, customs delays, local delivery service limitations, and global events affecting international logistics. During peak seasons, such as major holiday periods, customers may experience slightly longer shipping times due to increased volume in global logistics networks.

            To manage customer expectations effectively, we provide an estimated delivery date at checkout. This date is calculated using a sophisticated algorithm that takes into account current conditions, historical data for the specific location, and real-time information from our logistics partners. We continuously update this information to ensure its accuracy.

            For all shipments, domestic and international, we employ state-of-the-art packaging techniques to protect the Thingamajig during transit. Each unit is carefully cushioned and sealed in a custom-designed box that not only safeguards the product but also minimizes environmental impact through the use of recyclable materials.

            We understand that waiting for a Thingamajig can be an exciting time, and we strive to make the shipping process as transparent and efficient as possible. Our dedicated customer service team is available around the clock to address any questions or concerns about shipping. They can provide detailed updates on order status, help with any delivery issues, and offer advice on the best shipping options for each customer's unique situation.

            In our commitment to sustainability, we are constantly exploring ways to reduce the environmental impact of our shipping processes. This includes optimizing route planning to reduce fuel consumption, using electric vehicles for local deliveries where possible, and partnering with carbon-offset programs to mitigate the environmental impact of long-distance shipments.

            As we continue to innovate and expand our product line, our shipping and logistics capabilities evolve in tandem. We're investing in emerging technologies like predictive analytics and AI-driven logistics planning to further enhance the efficiency and reliability of our shipping process. Our goal is to ensure that every Thingamajig reaches its new owner not just quickly, but in a way that reflects the cutting-edge nature of the product itself.
            """
        }

        self.bot_voice = pyttsx3.init()
        self.user_voice = pyttsx3.init()

        voices = self.bot_voice.getProperty('voices')
        self.bot_voice.setProperty('voice', voices[0].id)
        self.user_voice.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

    def analyze_sentiment(self, text):
        """
        Analyzes the sentiment of the given text using the BERT sentiment classifier.

        Args:
            text (str): The input text to analyze.

        Returns:
            tuple: A tuple containing the sentiment (str) and the sentiment score (float).
                   Sentiment is either "Positive" or "Negative".
        """
        inputs = self.sentiment_tokenizer(text, return_tensors="pt").to(self.device)
        outputs = self.sentiment_model(**inputs)
        probs = outputs.logits.softmax(dim=-1)
        sentiment_score = probs[0][1].item()
        sentiment = "Positive" if sentiment_score > 0.5 else "Negative"
        return sentiment, sentiment_score

    def classify_question(self, text):
        """
        Classifies the type of question in the given text using the BERT question classifier.

        Args:
            text (str): The input text to classify.

        Returns:
            str: The classified question type (e.g., "Description", "Entity", "Expression", etc.).
        """
        inputs = self.question_tokenizer(text, return_tensors="pt").to(self.device)
        outputs = self.question_model(**inputs)
        probs = outputs.logits.softmax(dim=-1)
        class_id = probs.argmax().item()
        label_map = {0: "Description", 1: "Entity", 2: "Expression", 3: "Human", 4: "Location", 5: "Numeric"}
        query_type = label_map[class_id]
        return query_type

    def extract_order_number(self, text):
        """
        Extracts an order number from the given text using a regular expression.

        Args:
            text (str): The input text from which to extract the order number.

        Returns:
            str or None: The extracted order number if found, otherwise None.
        """
        match = re.search(r'\b\d{4,}\b', text)
        return match.group(0) if match else None

    def clean_entity(self, entity):
        """
        Cleans and formats an extracted entity string.

        Args:
            entity (str): The entity string to clean.

        Returns:
            str: The cleaned entity string.
        """
        entity = entity.replace("3000", "").replace("4000", "").strip()
        return entity

    def extract_entities(self, text):
        """
        Extracts named entities from the given text using the BERT NER model.

        This method processes the NER results, combines multi-word entities,
        and cleans the extracted entities.

        Args:
            text (str): The input text from which to extract entities.

        Returns:
            list: A list of cleaned and extracted entity strings.
        """
        results = self.nlp_ner(text)
        formatted_results = []
        for result in results:
            if result['word'].startswith('##'):
                formatted_results[-1]['word'] += result['word'].replace('##', '')
                formatted_results[-1]['end'] = result['end']
            else:
                formatted_results.append({
                    'entity': self.label_map[result['entity']],
                    'word': result['word'],
                    'start': result['start'],
                    'end': result['end']
                })

        entities = []
        current_entity = ""
        current_entity_type = ""

        for result in formatted_results:
            if result['entity'].startswith("B-"):
                if current_entity:
                    entities.append(self.clean_entity(current_entity.strip()))
                current_entity = result['word']
                current_entity_type = result['entity'][2:]
            elif result['entity'].startswith("I-") and result['entity'][2:] == current_entity_type:
                current_entity += f" {result['word']}"
            else:
                if current_entity:
                    entities.append(self.clean_entity(current_entity.strip()))
                current_entity = ""
                current_entity_type = ""

        if current_entity:
            entities.append(self.clean_entity(current_entity.strip()))

        print(Fore.CYAN + f"Extracted Entities Output: {formatted_results}")
        print(Fore.CYAN + f"Final Extracted Entities: {entities}")
        return entities

    def summarize_text(self, text, max_length=150, min_length=40):
        """
        Summarizes the given text using the BART summarization model and formats the output.

        Args:
            text (str): The input text to summarize.
            max_length (int): The maximum length of the summary.
            min_length (int): The minimum length of the summary.

        Returns:
            str: The generated summary, properly formatted as a single paragraph.
        """
        inputs = self.summarizer_tokenizer([text], max_length=1024, return_tensors="pt", truncation=True).to(self.device)
        summary_ids = self.summarizer_model.generate(inputs["input_ids"], num_beams=4, max_length=max_length, min_length=min_length, length_penalty=2.0)
        summary = self.summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        summary = summary.replace("\n", " ").strip()
        sentences = [s.strip().capitalize() for s in summary.split('.') if s.strip()]
        formatted_summary = ". ".join(sentences) + "."

        return formatted_summary

    def get_shipping_info(self, product):
        """
        Retrieves and summarizes shipping information about a specific product.

        Args:
            product (str): The name of the product to retrieve shipping information for.

        Returns:
            str: A summary of the shipping information or an error message if the product is not found.
        """
        product_key = next((key for key in self.shipping_info.keys() if key.lower() == product.lower()), None)
        if product_key:
            full_info = self.shipping_info[product_key]
            summary = self.summarize_text(full_info, max_length=200, min_length=100)
            return summary
        else:
            return "I'm sorry, I don't have shipping information about that product."

    def welcome_message(self):
        """
        Generates a welcome message for the chatbot.

        Returns:
            str: A welcome message string.
        """
        return "Welcome to the Acme Chatbot! How can I assist you today?"

    def initial_bot_response(self, sentiment):
        """
        Generates an initial response based on the detected sentiment of the user's message.

        Args:
            sentiment (str): The detected sentiment ("Positive" or "Negative").

        Returns:
            str: An appropriate initial response string.
        """
        if sentiment == "Positive":
            return "Thanks for reaching out! Can you please provide your order number so I can assist you further?"
        else:
            return "I'm sorry to hear that you're having issues. Can you please provide your order number so I can assist you?"

    def order_number_response(self, order_number):
        """
        Generates a response acknowledging the receipt of an order number.

        Args:
            order_number (str): The extracted order number.

        Returns:
            str: A response string confirming the order number.
        """
        return f"Thank you for providing your order number {order_number}. Let me check the status for you."

    def item_confirmation_response(self, entities):
        """
        Generates a response confirming the items in the user's order based on extracted entities.

        Args:
            entities (list): A list of extracted entity strings representing order items.

        Returns:
            str: A response string confirming the order items or requesting more information.
        """
        if entities:
            return f"I can confirm your order contains {', '.join(entities)}."
        else:
            return "Could you please provide more details about the items in your order?"

    def shipping_info_response(self, product):
        """
        Generates a response with summarized shipping information for a specific product.

        Args:
            product (str): The name of the product to provide shipping information for.

        Returns:
            str: A response string containing summarized shipping information.
        """
        shipping_summary = self.get_shipping_info(product)
        return f"Here's what I can tell you about shipping for the {product}: {shipping_summary}"

    def speak_bot(self, text):
        """Speak the bot's response"""
        print(Fore.YELLOW + f"Bot: {text}")
        self.bot_voice.say(text)
        self.bot_voice.runAndWait()

    def speak_user(self, text):
        """Speak the user's input"""
        print(Fore.GREEN + f"User: {text}")
        self.user_voice.say(text)
        self.user_voice.runAndWait()

    def run_test(self):
        """
        Runs a test simulation of the chatbot's functionality.

        This method simulates a conversation with a user, demonstrating the bot's
        ability to greet, analyze sentiment, process order numbers, confirm order items,
        and provide summarized shipping information. It uses color-coded output for better readability.
        """
        self.speak_bot(self.welcome_message())
        time.sleep(2)

        initial_query = random.choice([
            "Hi, I just wanted to check on my order status. Everything has been great so far!",
            "Hi, I haven't received my order yet and I'm getting frustrated."
        ])
        self.speak_user(initial_query)
        time.sleep(2)

        sentiment, sentiment_score = self.analyze_sentiment(initial_query)
        sentiment_color = Fore.BLUE if sentiment == "Positive" else Fore.RED
        print(f"{sentiment_color}Sentiment: {sentiment} (Score: {sentiment_score:.2f})")
        time.sleep(2)

        bot_response = self.initial_bot_response(sentiment)
        self.speak_bot(bot_response)
        time.sleep(2)

        order_number = str(random.randint(1000, 9999))
        follow_up_query = f"Sure, the order number is {order_number}."
        self.speak_user(follow_up_query)
        time.sleep(2)

        query_type = self.classify_question(follow_up_query)
        print(Fore.CYAN + f"Query Type: {query_type}")
        extracted_order_number = self.extract_order_number(follow_up_query)
        print(Fore.CYAN + f"Extracted Order Number: {extracted_order_number}")
        time.sleep(2)

        bot_response = self.order_number_response(extracted_order_number)
        self.speak_bot(bot_response)
        time.sleep(2)

        bot_response = "Can you confirm the items in your order?"
        self.speak_bot(bot_response)
        time.sleep(2)

        confirmation_query = random.choice([
            "I ordered the GizmoTron.",
            "I ordered the Thingamajig."
        ])
        self.speak_user(confirmation_query)
        time.sleep(2)

        entities = self.extract_entities(confirmation_query)
        time.sleep(2)

        bot_response = self.item_confirmation_response(entities)
        self.speak_bot(bot_response)
        time.sleep(2)

        self.speak_user("When will my order be shipped?")
        time.sleep(2)

        shipping_response = self.shipping_info_response(entities[0])
        self.speak_bot(shipping_response)

        time.sleep(2)
        self.speak_user("Thank you!")
        time.sleep(1)
        print(Fore.CYAN + "[User has disconnected]")

if __name__ == "__main__":
    bot = CustomerServiceBot()
    bot.run_test()
