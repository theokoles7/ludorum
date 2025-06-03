"""# ludorum.agents.nlm.main"""

from argparse   import Namespace

def main(
    arguments:  Namespace
) -> None:
    """# Execute Neural Logic Machine Action.
    
    ## Args:
        * arguments (Namespace):    Argument name space from parent process.
    """
    
    print(arguments)
    
    print("MADE IT 2 NLM.MAIN")
    
    # # Match action.
    # match args["action"]:
        
    #     # Invalid action.
    #     case _: raise ValueError(f"""Invliad NLM action selection: {args["action"]}""")