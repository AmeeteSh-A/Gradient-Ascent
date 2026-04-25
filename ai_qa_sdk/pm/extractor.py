from litellm import completion
from core.schemas import ProductRequirements

# --- THE SHIELD: MULTI-MODEL FAILOVER HELPER ---
def resilient_completion(prompt_messages, temp=0.2, primary_model="gemini/gemini-3.1-flash-lite-preview", **kwargs):
    """
    Cycles through a list of models. If one throws a 503 or 404, it instantly tries the next.
    Accepts **kwargs to pass things like 'response_format' securely.
    """
    failover_chain = [
        primary_model,
        "groq/llama-3.3-70b-versatile",    # Ultra-fast backup
        "gemini/gemini-1.5-flash-latest"   # Stable fallback
    ]
    
    for model_name in failover_chain:
        try:
            print(f"🔄 Extractor calling: {model_name}...")
            response = completion(
                model=model_name,
                messages=prompt_messages,
                temperature=temp,
                timeout=30,
                **kwargs  # CRITICAL: Passes the Pydantic schema formatting
            )
            return response
        except Exception as e:
            print(f"⚠️ Extractor Failover: {model_name} failed: {e}")
            continue
            
    # Absolute Emergency Fallback Object
    print("🚨 All APIs failed. Deploying emergency JSON mock.")
    class MockMessage:
        content = '{"epics": [{"title": "Emergency Fallback Epic", "description": "API Offline.", "source_refs": []}], "user_stories": []}'
    class MockChoice:
        message = MockMessage()
    class MockResponse:
        choices = [MockChoice()]
    return MockResponse()

class PMAgent:
    def __init__(self, model="gemini/gemini-3.1-flash-lite-preview"):
        self.model = model


    def extract_requirements(self, tagged_text: str) -> ProductRequirements:
        prompt = f"""
        You are an elite Product Manager. Extract Epics and User Stories from this tagged PRD.
        Every Epic and User Story MUST include the exact [REF-ID] tags that justify its creation in the `source_refs` field.
        
        PRD Text:
        {tagged_text}
        Return ONLY valid JSON matching the schema.
        """
        
        # --- SHIELDED CALL ---
        response = resilient_completion(
            prompt_messages=[{"role": "user", "content": prompt}],
            temp=0.2,
            primary_model=self.model,
            response_format=ProductRequirements
        )
        
        raw_json = response.choices[0].message.content
        
        # Cleanup just in case a model accidentally returns markdown code blocks around the JSON
        clean_json = raw_json.replace("```json", "").replace("```", "").strip()
        
        return ProductRequirements.model_validate_json(clean_json)