"""
Prompt Manager - Versioned prompt management system for consistent LLM interactions
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import structlog

logger = structlog.get_logger(__name__)

@dataclass
class PromptTemplate:
    """Represents a prompt template with metadata"""
    name: str
    description: str
    use_case: str
    content: str
    version: str
    category: str
    metadata: Dict[str, Any]

@dataclass
class PromptVersion:
    """Represents a prompt version with all templates"""
    version: str
    prompts: Dict[str, PromptTemplate]
    metadata: Dict[str, Any]

class PromptManager:
    """Manages versioned prompt templates for LLM interactions"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.versions_dir = self.prompts_dir / "versions"
        self.current_version = "v1.0.0"
        self.prompt_cache: Dict[str, PromptVersion] = {}
        
        # Ensure directories exist
        self.prompts_dir.mkdir(exist_ok=True)
        self.versions_dir.mkdir(exist_ok=True)
        
        # Load available versions
        self._load_available_versions()
    
    def _load_available_versions(self):
        """Load all available prompt versions"""
        try:
            for version_dir in self.versions_dir.iterdir():
                if version_dir.is_dir() and version_dir.name.startswith('v'):
                    version = version_dir.name
                    self._load_version(version)
                    
            logger.info("Loaded prompt versions", 
                       versions=list(self.prompt_cache.keys()),
                       current=self.current_version)
                       
        except Exception as e:
            logger.error("Failed to load prompt versions", error=str(e))
    
    def _load_version(self, version: str):
        """Load a specific prompt version"""
        version_dir = self.versions_dir / version
        if not version_dir.exists():
            raise ValueError(f"Version {version} not found")
        
        prompts = {}
        version_metadata = {"loaded_at": datetime.utcnow().isoformat()}
        
        # Load all YAML files in version directory
        for yaml_file in version_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                category = data.get('category', yaml_file.stem)
                file_metadata = data.get('metadata', {})
                
                # Update version metadata
                version_metadata.update(file_metadata)
                
                # Load prompts from this file
                for prompt_key, prompt_data in data.get('prompts', {}).items():
                    template = PromptTemplate(
                        name=prompt_data['name'],
                        description=prompt_data['description'],
                        use_case=prompt_data['use_case'],
                        content=prompt_data['content'].strip(),
                        version=version,
                        category=category,
                        metadata=file_metadata
                    )
                    prompts[prompt_key] = template
                    
            except Exception as e:
                logger.error("Failed to load prompt file", 
                           file=str(yaml_file), 
                           error=str(e))
        
        self.prompt_cache[version] = PromptVersion(
            version=version,
            prompts=prompts,
            metadata=version_metadata
        )
        
        logger.debug("Loaded prompt version", 
                    version=version, 
                    prompt_count=len(prompts))
    
    def get_prompt(self, prompt_key: str, version: Optional[str] = None) -> Optional[PromptTemplate]:
        """Get a specific prompt template"""
        version = version or self.current_version
        
        if version not in self.prompt_cache:
            try:
                self._load_version(version)
            except Exception as e:
                logger.error("Failed to load version for prompt", 
                           version=version, 
                           prompt_key=prompt_key, 
                           error=str(e))
                return None
        
        version_data = self.prompt_cache.get(version)
        if not version_data:
            return None
        
        return version_data.prompts.get(prompt_key)
    
    def get_prompt_content(self, prompt_key: str, version: Optional[str] = None) -> Optional[str]:
        """Get prompt content string"""
        template = self.get_prompt(prompt_key, version)
        return template.content if template else None
    
    def list_prompts(self, version: Optional[str] = None, category: Optional[str] = None) -> List[PromptTemplate]:
        """List available prompts"""
        version = version or self.current_version
        
        version_data = self.prompt_cache.get(version)
        if not version_data:
            return []
        
        prompts = list(version_data.prompts.values())
        
        if category:
            prompts = [p for p in prompts if p.category == category]
        
        return prompts
    
    def get_categories(self, version: Optional[str] = None) -> List[str]:
        """Get available prompt categories"""
        prompts = self.list_prompts(version)
        return list(set(p.category for p in prompts))
    
    def get_versions(self) -> List[str]:
        """Get available prompt versions"""
        return list(self.prompt_cache.keys())
    
    def set_current_version(self, version: str):
        """Set the current default version"""
        if version not in self.prompt_cache:
            raise ValueError(f"Version {version} not available")
        self.current_version = version
        logger.info("Changed current prompt version", version=version)
    
    def build_system_prompt(self, task_type: str, version: Optional[str] = None) -> str:
        """Build a system prompt for a specific task type"""
        version = version or self.current_version
        
        # Map task types to prompt keys
        task_prompt_mapping = {
            "navigation": "system_navigation",
            "search": "search_optimization", 
            "ecommerce": "product_search",
            "anti_bot_ecommerce": "anti_bot_ecommerce",
            "financial": "stock_research",
            "fund_analysis": "fund_analysis",
            "error_handling": "error_handling"
        }
        
        prompt_key = task_prompt_mapping.get(task_type, "system_navigation")
        base_prompt = self.get_prompt_content(prompt_key, version)
        
        if not base_prompt:
            # Fallback to basic navigation prompt
            base_prompt = self.get_prompt_content("system_navigation", version)
        
        if not base_prompt:
            # Ultimate fallback
            return self._get_fallback_prompt(task_type)
        
        # Add error handling if not already included
        if task_type != "error_handling":
            error_prompt = self.get_prompt_content("error_handling", version)
            if error_prompt:
                base_prompt += f"\n\nERROR HANDLING:\n{error_prompt}"
        
        return base_prompt
    
    def _get_fallback_prompt(self, task_type: str) -> str:
        """Fallback prompt if no templates are available"""
        return f"""You are a skilled web automation specialist performing {task_type} tasks.
        
Navigate websites naturally and human-like. Take time to understand each page before acting.
Use visual cues and context to make decisions. Be patient and methodical.
Handle errors gracefully and adapt to different website layouts."""
    
    def create_task_prompt(self, task_description: str, task_type: str = "navigation", 
                          version: Optional[str] = None) -> str:
        """Create a complete prompt for a specific automation task"""
        system_prompt = self.build_system_prompt(task_type, version)
        
        task_prompt = f"""
TASK: {task_description}

{system_prompt}

Now complete the specified task following these guidelines.
"""
        return task_prompt.strip()
    
    def get_prompt_stats(self) -> Dict[str, Any]:
        """Get statistics about loaded prompts"""
        stats = {
            "total_versions": len(self.prompt_cache),
            "current_version": self.current_version,
            "versions": {},
            "total_prompts": 0
        }
        
        for version, version_data in self.prompt_cache.items():
            prompt_count = len(version_data.prompts)
            categories = set(p.category for p in version_data.prompts.values())
            
            stats["versions"][version] = {
                "prompt_count": prompt_count,
                "categories": list(categories),
                "metadata": version_data.metadata
            }
            stats["total_prompts"] += prompt_count
        
        return stats
    
    def validate_prompts(self, version: Optional[str] = None) -> Dict[str, Any]:
        """Validate prompt templates for completeness and quality"""
        version = version or self.current_version
        version_data = self.prompt_cache.get(version)
        
        if not version_data:
            return {"valid": False, "error": f"Version {version} not found"}
        
        validation_results = {
            "valid": True,
            "version": version,
            "total_prompts": len(version_data.prompts),
            "issues": []
        }
        
        for key, prompt in version_data.prompts.items():
            # Check for required fields
            if not prompt.content or len(prompt.content.strip()) < 50:
                validation_results["issues"].append(f"{key}: Content too short")
            
            if not prompt.description:
                validation_results["issues"].append(f"{key}: Missing description")
            
            if not prompt.use_case:
                validation_results["issues"].append(f"{key}: Missing use_case")
        
        validation_results["valid"] = len(validation_results["issues"]) == 0
        return validation_results

# Global prompt manager instance
prompt_manager = PromptManager()

# Convenience functions
def get_prompt(prompt_key: str, version: Optional[str] = None) -> Optional[str]:
    """Get prompt content by key"""
    return prompt_manager.get_prompt_content(prompt_key, version)

def create_task_prompt(task_description: str, task_type: str = "navigation") -> str:
    """Create a task-specific prompt"""
    return prompt_manager.create_task_prompt(task_description, task_type)

def build_system_prompt(task_type: str) -> str:
    """Build system prompt for task type"""
    return prompt_manager.build_system_prompt(task_type)