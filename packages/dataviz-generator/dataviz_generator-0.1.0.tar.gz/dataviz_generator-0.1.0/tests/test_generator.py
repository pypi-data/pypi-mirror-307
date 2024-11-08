import pandas as pd
import numpy as np
from dataviz_generator import DataVizGenerator

def test_dataviz_generator():
    # Create sample data
    df = pd.DataFrame({
        'date': pd.date_range(start='2023-01-01', periods=12, freq='M'),
        'sales': np.random.randint(1000, 5000, 12),
        'category': np.random.choice(['A', 'B', 'C'], 12)
    })
    
    # Initialize generator with test API key
    generator = DataVizGenerator(api_key="test-key")
    
    # Test visualization generation
    viz_code = generator.genvizz(df, "Buat visualisasi trend penjualan per bulan")
    
    # Basic checks
    assert isinstance(viz_code, str)
    assert len(viz_code) > 0
    assert "plt" in viz_code
    assert "df" in viz_code
    assert not viz_code.startswith("# Error")

if __name__ == '__main__':
    test_dataviz_generator()
