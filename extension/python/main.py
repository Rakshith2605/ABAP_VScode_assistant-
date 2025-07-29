#!/usr/bin/env python3
"""
VS Code Extension Backend for ABAP AI Code Completion
"""
import sys
import os
import json
import asyncio
from pathlib import Path

# Add the local_ai_code_completion package to the path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from local_ai_code_completion import config, logger, setup, ai_completion
except ImportError as e:
    print(f"Error: Missing dependencies. Please install required packages: {e}")
    print("The extension will attempt to install dependencies automatically.")
    sys.exit(1)


def main():
    """Main entry point for the VS Code extension backend"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        if command == "generate":
            handle_generate()
        elif command == "setup":
            handle_setup()
        elif command == "config":
            handle_config()
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error in command '{command}': {e}")
        sys.exit(1)


def handle_generate():
    """Handle ABAP code generation command"""
    # Get context from environment variables
    prefix = os.getenv("LACC_PREFIX", "")
    suffix = os.getenv("LACC_SUFFIX", "")
    comment = os.getenv("LACC_COMMENT", "")
    file_path = os.getenv("LACC_FILE", "")
    language = os.getenv("LACC_LANGUAGE", "abap")
    mode = os.getenv("LACC_MODE", "code")
    
    if not prefix and not suffix and not comment:
        print("Error: No context provided for generation")
        sys.exit(1)
    
    # Run generation
    async def generate():
        try:
            # Use the global AI completion instance
            completion = ai_completion
            
            # Create ABAP-specific prompt based on mode
            if mode == "debug":
                prompt = create_abap_debug_prompt(prefix, suffix)
            elif mode == "comment":
                prompt = create_abap_comment_prompt(prefix, suffix, comment)
            else:
                prompt = create_abap_code_prompt(prefix, suffix)
            
            # Generate code
            result = await completion.generate_code_with_prompt(prompt)
            
            if result:
                # Clean up the result to remove any markdown formatting or comments
                cleaned_result = clean_abap_output(result)
                print(cleaned_result)
            else:
                print("No completion generated")
                
        except Exception as e:
            logger.error(f"Generation error: {e}")
            print(f"Error: {e}")
            sys.exit(1)
    
    asyncio.run(generate())


def create_abap_code_prompt(prefix, suffix):
    """Create ABAP-specific code generation prompt"""
    return f"""You are an expert ABAP developer. Generate ABAP code that follows SAP best practices.

Context before cursor:
{prefix}

Context after cursor:
{suffix}

Generate ABAP code that:
1. Follows SAP coding standards
2. Uses proper ABAP syntax and keywords
3. Includes proper error handling
4. Uses meaningful variable names
5. Includes comments where appropriate
6. Follows the context and completes the code logically

CRITICAL: Generate ONLY the ABAP code implementation. Do NOT include any thinking, reasoning, explanations, or markdown formatting. Output ONLY the pure ABAP code. Start directly with the ABAP code:"""


def create_abap_comment_prompt(prefix, suffix, comment):
    """Create ABAP-specific comment-based code generation prompt"""
    return f"""You are an expert ABAP developer. Generate ABAP code based on the provided comment and context.

Context before the comment:
{prefix}

Comment to implement:
{comment}

Context after the comment:
{suffix}

Generate ABAP code that:
1. Implements the functionality described in the comment
2. Follows SAP coding standards
3. Uses proper ABAP syntax and keywords
4. Includes proper error handling
5. Uses meaningful variable names
6. Integrates well with the surrounding code context
7. Replaces the comment with actual implementation

CRITICAL: Generate ONLY the ABAP code implementation. Do NOT include any thinking, reasoning, explanations, or markdown formatting. Output ONLY the pure ABAP code that implements the comment. Start directly with the ABAP code. Do NOT include <think> tags or any other formatting:"""


def create_abap_debug_prompt(prefix, suffix):
    """Create ABAP-specific debug code generation prompt"""
    return f"""You are an expert ABAP developer. Generate ABAP debug code that follows SAP debugging best practices.

Context before cursor:
{prefix}

Context after cursor:
{suffix}

Generate ABAP debug code that:
1. Uses proper ABAP debugging statements (BREAK-POINT, WRITE, etc.)
2. Includes variable inspection code
3. Uses proper ABAP debugging patterns
4. Includes performance monitoring if applicable
5. Uses meaningful debug messages
6. Follows SAP debugging guidelines

Common ABAP debug patterns to include:
- BREAK-POINT for breakpoints
- WRITE statements for output
- DESCRIBE TABLE for table inspection
- SY_TABIX for loop index
- SY_SUBRC for return codes
- Performance timing with GET TIME

CRITICAL: Generate ONLY the ABAP debug code implementation. Do NOT include any thinking, reasoning, explanations, or markdown formatting. Output ONLY the pure ABAP debug code. Start directly with the ABAP code:"""


def clean_abap_output(text):
    """Clean up ABAP output to remove markdown formatting and comments"""
    if not text:
        return text
    
    # Remove markdown code blocks
    lines = text.split('\n')
    cleaned_lines = []
    
    in_code_block = False
    for line in lines:
        # Skip markdown code block markers
        if line.strip().startswith('```'):
            continue
        
        # Skip comment lines that start with # (markdown comments)
        if line.strip().startswith('#'):
            continue
        
        # Skip thinking tags
        if line.strip().startswith('<think>') or line.strip().startswith('</think>'):
            continue
        
        # Skip empty lines at the beginning and end
        if not line.strip() and (not cleaned_lines or all(not l.strip() for l in lines[lines.index(line):])):
            continue
            
        cleaned_lines.append(line)
    
    # Join lines and remove extra whitespace
    result = '\n'.join(cleaned_lines).strip()
    
    return result


def handle_setup():
    """Handle setup command"""
    async def setup_groq():
        try:
            # Get API key from VS Code settings
            api_key = os.getenv("GROQ_API_KEY", "")
            
            if not api_key:
                print("Error: No API key provided")
                sys.exit(1)
            
            # Update configuration
            config.model.api_key = api_key
            
            # Run setup
            success = await setup.setup()
            
            if success:
                print("Setup completed successfully")
            else:
                print("Setup failed")
                sys.exit(1)
                
        except Exception as e:
            logger.error(f"Setup error: {e}")
            print(f"Error: {e}")
            sys.exit(1)
    
    asyncio.run(setup_groq())


def handle_config():
    """Handle configuration display command"""
    try:
        # Get API key from environment variable (passed by VS Code extension)
        api_key = os.getenv("GROQ_API_KEY", "")
        
        model_config = config.get_model_config()
        
        config_data = {
            "model": model_config.name,
            "temperature": model_config.temperature,
            "top_p": model_config.top_p,
            "timeout": model_config.timeout,
            "api_key": "***" if api_key else "Not set",
            "base_url": model_config.base_url,
            "language": "ABAP",
            "features": ["code_generation", "debug_generation", "syntax_highlighting"]
        }
        
        print(json.dumps(config_data, indent=2))
        
    except Exception as e:
        logger.error(f"Config error: {e}")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 