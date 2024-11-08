from typing import Dict, Any, List, Union
import pandas as pd
from openai import OpenAI
import re

class DataVizGenerator:
    def __init__(self, api_key: str):
        """
        Initialize DataVizGenerator with OpenAI API key.
        
        Parameters:
        -----------
        api_key : str
            Your OpenAI API key
        """
        self.client = OpenAI(api_key=api_key)
        
    def _analyze_column(self, series: pd.Series) -> Dict[str, Any]:
        """Analyze characteristics of DataFrame column"""
        col_info = {
            "dtype": str(series.dtype),
            "n_unique": len(series.unique()),
            "n_missing": series.isna().sum()
        }
        
        try:
            if pd.api.types.is_numeric_dtype(series):
                values = pd.to_numeric(series, errors='coerce')
                col_info.update({
                    "min": float(values.min()),
                    "max": float(values.max()),
                    "mean": float(values.mean()),
                    "type": "numeric"
                })
            else:
                unique_values = series.unique().tolist()
                if len(unique_values) > 10:
                    unique_values = unique_values[:10]
                col_info.update({
                    "unique_values": unique_values,
                    "type": "categorical"
                })
        except Exception as e:
            unique_values = series.unique().tolist()[:10]
            col_info.update({
                "unique_values": unique_values,
                "type": "categorical",
                "error": str(e)
            })
            
        return col_info
    
    def _get_column_info_for_prompt(self, df: pd.DataFrame) -> str:
        """Generate detailed column information for prompt"""
        info = []
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                info.append(f"- {col}: numerik")
            else:
                info.append(f"- {col}: kategorikal")
                unique_vals = df[col].unique().tolist()
                if len(unique_vals) <= 10:
                    info.append(f"  Nilai unik: {unique_vals}")
        
        return "\n".join(info)
    
    def _is_id_column(self, col_name: str) -> bool:
        """Check if column name indicates an ID column"""
        id_indicators = ['id', 'ID', 'Id', '_id', 'number', 'num', 'no']
        return any(indicator in col_name for indicator in id_indicators)
    
    def _generate_context(self, df: pd.DataFrame) -> str:
        """Generate context with additional information"""
        columns_info = {}
        for col in df.columns:
            columns_info[col] = self._analyze_column(df[col])
            
        context = "Informasi DataFrame:\n"
        context += f"- Jumlah baris: {len(df)}\n"
        context += f"- Jumlah kolom: {len(df.columns)}\n\n"
        context += "Detail setiap kolom:\n"
        
        id_columns = [col for col in df.columns if self._is_id_column(col)]
        if id_columns:
            context += "\nPerhatian: Kolom berikut adalah ID (jangan gunakan sebagai nilai numerik):\n"
            context += ", ".join(id_columns) + "\n\n"
        
        for col, info in columns_info.items():
            context += f"\nKolom '{col}':\n"
            context += f"- Tipe data: {info['dtype']}\n"
            context += f"- Jumlah nilai unik: {info['n_unique']}\n"
            context += f"- Nilai kosong: {info['n_missing']}\n"
            
            if info['type'] == 'numeric':
                context += f"- Nilai minimum: {info['min']}\n"
                context += f"- Nilai maksimum: {info['max']}\n"
                context += f"- Rata-rata: {info['mean']}\n"
            else:
                context += "- Beberapa nilai unik: "
                context += f"{', '.join(str(v) for v in info['unique_values'])}\n"
                
        return context

    def _extract_python_code(self, text: str) -> str:
        """Extract Python code from various text formats"""
        code_block_pattern = r'```(?:python)?(.*?)```'
        matches = re.findall(code_block_pattern, text, re.DOTALL)
        
        if matches:
            code = max(matches, key=len).strip()
        else:
            code = text.strip()
            
        return code

    def _clean_code(self, code: str) -> str:
        """Clean code while maintaining indentation"""
        try:
            code = self._extract_python_code(code)
            code = code.replace('`', '')
            
            lines = code.split('\n')
            
            cleaned_lines = []
            for line in lines:
                leading_space = len(line) - len(line.lstrip())
                indent = ' ' * leading_space
                
                cleaned = line.strip()
                
                if cleaned and cleaned not in ['#', '# ']:
                    cleaned_lines.append(indent + cleaned)
            
            required_imports = [
                "import pandas as pd",
                "import matplotlib.pyplot as plt",
                "import seaborn as sns"
            ]
            
            existing_imports = []
            for line in cleaned_lines:
                for imp in required_imports:
                    if imp in line.strip():
                        existing_imports.append(imp)
            
            final_lines = []
            
            for imp in required_imports:
                if imp not in existing_imports:
                    final_lines.append(imp)
            
            if final_lines:
                final_lines.append("")
            
            final_lines.extend(cleaned_lines)
            final_lines.append("")
            
            return '\n'.join(final_lines)
            
        except Exception as e:
            return f"# Error saat membersihkan kode:\n# {str(e)}"
    
    def genvizz(self, df: pd.DataFrame, prompt: str) -> str:
        """
        Generate visualization code based on DataFrame and prompt.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            Input DataFrame to visualize
        prompt : str
            Description of desired visualization in Indonesian
            
        Returns:
        --------
        str
            Generated Python code for visualization
        """
        try:
            context = self._generate_context(df)
            column_info = self._get_column_info_for_prompt(df)
            
            full_prompt = f"""Berdasarkan informasi DataFrame berikut:

{context}

Tipe data setiap kolom:
{column_info}

Aku ingin kamu:
{prompt}

PENTING:
1. Berikan HANYA kode Python murni sederhana yang tidak mungkin error.
2. JANGAN gunakan customerID atau kolom ID lainnya sebagai nilai numerik.
3. Pastikan kode menggunakan variabel 'df'.
4. Jangan define df baru, asumsikan df sudah ter-define sebelumnya.
5. Gunakan label dalam Bahasa Indonesia.
6. Tambahkan title dan label yang informatif.
7. Tangani data kategorik dan numerik dengan benar.
8. Pastikan semua kolom yang digunakan ada dalam DataFrame.
"""

            completion = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Changed model here
                messages=[
                    {
                        "role": "system", 
                        "content": "Anda adalah expert Python data visualization yang fokus pada error prevention. Berikan HANYA kode Python murni tanpa formatting atau penjelasan apapun."
                    },
                    {"role": "user", "content": full_prompt}
                ]
            )
            
            raw_code = completion.choices[0].message.content
            clean_code = self._clean_code(raw_code)
            
            if clean_code.startswith("Error"):
                raise Exception(clean_code)
                
            return clean_code
            
        except Exception as e:
            return f"# Error saat menghasilkan visualisasi:\n# {str(e)}"
