from litellm import completion
from core.schemas import TestSuite, ProductRequirements

# --- THE SHIELD: MULTI-MODEL FAILOVER HELPER ---
def resilient_completion(prompt_messages, temp=0.3, primary_model="gemini/gemini-3.1-flash-lite-preview", **kwargs):
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
            print(f"🔄 QA Generator calling: {model_name}...")
            response = completion(
                model=model_name,
                messages=prompt_messages,
                temperature=temp,
                timeout=45, # Matrix generation takes a bit longer, so we give it 45s
                **kwargs  # CRITICAL: Passes the Pydantic schema formatting
            )
            return response
        except Exception as e:
            print(f"⚠️ QA Generator Failover: {model_name} failed: {e}")
            continue
            
    # Absolute Emergency Fallback Object
    print("🚨 All APIs failed. Deploying emergency JSON mock for Test Suite.")
    class MockMessage:
        content = '{"test_cases": [{"test_type": "System Error", "scenario_description": "API Services Offline", "expected_result": "System gracefully handles failure via Failover Shield.", "source_refs": ["[REF-EMERGENCY]"]}]}'
    class MockChoice:
        message = MockMessage()
    class MockResponse:
        choices = [MockChoice()]
    return MockResponse()

class QAAgent:
    def __init__(self, model="gemini/gemini-3.1-flash-lite-preview"):
        self.model = model

    def generate_tests(self, requirements: ProductRequirements) -> TestSuite:
        req_json = requirements.model_dump_json(indent=2)
        
        prompt = f"""
        You are an adversarial QA Automation Engineer. Read these User Stories and generate a comprehensive Test Suite.
        Include Positive, Negative, and Edge Cases. 
        CRITICAL: You MUST preserve the `source_refs` from the User Story into the Test Case. If it's a new inferred edge case, use ["[REF-INFERRED]"].
        
        User Stories:
        {req_json}
        
        Return ONLY valid JSON matching the schema.
        """
        
        # --- SHIELDED CALL ---
        response = resilient_completion(
            prompt_messages=[{"role": "user", "content": prompt}],
            temp=0.3,
            primary_model=self.model,
            response_format=TestSuite
        )
        
        raw_json = response.choices[0].message.content
        
        # Cleanup just in case a model accidentally returns markdown code blocks around the JSON
        clean_json = raw_json.replace("```json", "").replace("```", "").strip()
        
        return TestSuite.model_validate_json(clean_json)