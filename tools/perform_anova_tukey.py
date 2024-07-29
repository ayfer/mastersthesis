import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import sys

def perform_anova_tukey(input_file, output_file, matrix_output_file):
    # Load the provided Excel file
    data = pd.read_excel(input_file)

    # Automatically identify the ID column and value columns
    id_var = data.columns[0]
    value_vars = data.columns[1:]

    # Reshape the data to long format
    data_long = pd.melt(data, id_vars=[id_var], value_vars=value_vars)
    data_long.columns = ['Group', 'Test', 'Value']

    # Perform ANOVA
    model = ols('Value ~ Group', data=data_long).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    # Perform Tukey's HSD test
    tukey = pairwise_tukeyhsd(endog=data_long['Value'], groups=data_long['Group'], alpha=0.05)

    # Convert Tukey HSD results to a DataFrame
    tukey_results_df = pd.DataFrame(data=tukey._results_table.data[1:], columns=tukey._results_table.data[0])

    # Save the Tukey HSD results to an Excel file
    tukey_results_df.to_excel(output_file, index=False)
    print(f"Tukey HSD results saved to {output_file}")

    # Create a matrix to show significant differences
    groups = sorted(data_long['Group'].unique())
    matrix = pd.DataFrame(index=groups, columns=groups, data='')

    for row in tukey_results_df.itertuples():
        group1, group2, reject = row.group1, row.group2, row.reject
        significance = '' if reject else 'Not Significant'
        matrix.at[group1, group2] = significance
        matrix.at[group2, group1] = significance

    # Fill diagonal with 'NA' since a group is not compared with itself
    for group in groups:
        matrix.at[group, group] = 'na'

    # Save the matrix to an Excel file
    matrix.to_excel(matrix_output_file)
    print(f"Significance matrix saved to {matrix_output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script_name.py input_file.xlsx output_file.xlsx matrix_output_file.xlsx")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        matrix_output_file = sys.argv[3]
        perform_anova_tukey(input_file, output_file, matrix_output_file)

