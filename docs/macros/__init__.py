"""
Macros for the EZQ documentation.
"""

def define_env(env):
    """
    Define environment variables for the macros plugin.
    
    Args:
        env: The environment object from MkDocs macros plugin
    """
    # Set up project-wide variables
    env.variables.project_name = "EZQ"
    env.variables.project_version = "0.1.0"  # Should match pyproject.toml
    
    # Example function to generate code examples
    @env.macro
    def example_config(host="localhost", port=5432):
        """Generate an example configuration code block."""
        return f"""```python
import ezq

ezq.configure(
    queue_host="{host}",
    queue_port={port}
)
```"""
    
    # Example macro to generate a configuration table row
    @env.macro
    def config_row(option, env_var, default, description):
        """Generate a configuration table row with proper formatting."""
        return f"| `{option}` | `{env_var}` | {default} | {description} |" 