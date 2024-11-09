# fvqv/cli.py

import typer
import json
import fast_vertex_quality_inference as fvqi

app = typer.Typer()

def main(config: str):
    """
    Run the Fast Vertex Quality Inference Tool.

    Args:
        config (str): Path to the configuration JSON file.
        match_to_reference (bool): Flag to match inference results to reference.
    """
    # # Load JSON configuration
    # try:
    #     with open(config, 'r') as f:
    #         config_data = json.load(f)
    # except Exception as e:
    #     typer.echo(f"Error loading config file: {e}")
    #     raise typer.Exit(code=1)

    # Here you would run the main functionality
    # Replace `your_function` with the actual function that processes the config
    # your_function(config_data, match_to_reference)

    print(config, config)
    
    fvqi.run(
        events=2500,
        decay="B+ -> K+ e+ e-",
        naming_scheme="MOTHER -> DAUGHTER1 DAUGHTER2 DAUGHTER3",
        decay_models="BTOSLLBALL_6 -> PHSP PHSP PHSP",
        mass_hypotheses=None,
        intermediate_particle={"INTERMEDIATE":["DAUGHTER2","DAUGHTER3"]},
        verbose=False,
        run_systematics=True,
        workingDir='./TEST',
        )


# def your_function(config_data, match_to_reference):
#     # Example of main functionality based on config
#     typer.echo(f"Running inference with config: {config_data} and match_to_reference: {match_to_reference}")

# Add the main function as a Typer command
app.command()(main)

# Allow running as a script
if __name__ == "__main__":
    app()
