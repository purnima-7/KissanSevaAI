from backend.chat.multilingual_rag import answer_question_multilingual


def run_tests():
    test_questions = [
    # "Which pesticide is used for aphids?",                           # English
    # "What is the recommended chemical treatment for Early Blight in Tomato plants?",  # English
    "ఆంధ్రప్రదేశ్‌లో ఖరీఫ్ వరి (Kharif Paddy) విత్తే కాలం ఏమిటి?",               # Telugu
    "ਸਰ੍ਹੋਂ ਦੀ ਫ਼ਸਲ ਵਿੱਚ ਤੇਲੇ (aphid) ਦੇ ਹਮਲੇ ਨੂੰ ਰੋਕਣ ਲਈ ਕੀ ਉਪਾਅ ਸੁਝਾਇਆ ਗਿਆ ਹੈ?",  # Punjabi
    "ಮರಳು ಮಣ್ಣಿನಲ್ಲಿ (Sandy soil) ಮೆಕ್ಕೆಜೋಳಕ್ಕೆ ಯಾವ ರಸಗೊಬ್ಬರವನ್ನು ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ?",  # Kannada
    # "১৯৯৭ চনৰ শস্য বৰ্ষত অসমত তামোলৰ (Arecanut) উৎপাদন কিমান আছিল?",               # Assamese
    # "ബാർലിയിലെ ലീഫ് ബ്ലൈറ്റ് (Leaf Blight) രോഗത്തിന് കാരണമാകുന്ന ഏజెంట్ ഏതാണ്?",          # Malayalam
    # "એડ્રિસ્ટીરેનસ (Adristyrannus) જીવાત માટે સામાન્ય રીતે કઈ જંતુનાશકોનો ઉપયોગ થાય છે?",  # Gujarati
    # "ஆப்பிரிக்காவில் உணவின் முக்கிய ஆதாரமாக விளங்கும் பயிர் எது?",                      # Tamil
    # "गाईचे दूध उत्पादन कमी असल्यास कोणता उपचार सुचवला जातो?",                      # Marathi
    # "আসামে রবি ধান কাটার সময়কাল কোনটি?",                                       # Bengali
    # "ଧାନରେ ବ୍ଲାଷ୍ଟ (Blast) ରୋଗ ନିୟନ୍ତ୍ରଣ ପାଇଁ ଜୈବିକ ବିକଳ୍ପ କ’ଣ?",                          # Odia

    # ---------------- OUT OF SCOPE -------------------------
    "रॉकेट कैसे बनाया जाता है?",                                     # Hindi
    "ક્વાંટમ ભૌતિકશાસ્ત્ર સમજાવો"                                      # Gujarati
    ]


    print("\n========== RAG TEST OUTPUT ==========\n")

    for i, question in enumerate(test_questions, start=1):
        print(f"Test {i}")
        print("Q:", question)

        answer = answer_question_multilingual(question)

        print("A:", answer)
        print("-" * 70)


if __name__ == "__main__":
    run_tests()
