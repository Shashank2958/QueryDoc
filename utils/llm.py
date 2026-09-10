from google import genai


def get_gemini_client():
    """
    Gemini API client banata hai. GEMINI_API_KEY .env file se
    automatically uthega (load_dotenv() app.py mein already chal chuka hoga).
    """
    return genai.Client()


def get_answer_from_gemini(gemini_client, user_input, context_chunks):
    """
    User ka poora message (chahe usme ek ya kayi sawaal hon) aur uske
    relevant chunks (context) leta hai, Gemini ko bhejta hai, aur
    Gemini ka answer wapas deta hai.
    """
    context_text = "\n\n".join(context_chunks)

    prompt = (
        "Tum ek helpful assistant ho jo sirf diye gaye context (PDF se liya "
        "gaya text) ke basis par answer deta hai. Agar answer context mein "
        "nahi hai, to saaf bol do ki 'Ye jaankari PDF mein nahi mili.' "
        "Kisi bhi cheez ko khud se mat banao.\n\n"
        "Agar user ke message mein ek se zyada alag-alag sawaal hain "
        "(chahe wo alag lines mein ho, ek hi paragraph mein ho, ya kisi "
        "bhi format mein likhe hon), to har sawaal ko pehchano aur "
        "har ek ka jawab clearly alag-alag, numbered format mein do.\n\n"
        f"Context:\n{context_text}\n\n"
        f"User ka sawaal/sawaal:\n{user_input}"
    )

    response = gemini_client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text