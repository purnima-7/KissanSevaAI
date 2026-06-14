from backend.chat.rag import answer_question


def run_tests():
    test_questions = [
        # ---------------- PEST & PESTICIDE DATA ----------------
        "Which pesticide is used for aphids?",
        "What is the sowing period for Rabi wheat in Madhya Pradesh?"
        # "Which insecticide controls bean fly and aphids?",
        # "Which insecticides are effective against aphids and whiteflies?",

        # ---------------- CROP / DISEASE DATA ------------------
        # "What is the recommended treatment for aphids?",
        # "What precautions should be taken while controlling aphids?",
        # "Which pesticide is used to control jute aphid?",

        # ---------------- FARMING PRACTICES --------------------
        "What is crop rotation?",
        # "Why is crop rotation important in farming?",
        "What are the different methods of irrigation?",

        # ---------------- FERTILIZER / YIELD -------------------
        "What type of fertilizers are used in farming?",
        # "Why are fertilizers used in farming?",

        # ---------------- OUT OF SCOPE -------------------------
        # "How to build a rocket?",
        # "Explain quantum physics"
    ]

    print("\n========== RAG TEST OUTPUT ==========\n")

    for i, question in enumerate(test_questions, start=1):
        print(f"Test {i}")
        print("Q:", question)

        answer = answer_question(question)

        print("A:", answer)
        print("-" * 70)


if __name__ == "__main__":
    run_tests()
