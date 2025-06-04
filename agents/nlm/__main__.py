"""# ludorum.agents.nlm.main"""

def main(
    action: str,
    **kwargs
) -> None:
    """# Execute Neural Logic Machine Action.
    
    ## Args:
        * action    (str):  Neural Logic Machine action being executed.
    """
    # Match action.
    match action:
        
        # Invalid action.
        case _: raise ValueError(f"""Invliad NLM action selection: {action}""")