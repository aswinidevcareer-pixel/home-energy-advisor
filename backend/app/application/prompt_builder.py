from app.domain.entities import HomeProfile
from typing import Optional, List


class EnergyAdvicePromptBuilder:
    """Builder pattern for constructing energy advice prompts with fluent interface."""
    
    def __init__(self):
        self._parts: List[str] = []
        self._home: Optional[HomeProfile] = None
        
    def with_home_profile(self, home: HomeProfile) -> 'EnergyAdvicePromptBuilder':
        """Set the home profile for the prompt."""
        self._home = home
        return self
    
    def add_system_context(self) -> 'EnergyAdvicePromptBuilder':
        """Add the expert system context."""
        self._parts.append(self.build_system_message())
        return self
    
    def add_home_details(self) -> 'EnergyAdvicePromptBuilder':
        """Add home profile details."""
        if not self._home:
            raise ValueError("Home profile must be set before adding details")
        
        details = f"""
Home Profile:
- Size: {self._home.size_sqft} square feet
- Age: {self._home.age_years} years old
- Heating Type: {self._home.heating_type}
- Insulation: {self._home.insulation_type}
- Windows: {self._home.window_type}
- Floors: {self._home.num_floors}
- Occupants: {self._home.num_occupants}
- Basement: {"Yes" if self._home.has_basement else "No"}
- Attic: {"Yes" if self._home.has_attic else "No"}
- Solar Panels: {"Yes" if self._home.has_solar_panels else "No"}"""
        
        if self._home.avg_monthly_energy_cost:
            details += f"\n- Average Monthly Energy Cost: ${self._home.avg_monthly_energy_cost:.2f}"
        
        if self._home.zip_code:
            details += f"\n- Location (Zip Code): {self._home.zip_code}"
        
        self._parts.append(details)
        return self
    
    def add_output_format_instructions(self) -> 'EnergyAdvicePromptBuilder':
        """Add instructions for the expected output format."""
        instructions = """
Based on this information, provide a comprehensive energy efficiency analysis with the following structure:

1. SUMMARY: A brief 2-3 sentence overview of the home's current energy efficiency status and potential for improvement. Include the estimated total annual savings if all recommendations are implemented.

2. RECOMMENDATIONS: Provide 5-8 prioritized recommendations in the JSON format added to the input (return ONLY valid JSON, no markdown)

IMPORTANT GUIDELINES:
- Prioritize recommendations by impact and cost-effectiveness
- Consider the home's age and current features when making suggestions
- Provide realistic cost estimates and savings projections
- Include both quick wins (low-cost, high-impact) and long-term investments
- Make recommendations specific to this home's characteristics
- Ensure all recommendations are actionable and practical
- Return ONLY valid JSON, no markdown formatting, no code blocks
- All numeric values should be numbers, not strings
- Provide Details for all the properties of the response model mentioned in the format
- Do mathmetical calculation and fill in the property values(estimated_savings_annual for each recommendation, estimated_total_annual_savings for EnergyAdvice) based on the logic provided in the schema description."""
        
        self._parts.append(instructions)
        return self
    
    def add_custom_section(self, section: str) -> 'EnergyAdvicePromptBuilder':
        """Add a custom section to the prompt."""
        self._parts.append(section)
        return self
    
    def build(self) -> str:
        """Build and return the final prompt."""
        if not self._home:
            raise ValueError("Home profile must be set before building prompt")
        
        if not self._parts:
            raise ValueError("Prompt must have at least one section")
        
        return "\n".join(self._parts)
    
    def reset(self) -> 'EnergyAdvicePromptBuilder':
        """Reset the builder for reuse."""
        self._parts = []
        self._home = None
        return self
    
    @staticmethod
    def build_prompt(home: HomeProfile) -> str:
        """Convenience method for building a standard prompt (backwards compatible)."""
        return (EnergyAdvicePromptBuilder()
                .with_home_profile(home)
                .add_system_context()
                .add_home_details()
                .add_output_format_instructions()
                .build())
    
    @staticmethod
    def build_system_message() -> str:
        """Build the system message for the LLM."""
        return """You are an expert energy efficiency consultant with deep knowledge of:
- Building science and thermal dynamics
- HVAC systems and heating/cooling efficiency
- Insulation materials and techniques
- Renewable energy systems
- Energy-efficient appliances and technologies
- Cost-benefit analysis for energy improvements
- Regional climate considerations

Provide accurate, practical, and cost-effective recommendations tailored to each home's unique characteristics."""
