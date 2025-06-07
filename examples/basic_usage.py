"""
Basic usage example for QuantumScope.

This script demonstrates how to use QuantumScope programmatically.
"""
import asyncio
from QuantumScope.main import QuantumScopeEngine, QuantumScopeConfig

async def main():
    """Run a basic QuantumScope query."""
    print("🚀 Starting QuantumScope example...")
    
    # Initialize with default config
    config = QuantumScopeConfig()
    engine = QuantumScopeEngine(config)
    
    # Run a research query
    query = "latest advancements in quantum computing"
    print(f"🔍 Researching: {query}")
    
    try:
        await engine.search(
            query=query,
            report_type="summary",
            tone="Objective",
            domains=["arxiv.org", "nature.com", "quantamagazine.org"],
            show_logs=False
        )
        print("✅ Research completed successfully!")
    except Exception as e:
        print(f"❌ Error during research: {e}")

if __name__ == "__main__":
    asyncio.run(main())
