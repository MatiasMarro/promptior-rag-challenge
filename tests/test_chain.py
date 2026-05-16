from app.chain import rag_chain

def test_founded_date():
    answer = rag_chain.invoke("When was Promtior founded?")
    assert "2023" in answer, f"Expected '2023' in answer, got: {answer}"
    assert "may" in answer.lower(), f"Expected 'May' in answer, got: {answer}"

def test_services():
    answer = rag_chain.invoke("What services does Promtior offer?")
    # Debe mencionar consultoría
    assert any(word in answer.lower()
        for word in ["consult", "consulting", "consultoría", "advisory"])

def test_offtopic_refusal():
    answer = rag_chain.invoke("What is the capital of Cordoba?")
    # Debe responder con el "no sé", no "Paris"
    assert "paris" not in answer.lower(), \
        f"Chatbot leaked prior knowledge: {answer}"
    assert any(phrase in answer.lower()
        for phrase in ["don't have", "no tengo", "cannot find", "not in"])
    
if __name__ == "__main__":
    test_founded_date()
    print("✓ test_founded_date passed")
    test_services()
    print("✓ test_services passed")
    test_offtopic_refusal()
    print("✓ test_offtopic_refusal passed")
    print("\nAll tests passed.")