import typer
import json
import fast_vertex_quality_inference as fvqi

app = typer.Typer()


def main(config: str, nevents: int):
    """
    Run the Fast Vertex Quality Inference Tool.

    Args:
        config (str): Path to the configuration JSON file.
        match_to_reference (bool): Flag to match inference results to reference.
    """

    output_dir = config.split(".")[0]

    try:
        with open(config, "r") as f:
            config_data = json.load(f)
    except Exception as e:
        typer.echo(f"Error loading config file: {e}")
        raise typer.Exit(code=1)

    fvqi.run(
        events=nevents,
        decay=config_data.get("decay"),
        naming_scheme=config_data.get("naming_scheme"),
        decay_models=config_data.get("decay_models"),
        mass_hypotheses=config_data.get("mass_hypotheses"),
        intermediate_particle=config_data.get("intermediate_particle"),
        verbose=config_data.get("verbose", False),
        run_systematics=config_data.get("run_systematics", False),
        workingDir=f"./{output_dir}",
    )


# Add the main function as a Typer command
app.command()(main)

# Allow running as a script
if __name__ == "__main__":
    app()
