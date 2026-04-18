"""Run gaming analytics pipeline."""

from gaming_pipeline.orchestrate.flows import pipeline_flow


def main() -> None:
    print("Running gaming analytics pipeline...")
    try:
        pipeline_flow()
    except Exception as e:
        print(f"Pipeline failed: {e}")
        raise SystemExit(1) from None
    print("Pipeline completed successfully!")


if __name__ == "__main__":
    main()
