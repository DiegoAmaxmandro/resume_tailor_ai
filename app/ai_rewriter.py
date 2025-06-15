from transformers import pipeline, AutoTokenizer

# Loading the model
model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
generator = pipeline("text2text-generation", model=model_name, tokenizer=tokenizer, device="mps")

def truncate_text_by_tokens(text, max_tokens=250):
    tokens = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return tokenizer.decode(tokens, skip_special_tokens=True)

def suggest_resume_improvements(resume_text, job_text):
    resume_text = truncate_text_by_tokens(resume_text, max_tokens=250)
    job_text = truncate_text_by_tokens(job_text, max_tokens=250)

    prompt = f'''
     You're an expert career coach. Based on the job description below, suggest 3–5 specific improvements to the resume so it better matches the job.
    
    Job Description:
    {job_text}
    
    Resume:
    {resume_text}   
    
    '''
    result = generator(
        prompt,
        max_new_tokens=200,
        truncation=True,
        max_length=512
    )[0]["generated_text"]

    return result