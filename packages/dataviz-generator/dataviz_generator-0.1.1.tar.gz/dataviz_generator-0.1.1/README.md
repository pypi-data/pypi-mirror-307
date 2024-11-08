# DataVizGenerator

DataVizGenerator is an AI-powered data visualization tool that automatically generates appropriate visualizations based on data characteristics and user requirements using OpenAI's GPT models.

## Installation

```bash
pip install dataviz-generator
```

## Quick Start

```python
from dataviz_generator import DataVizGenerator
import pandas as pd

# Initialize with your OpenAI API key
generator = DataVizGenerator(api_key="your-api-key")

# Load your data
df = pd.read_csv("your_data.csv")

# Generate visualization code
viz_code = generator.genvizz(df, "Create complete EDA from this data.")

# Execute the generated code
exec(viz_code)
```

## Features

- Automatic data analysis and visualization suggestion
- Smart column type detection
- ID column identification and handling
- Comprehensive error handling
- Clean code generation with proper styling
