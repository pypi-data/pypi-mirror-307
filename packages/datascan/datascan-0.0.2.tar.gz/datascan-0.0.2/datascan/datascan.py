
#***********************************************************************************************************
#*************************** WELCOME MESSAGE ****************************************************************
#***********************************************************************************************************

def datascan():
#  pip install mlxtend pandas openpyxl
#  pip install pandas scikit-learn openpyxl matplotlib
  print("**********************************************************")
  print("Welcome to use datascan *: an analytics solution")
  print()
  print("Get ready to power up your data journey with datascan!")
  print("**********************************************************")
  print()
  print("Contacts:")
  print()
  print("Dr Anna Sung - email: a.sung@chester.ac.uk")
  print("Prof Kelvin Leong - email: k.leong@chester.ac.uk")
  print()
  print("subpackages: arule01, arule, cluster, dtree, linear, temporal, test, liquidity, profitability, solvency")
  # print()
  # print()
  print("**********************************************************")


#SUBPACKAGE: temporal---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: identify basic temporal patterns with autocorrelation (which lag =1)
#***********************************************************************************************************
def temporal():
  import pandas as pd
  import matplotlib.pyplot as plt
  from statsmodels.tsa.seasonal import seasonal_decompose
  from statsmodels.graphics.tsaplots import plot_acf
  from statsmodels.tsa.stattools import acf
  from google.colab import files
  import numpy as np
  from scipy.stats import linregress

  # Step 1: Allow the user to upload an Excel file
  uploaded = files.upload()

  # Step 2: Load the Excel file into a pandas DataFrame
  # Assuming the time series data is in the first sheet, and the first column contains the date, second column contains the values.
  file_name = list(uploaded.keys())[0]
  df = pd.read_excel(file_name)

  # Display the first few rows to verify data
  print("Data Preview:")
  print(df.head())

  # Convert the first column to datetime if it's not already
  df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])

  # Set the first column as the index (time)
  df.set_index(df.columns[0], inplace=True)

  # Step 3: Plot the time series to visualize the data
  plt.figure(figsize=(10,6))
  plt.plot(df, label='Time Series')
  plt.title('Time Series Data')
  plt.xlabel('Date')
  plt.ylabel('Values')
  plt.legend()
  plt.show()

  # Brief explanation of the time series plot
  print("\n### Time Series Plot Discussion ###")
  print("This plot shows the raw time series data over time. From this chart, you can observe the overall trend and variations in the data. "
        "If there's an upward or downward movement, it indicates a trend. If you notice recurring peaks and troughs at regular intervals, "
        "there may be seasonality. For now, we only see a general trend.\n")

  # Step 4: Decompose the time series into trend, seasonality, and residuals
  # This works if the data has more than one complete season
  decompose_result = seasonal_decompose(df, model='additive', period=12)  # Adjust the period to match your data's seasonality

  # Plot the decomposition
  decompose_result.plot()
  plt.show()

  # Extract the trend, seasonal, and residual components
  trend = decompose_result.trend.dropna()
  seasonal = decompose_result.seasonal.dropna()
  residual = decompose_result.resid.dropna()

  # Display summary statistics for trend, seasonality, and residual components
  trend_mean = trend.mean()
  seasonal_mean = seasonal.mean()
  residual_mean = residual.mean()

  # Step 4.1: Calculate the slope of the trend
  slope, intercept, r_value, p_value, std_err = linregress(range(len(trend)), trend)

  print("\n### Decomposition Quantified Results ###")
  # print(f"1. **Trend Mean**: {trend_mean:.2f}")
  print(f"2. **Trend Slope**: {slope:.2f}")
  print(f"3. **Seasonality Mean**: {seasonal_mean:.2f}")
  print(f"4. **Residual Mean**: {residual_mean:.2f}")

  # Conclusions based on the figures
  print("\n### Conclusions ###")
  if slope > 0:
      print(f"The trend component shows an increasing pattern with a positive slope of {slope:.2f}")
  elif slope < 0:
      print(f"The trend component shows a decreasing pattern with a negative slope of {slope:.2f}")
  else:
      print(f"The trend is relatively flat, with a slope of {slope:.2f} ")

  if seasonal_mean != 0:
      print(f"The seasonality component has a mean of {seasonal_mean:.2f}, which suggests { 'regular repeating patterns' if seasonal_mean > 0 else 'less significant seasonality'}.")
  else:
      print("There is no strong seasonality detected in the time series.")

  if residual_mean == 0:
      print("The residual (noise) component has a mean of 0, indicating that the noise is balanced around the time series.")
  else:
      print(f"The residual component has a mean of {residual_mean:.2f}, which indicates there may be a slight bias in the noise component.")

  """    
  # Step 5: Plot the autocorrelation function to check for patterns
  plot_acf(df, lags=12)  # Limiting to 12 lags for visualization
  plt.show()
  """

  # Step 6: Calculate the autocorrelations and show the values for key lags
  autocorrelations = acf(df.iloc[:, 0], nlags=12)  # Calculate autocorrelations for up to 12 lags

  """
  # Display the autocorrelations for the first few lags
  print("\n### Autocorrelation Quantified Results ###")
  for i, autocorr in enumerate(autocorrelations):
      print(f"Lag {i}: {autocorr:.2f}")
  """

  # Conclusions based on autocorrelations
  print("\n### Autocorrelation Conclusions ###")
  strong_lag = np.argmax(np.abs(autocorrelations[1:])) + 1  # Find the strongest autocorrelation lag (excluding lag 0)

  # Analyze the highest autocorrelation
  strong_autocorr_value = autocorrelations[strong_lag]

  if strong_autocorr_value > 0.5:
      print(f"There is a strong positive correlation, with an autocorrelation value of {strong_autocorr_value:.2f}. "
            "This indicates that the values of the time series are strongly related, suggesting repeating patterns or seasonality.")
  elif strong_autocorr_value < -0.5:
      print(f"There is a strong negative correlation, with an autocorrelation value of {strong_autocorr_value:.2f}. "
            "This indicates that the values of the time series are negatively related, suggesting an inverse pattern.")
  else:
      print(f"The highest autocorrelation, with a value of {strong_autocorr_value:.2f}, "
            "which suggests weak or moderate autocorrelation. This indicates that the time series does not have strong dependencies.")



#SUBPACKAGE: arule01---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: association tree will be created for data input as 0 1 format
#***********************************************************************************************************
def arule01():
  import pandas as pd
  from mlxtend.frequent_patterns import apriori, association_rules
  from google.colab import files

  # Allow the user to upload the file
  uploaded = files.upload()

  # Assume only one file is uploaded, get the file name
  file_name = list(uploaded.keys())[0]

  # Load the dataset from the uploaded file
  df = pd.read_excel(file_name)

  # Display the dataset
  print("Dataset:")
  print(df)

  # Remove 'Transaction' column if it exists
  if 'Transaction' in df.columns:
      df = df.drop(columns=['Transaction'])

  # Prompt the user to input the minimum support value
  while True:
      try:
          min_support = float(input("Please enter the minimum support value (less than 1):\n "))
          if min_support <= 0 or min_support >= 1:
              raise ValueError("The value must be between 0 and 1 (exclusive).")
          break
      except ValueError as e:
          print(e)

  # Perform Apriori algorithm to find frequent itemsets
  frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)

  # Display the frequent itemsets
  print("\nFrequent Itemsets:")
  print(frequent_itemsets)

  # Generate the association rules
  rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

  # Display the association rules
  print("\nAssociation Rules:")
  print(rules)

#SUBPACKAGE: arule---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: association tree will be created for data input as text (e.g. milk, chips, cake)
#***********************************************************************************************************
def arule():
  import pandas as pd 
  from mlxtend.frequent_patterns import apriori, association_rules
  from google.colab import files

  # Allow the user to upload the file
  uploaded = files.upload()

  # Assume only one file is uploaded, get the file name
  file_name = list(uploaded.keys())[0]

  # Load the dataset from the uploaded file
  df = pd.read_excel(file_name)

  # Display the dataset
  print("Original Dataset:")
  print(df)

  # Split the items into lists and create a one-hot encoded DataFrame
  df['Items'] = df['Items'].str.split(', ')

  # One-hot encode the items
  df_onehot = df['Items'].str.join('|').str.get_dummies()

  # Display the one-hot encoded DataFrame
  print("\nOne-Hot Encoded Dataset:")
  print(df_onehot)

  # Prompt the user to input the minimum support value
  while True:
      try:
          min_support = float(input("Please enter the minimum support value (less than 1):\n "))
          if min_support <= 0 or min_support >= 1:
              raise ValueError("The value must be between 0 and 1 (exclusive).")
          break
      except ValueError as e:
          print(e)

  # Perform Apriori algorithm to find frequent itemsets
  frequent_itemsets = apriori(df_onehot, min_support=min_support, use_colnames=True)

  # Display the frequent itemsets
  print("\nFrequent Itemsets:")
  print(frequent_itemsets)

  # Generate the association rules
  rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

  # Display the association rules
  print("\nAssociation Rules:")
  print(rules)

  # Select only the columns required and rename them
  rules_filtered = rules[['antecedents', 'consequents', 'support', 'confidence']].copy()
  rules_filtered.columns = ['If', 'Then', 'Support', 'Confidence']

  # Convert frozen sets to strings for easier readability
  rules_filtered['If'] = rules_filtered['If'].apply(lambda x: ', '.join(list(x)))
  rules_filtered['Then'] = rules_filtered['Then'].apply(lambda x: ', '.join(list(x)))

  # Sort the DataFrame by confidence in descending order
  rules_filtered = rules_filtered.sort_values(by='Confidence', ascending=False)

  # Save the sorted rules to an Excel file
  output_file = 'association_rules_output.xlsx'
  rules_filtered.to_excel(output_file, index=False)

  # Download the file to local system
  files.download(output_file)

  print("\nThe association rules have been saved to 'association_rules_output.xlsx', sorted by confidence, and are available for download.")


#SUBPACKAGE: cluster---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: conduct clustering analysis
#***********************************************************************************************************
def cluster():
  # Import necessary libraries
  import pandas as pd
  from sklearn.cluster import KMeans
  from sklearn.preprocessing import StandardScaler, OneHotEncoder
  from sklearn.compose import ColumnTransformer
  from sklearn.pipeline import Pipeline
  import matplotlib.pyplot as plt
  from google.colab import files

  # Step 1: Upload the Excel file
  print("Please upload your Excel file:")
  uploaded = files.upload()

  # Step 2: Load the Excel file into a Pandas DataFrame
  df = pd.read_excel(list(uploaded.keys())[0])

  # Display the first few rows of the dataset
  print("\nHere is a preview of your dataset:")
  print(df.head())

  # Step 3: Allow users to choose the number of clusters
  print("\nHow many clusters would you like to create?")
  num_clusters = int(input("> "))  # User input on the next line

  # Step 4: Allow users to select columns for clustering
  print("\nAvailable columns in the dataset:")
  print(df.columns)
  print("\nEnter the column names to use for clustering (separated by commas):")
  columns = input("> ").split(',')  # User input on the next line

  # Step 5: Prepare the selected data for clustering
  selected_data = df[columns]

  # Step 6: Identify categorical and continuous columns
  categorical_cols = selected_data.select_dtypes(include=['object', 'category']).columns
  continuous_cols = selected_data.select_dtypes(include=['float64', 'int64']).columns

  # Step 7: Create a preprocessing pipeline
  # Scale continuous data and one-hot encode categorical data
  preprocessor = ColumnTransformer(
      transformers=[
          ('num', StandardScaler(), continuous_cols),
          ('cat', OneHotEncoder(), categorical_cols)
      ])

  # Step 8: Create a pipeline to preprocess the data and apply KMeans
  pipeline = Pipeline(steps=[
      ('preprocessor', preprocessor),
      ('kmeans', KMeans(n_clusters=num_clusters))
  ])

  # Fit the pipeline to the data
  pipeline.fit(selected_data)

  # Get the cluster labels
  cluster_labels = pipeline.named_steps['kmeans'].labels_

  # Step 9: Add the cluster labels to the original DataFrame
  df['Cluster'] = cluster_labels

  # Display the DataFrame with the cluster labels
  print("\nHere is your dataset with the assigned cluster labels:")
  print(df.head())

  # Step 10: Visualize the Clusters (optional: if you selected two numeric columns)
  if len(continuous_cols) == 2:
      plt.scatter(df[continuous_cols[0]], df[continuous_cols[1]], c=df['Cluster'], cmap='viridis')
      plt.xlabel(continuous_cols[0])
      plt.ylabel(continuous_cols[1])
      plt.title(f'K-Means Clustering with {num_clusters} clusters')
      plt.show()

  # Step 11: Save the DataFrame with the cluster labels into a new Excel file
  output_file = "clustered_data.xlsx"
  df.to_excel(output_file, index=False)

  # Step 12: Allow the user to download the new Excel file
  print(f"\nThe file '{output_file}' has been created and is ready for download.")
  files.download(output_file)


#SUBPACKAGE: dtree---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: conduct clustering analysis for data input as text type
#***********************************************************************************************************
def dtree():
  import pandas as pd
  from sklearn.model_selection import train_test_split
  from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, plot_tree, export_text
  from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
  from sklearn.preprocessing import LabelEncoder
  import matplotlib.pyplot as plt
  from google.colab import files

  # Upload the Excel file
  uploaded = files.upload()

  # Load the uploaded Excel file into a pandas DataFrame
  file_name = list(uploaded.keys())[0]
  data = pd.read_excel(file_name)

  # Display the first few rows of the dataset
  print("Dataset Preview:")
  print(data.head())

  # Ask user to input feature columns and target column
  print("\nFeature (X) and Target (y) Selection:")
  print("***********************************************************************")
  print("Features (X) are the independent variables used to predict the target.")
  print("Target (y) is the dependent variable that we are trying to predict.")
  print("***********************************************************************")

  # Display column names to help user choose
  print("\nAvailable columns in the dataset:")
  print(data.columns)

  # User input for features and target
  features = input("\nEnter the column names for features (X) separated by commas: \n").split(',')
  features = [feature.strip() for feature in features]
  print(f"\nYou selected features: {features}")

  target = input("\nEnter the column name for the target (y): \n").strip()
  print(f"\nYou selected target: {target}")

  # Split data into features (X) and target (y)
  X = data[features]
  y = data[target]

  # Test size input and explanation
  print("\nTest Size Selection:")
  test_size = float(input("\nEnter the test size as a fraction (e.g., 0.3 for 30% test size): \n"))
  print(f"\nYou selected a test size of: {test_size}")

  # Handle categorical features in X
  categorical_features = X.select_dtypes(include=['object', 'category']).columns
  if len(categorical_features) > 0:
      X_encoded = pd.get_dummies(X, columns=categorical_features)
      print(f"\nCategorical features found and one-hot encoded: {list(categorical_features)}")
      print("\nEncoded feature mapping (columns):")
      print(X_encoded.columns)
      X = X_encoded
  else:
      X_encoded = X

  # Detect if the target is categorical or continuous
  is_classification = False
  target_column_name = target  # Dynamic column heading for predicted target in Excel
  if pd.api.types.is_numeric_dtype(y):
      print("\nThe target is continuous. Performing regression analysis.")
      model = DecisionTreeRegressor(random_state=42)
  else:
      print("\nThe target is categorical. Performing classification analysis.")
      le = LabelEncoder()
      y_encoded = le.fit_transform(y)
      print("\nEncoded labels for target classes:")
      class_labels = le.classes_  # For mapping encoded labels back to class names
      print(pd.DataFrame({"Class": le.classes_, "Encoded": range(len(le.classes_))}))
      y = y_encoded
      model = DecisionTreeClassifier(random_state=42)
      is_classification = True

  # Split the dataset into training and testing sets
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

  # Train the model
  model.fit(X_train, y_train)

  # Predict on the test set
  y_pred = model.predict(X_test)

  # Evaluate the model
  if is_classification:
      accuracy = accuracy_score(y_test, y_pred)
      print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
  else:
      mse = mean_squared_error(y_test, y_pred)
      r2 = r2_score(y_test, y_pred)
      print("\nModel Evaluation Metrics:")
      print(f"Mean Squared Error: {mse}")
      print(f"R-squared: {r2}")

  # Display the Decision Tree diagram
  plt.figure(figsize=(12, 8))
  plot_tree(model, feature_names=X.columns, filled=True)
  plt.show()

  # Generate human-readable rules with "Yes/No" labels for binary columns
  def get_decision_tree_rules(model, X, y, is_classification):
      node_indicator = model.decision_path(X)
      leaf_id = model.apply(X)

      rules = []
      for sample_id in range(len(X)):
          rule = []
          for node_id in node_indicator.indices[node_indicator.indptr[sample_id]:node_indicator.indptr[sample_id + 1]]:
              if leaf_id[sample_id] == node_id:
                  continue
              feature_index = model.tree_.feature[node_id]
              threshold = model.tree_.threshold[node_id]
              feature_name = X.columns[feature_index]

              # Check if the feature is binary (0 or 1 from one-hot encoding)
              if X[feature_name].nunique() == 2 and set(X[feature_name].unique()) <= {0, 1}:
                  # Interpret <= 0.5 as "No" and > 0.5 as "Yes"
                  if X.iloc[sample_id, feature_index] <= 0.5:
                      condition = f"is {feature_name}: No"
                  else:
                      condition = f"is {feature_name}: Yes"
              else:
                  # For continuous features, display threshold-based conditions
                  if X.iloc[sample_id, feature_index] <= threshold:
                      condition = f"{feature_name} <= {threshold:.2f}"
                  else:
                      condition = f"{feature_name} > {threshold:.2f}"

              rule.append(condition)

          # Convert predicted target to class name if classification
          predicted_value = model.predict(X.iloc[[sample_id]])[0]
          if is_classification:
              predicted_value = class_labels[predicted_value]  # Map encoded value to class name

          rules.append({
              "Sample": sample_id,
              "Decision Path": " AND ".join(rule),
              target_column_name: predicted_value  # Use dynamic column name for target
          })
      return rules

  # Generate and display the decision tree rules with predicted target values
  rules = get_decision_tree_rules(model, X_train, y_train, is_classification)
  rules_df = pd.DataFrame(rules)
  print(f"\nTabular Decision Tree Rules (Sample Paths with Predicted {target_column_name}):")
  print(rules_df.head())

  # Save rules to an Excel file
  output_file = "Decision_Tree_Rules_with_Targets.xlsx"
  rules_df.to_excel(output_file, index=False)
  print(f"\nThe decision tree rules have been saved as '{output_file}'.")

  # Allow the user to download the file in Google Colab
  files.download(output_file)

  # Display text representation of the tree for detailed rules
  print("\nDetailed Decision Tree Rules:")
  print(export_text(model, feature_names=list(X.columns)))

  # Display brief summary of tree structure
  n_nodes = model.tree_.node_count
  max_depth = model.tree_.max_depth
  print(f"\nThe decision tree has {n_nodes} nodes and a maximum depth of {max_depth}.")

  # Short conclusion based on model evaluation
  if is_classification:
      if accuracy > 0.8:
          print("\nConclusion: The model has a high accuracy, indicating that it performs well on this dataset.")
      elif accuracy > 0.6:
          print("\nConclusion: The model has moderate accuracy. It performs decently, but there is room for improvement.")
      else:
          print("\nConclusion: The model has low accuracy, and its predictions may not be reliable.")
  else:
      if r2 > 0.8:
          print("\nConclusion: The model explains most of the variance in the data and performs well.")
      elif r2 > 0.6:
          print("\nConclusion: The model explains a decent amount of variance, but there is room for improvement.")
      else:
          print("\nConclusion: The model does not explain much of the variance, and its predictions may not be very accurate.")




#SUBPACKAGE: test---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: conduct varoious statistic tests
#***********************************************************************************************************
def test():
  import pandas as pd
  import numpy as np
  from scipy import stats
  import seaborn as sns
  import matplotlib.pyplot as plt
  from google.colab import files
  import io

  # Step 1: Upload the Excel file
  uploaded = files.upload()

  # Step 2: Load the Excel file into a DataFrame
  df = pd.read_excel(io.BytesIO(uploaded[list(uploaded.keys())[0]]))

  # Step 3: Display the uploaded data
  print("Here is the uploaded data:")
  print(df.head())

  # Step 4: Explain the statistical tests
  print("\nPlease choose a statistical test to perform:")
  print("1. Chi-Square Test: Used to examine the association between two categorical variables.")
  print("2. T-test: Used to compare the means of two groups (independent or paired).")
  print("3. ANOVA: Used to compare the means of three or more groups.")
  print("4. Z-test: Used to compare the means of two groups, typically when the sample size is large or the population variance is known.")

  # Step 5: User chooses the statistical test
  choice = input("\nEnter the number corresponding to your choice (1, 2, 3, or 4):\n")

  # Step 6: User enters the significance level
  alpha = float(input("\nEnter the significance level (e.g., 0.05 for 5% significance):\n"))

  # Step 7: Perform the chosen test and display the results
  if choice == '1':
      # Chi-Square Test
      crosstab = pd.crosstab(df['Group'], df['Measure'])
      chi2, p, dof, expected = stats.chi2_contingency(crosstab)

      print(f"\nChi-Square Test Results:")
      print(f"Chi-Square Statistic: {chi2:.4f}")
      print(f"Degrees of Freedom: {dof}")
      print(f"p-value: {p:.4f}")
      
      if p < alpha:
          print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant association between the Group and Measure variables. This means that the distribution of the Measure variable is different across the different Groups, and the likelihood of this difference being due to chance is low.")
      else:
          print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant association between the Group and Measure variables. This suggests that any observed differences in the distribution of the Measure variable across the Groups could likely be due to chance.")

      print("Note: Chi-Square Test is most appropriate when you have two categorical variables and you want to see if the categories are independent of each other.")
      
      # Plot the results
      sns.countplot(x='Group', hue='Measure', data=df)
      plt.title('Chi-Square Test: Group vs Measure')
      plt.show()

  elif choice == '2':
      # T-test (independent samples)
      groups = df['Group'].unique()
      
      if len(groups) != 2:
          print("Error: T-test requires exactly two groups.")
      else:
          group1 = df[df['Group'] == groups[0]]['Measure']
          group2 = df[df['Group'] == groups[1]]['Measure']
          
          t_stat, p = stats.ttest_ind(group1, group2)
          
          print(f"\nT-test Results:")
          print(f"T-statistic: {t_stat:.4f}")
          print(f"p-value: {p:.4f}")
          
          if p < alpha:
              print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant difference in the means of {groups[0]} and {groups[1]}. This suggests that the observed difference in means is unlikely to have occurred by chance.")
          else:
              print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant difference in the means of {groups[0]} and {groups[1]}. This implies that any observed difference in means could likely be due to chance.")

          print("Note: The T-test assumes that the data in each group is normally distributed and that the variances in the two groups are equal.")
          
          # Plot the results
          sns.boxplot(x='Group', y='Measure', data=df)
          plt.title('T-test: Group vs Measure')
          plt.show()

  elif choice == '3':
      # ANOVA
      f_stat, p = stats.f_oneway(*(df[df['Group'] == group]['Measure'] for group in df['Group'].unique()))

      print(f"\nANOVA Results:")
      print(f"F-statistic: {f_stat:.4f}")
      print(f"p-value: {p:.4f}")
      
      if p < alpha:
          print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant difference in means across the groups. This suggests that at least one group mean is significantly different from the others.")
      else:
          print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant difference in means across the groups. This suggests that any observed differences in means are likely due to chance.")

      print("Note: ANOVA assumes that the data in each group is normally distributed and that the variances across the groups are equal. If you find a significant result, post-hoc tests can be conducted to determine which specific groups differ from each other.")
      
      # Plot the results
      sns.boxplot(x='Group', y='Measure', data=df)
      plt.title('ANOVA: Group vs Measure')
      plt.show()

  elif choice == '4':
      # Z-test
      groups = df['Group'].unique()
      
      if len(groups) != 2:
          print("Error: Z-test requires exactly two groups.")
      else:
          group1 = df[df['Group'] == groups[0]]['Measure']
          group2 = df[df['Group'] == groups[1]]['Measure']
          
          mean1 = np.mean(group1)
          mean2 = np.mean(group2)
          std1 = np.std(group1, ddof=1)
          std2 = np.std(group2, ddof=1)
          n1 = len(group1)
          n2 = len(group2)
          
          # Calculate the Z-statistic
          z_stat = (mean1 - mean2) / np.sqrt((std1**2/n1) + (std2**2/n2))
          p = stats.norm.sf(abs(z_stat)) * 2  # two-tailed p-value
          
          print(f"\nZ-test Results:")
          print(f"Z-statistic: {z_stat:.4f}")
          print(f"p-value: {p:.4f}")
          
          if p < alpha:
              print(f"Interpretation: The p-value is less than {alpha}, indicating a statistically significant difference in the means of {groups[0]} and {groups[1]}. This suggests that the observed difference in means is unlikely to have occurred by chance.")
          else:
              print(f"Interpretation: The p-value is greater than {alpha}, indicating no statistically significant difference in the means of {groups[0]} and {groups[1]}. This implies that any observed difference in means could likely be due to chance.")

          print("Note: The Z-test is generally used when the sample size is large or when the population variance is known. It assumes that the data in each group is normally distributed.")
          
          # Plot the results
          sns.boxplot(x='Group', y='Measure', data=df)
          plt.title('Z-test: Group vs Measure')
          plt.show()

  else:
      print("Invalid choice. Please restart and select a valid option.")

#SUBPACKAGE: linear---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions: conduct linear programming
#***********************************************************************************************************
def linear():
  import pandas as pd
  import numpy as np
  from scipy.optimize import linprog
  from google.colab import files

  # Step 1: Upload the Excel file
  uploaded = files.upload()

  # Step 2: Load the Excel file into a Pandas DataFrame
  file_name = list(uploaded.keys())[0]
  df = pd.read_excel(file_name)

  # Display the uploaded data
  print("Uploaded Data:")
  print(df.head())

  # Step 3: Extract necessary data from the DataFrame
  # Assuming the Excel file has columns 'Asset', 'Expected Return', and 'Risk' (standard deviation)

  assets = df['Asset'].tolist()
  expected_returns = df['Expected Return'].to_numpy()
  risks = df['Risk'].to_numpy()

  # Number of assets
  n = len(assets)

  # Step 4: Define the Linear Programming problem

  # Objective: Maximize the expected return (minimize the negative expected return)
  c = -expected_returns

  # Constraints:
  # 1. Sum of the weights must equal 1 (fully invested portfolio)
  A_eq = [np.ones(n)]
  b_eq = [1]

  # 2. Add any additional constraints (e.g., limits on individual asset allocation, etc.)
  # For simplicity, we do not add additional constraints here

  # Bounds: Each weight should be between 0 and 1
  bounds = [(0, 1) for _ in range(n)]

  # Step 5: Solve the Linear Programming problem
  result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

  # Extract the optimal weights
  optimal_weights = result.x

  # Step 6: Display the results
  optimal_portfolio = pd.DataFrame({
      'Asset': assets,
      'Optimal Weight': optimal_weights
  })

  print("\nOptimal Portfolio Allocation:")
  print(optimal_portfolio)

  # Display the DataFrame in a more readable format in Google Colab
  from IPython.display import display
  display(optimal_portfolio)
  
#SUBPACKAGE: liquidity---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions include:
# allow user to upload an excel file and then fstar will conduct liquidity ratio analysis 
#***********************************************************************************************************
def liquidity():
  from google.colab import files
  import io

  # Upload Excel file
  print("Please upload the Excel file containing company information:")
  uploaded = files.upload()

  # Load the Excel file into a DataFrame
  for file_name in uploaded.keys():
      df = pd.read_excel(io.BytesIO(uploaded[file_name]))

  # Display the first few rows of the DataFrame to understand the structure
  print("Here are the first few rows of the uploaded data:")
  print(df.head())

  # Prepare a list to store missing columns and calculations
  missing_columns = []
  calculated_ratios = []

  # Conduct liquidity and solvency analysis by calculating key ratios
  if 'Current Assets' in df.columns and 'Current Liabilities' in df.columns:
      df['Current Ratio'] = df['Current Assets'] / df['Current Liabilities']
      calculated_ratios.append('Current Ratio')
  else:
      missing_columns.append('Current Ratio')

  if 'Current Assets' in df.columns and 'Inventory' in df.columns and 'Current Liabilities' in df.columns:
      df['Quick Ratio'] = (df['Current Assets'] - df['Inventory']) / df['Current Liabilities']
      calculated_ratios.append('Quick Ratio')
  else:
      missing_columns.append('Quick Ratio')

  if 'Cash and Cash Equivalents' in df.columns and 'Current Liabilities' in df.columns:
      df['Cash Ratio'] = df['Cash and Cash Equivalents'] / df['Current Liabilities']
      calculated_ratios.append('Cash Ratio')
  else:
      missing_columns.append('Cash Ratio')

  if 'Current Assets' in df.columns and 'Current Liabilities' in df.columns:
      df['Working Capital'] = df['Current Assets'] - df['Current Liabilities']
      calculated_ratios.append('Working Capital')
  else:
      missing_columns.append('Working Capital')

  if 'Total Liabilities' in df.columns and 'Equity' in df.columns:
      df['Debt to Equity Ratio'] = df['Total Liabilities'] / df['Equity']
      calculated_ratios.append('Debt to Equity Ratio')
  else:
      missing_columns.append('Debt to Equity Ratio')

  if 'EBIT' in df.columns and 'Interest Expense' in df.columns:
      df['Interest Coverage Ratio'] = df['EBIT'] / df['Interest Expense']
      calculated_ratios.append('Interest Coverage Ratio')
  else:
      missing_columns.append('Interest Coverage Ratio')

  if 'Operating Cash Flow' in df.columns and 'Current Liabilities' in df.columns:
      df['Operating Cash Flow Ratio'] = df['Operating Cash Flow'] / df['Current Liabilities']
      calculated_ratios.append('Operating Cash Flow Ratio')
  else:
      missing_columns.append('Operating Cash Flow Ratio')

  # Display a message for missing columns
  if missing_columns:
      print("\nThe following ratios could not be calculated due to missing columns:")
      for ratio in missing_columns:
          print(f"- {ratio}")

#SUBPACKAGE: profitability---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions include:
# allow user to upload an excel file and then fstar will conduct profitability ratio analysis 
#***********************************************************************************************************
def profitability():
  from google.colab import files
  import io

  # Upload Excel file
  print("Please upload the Excel file containing company information:")
  uploaded = files.upload()

  # Load the Excel file into a DataFrame
  for file_name in uploaded.keys():
      df = pd.read_excel(io.BytesIO(uploaded[file_name]))

  # Display the first few rows of the DataFrame to understand the structure
  print("Here are the first few rows of the uploaded data:")
  print(df.head())

  # Prepare a list to store missing columns and calculations
  missing_columns = []
  calculated_ratios = []

  # Conduct profitability analysis by calculating key ratios
  if 'Revenue' in df.columns and 'Cost of Goods Sold' in df.columns:
      df['Gross Profit Margin'] = (df['Revenue'] - df['Cost of Goods Sold']) / df['Revenue']
      calculated_ratios.append('Gross Profit Margin')
  else:
      missing_columns.append('Gross Profit Margin')

  if 'Operating Income' in df.columns and 'Revenue' in df.columns:
      df['Operating Profit Margin'] = df['Operating Income'] / df['Revenue']
      calculated_ratios.append('Operating Profit Margin')
  else:
      missing_columns.append('Operating Profit Margin')

  if 'Net Income' in df.columns and 'Revenue' in df.columns:
      df['Net Profit Margin'] = df['Net Income'] / df['Revenue']
      calculated_ratios.append('Net Profit Margin')
  else:
      missing_columns.append('Net Profit Margin')

  if 'Net Income' in df.columns and 'Total Assets' in df.columns:
      df['Return on Assets (ROA)'] = df['Net Income'] / df['Total Assets']
      calculated_ratios.append('Return on Assets (ROA)')
  else:
      missing_columns.append('Return on Assets (ROA)')

  if 'Net Income' in df.columns and 'Equity' in df.columns:
      df['Return on Equity (ROE)'] = df['Net Income'] / df['Equity']
      calculated_ratios.append('Return on Equity (ROE)')
  else:
      missing_columns.append('Return on Equity (ROE)')

  # Display a message for missing columns
  if missing_columns:
      print("\nThe following ratios could not be calculated due to missing columns:")
      for ratio in missing_columns:
          print(f"- {ratio}")

  # Display the resulting DataFrame with the calculated ratios
  if calculated_ratios:
      print("\nRatios have been calculated. Here is the updated DataFrame with the key ratios:\n")
      print(df[['Company Name'] + calculated_ratios])

      # Plotting the ratios for each company
      for ratio in calculated_ratios:
          plt.figure(figsize=(10, 6))
          plt.bar(df['Company Name'], df[ratio], color='lightgreen')
          plt.title(f'{ratio} Analysis')
          plt.xlabel('Company Name')
          plt.ylabel(ratio)
          plt.grid(True, axis='y', linestyle='--', alpha=0.7)
          plt.show()

  # Print the ratio explanations for the calculated ratios
  if calculated_ratios:
      print("\n### Ratio Explanations ###\n")

  ratios_explanation = {
      "Gross Profit Margin": {
          "Formula": "(Revenue - Cost of Goods Sold) / Revenue",
          "Interpretation": "Measures the percentage of revenue that exceeds the cost of goods sold, indicating how efficiently a company produces and sells its products."
      },
      "Operating Profit Margin": {
          "Formula": "Operating Income / Revenue",
          "Interpretation": "Indicates the percentage of revenue left after deducting operating expenses, showing how well a company manages its core business operations."
      },
      "Net Profit Margin": {
          "Formula": "Net Income / Revenue",
          "Interpretation": "Represents the percentage of revenue that remains as profit after all expenses, taxes, and costs have been deducted. A higher margin indicates better profitability."
      },
      "Return on Assets (ROA)": {
          "Formula": "Net Income / Total Assets",
          "Interpretation": "Measures how efficiently a company uses its assets to generate profit. A higher ROA indicates more efficient asset use."
      },
      "Return on Equity (ROE)": {
          "Formula": "Net Income / Equity",
          "Interpretation": "Assesses the profitability relative to shareholders' equity. A higher ROE indicates better returns on investment for shareholders."
      }
  }

  for ratio in calculated_ratios:
      if ratio in ratios_explanation:
          details = ratios_explanation[ratio]
          print(f"{ratio}:\n  Formula: {details['Formula']}\n  Interpretation: {details['Interpretation']}\n")

  # Optionally, save the DataFrame with the new columns to a new Excel file
  if calculated_ratios:
      output_file = "profitability_analysis.xlsx"
      df.to_excel(output_file, index=False)
      print(f"Profitability analysis has been saved to {output_file}")

      # Allow the user to download the result file
      files.download(output_file)

#SUBPACKAGE: solvency---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
# functions include:
# allow user to upload an excel file and then fstar will conduct solvency ratio analysis 
#***********************************************************************************************************
def solvency():
  from google.colab import files
  import io
  # Upload Excel file
  print("Please upload the Excel file containing company information:")
  uploaded = files.upload()

  # Load the Excel file into a DataFrame
  for file_name in uploaded.keys():
      df = pd.read_excel(io.BytesIO(uploaded[file_name]))

  # Display the first few rows of the DataFrame to understand the structure
  print("Here are the first few rows of the uploaded data:")
  print(df.head())

  # Prepare a list to store missing columns and calculations
  missing_columns = []
  calculated_ratios = []

  # Conduct solvency analysis by calculating key ratios
  if 'Total Liabilities' in df.columns and 'Total Assets' in df.columns:
      df['Debt to Assets Ratio'] = df['Total Liabilities'] / df['Total Assets']
      calculated_ratios.append('Debt to Assets Ratio')
  else:
      missing_columns.append('Debt to Assets Ratio')

  if 'Total Liabilities' in df.columns and 'Equity' in df.columns:
      df['Debt to Equity Ratio'] = df['Total Liabilities'] / df['Equity']
      calculated_ratios.append('Debt to Equity Ratio')
  else:
      missing_columns.append('Debt to Equity Ratio')

  if 'Equity' in df.columns and 'Total Assets' in df.columns:
      df['Equity Ratio'] = df['Equity'] / df['Total Assets']
      calculated_ratios.append('Equity Ratio')
  else:
      missing_columns.append('Equity Ratio')

  if 'EBIT' in df.columns and 'Interest Expense' in df.columns:
      df['Interest Coverage Ratio'] = df['EBIT'] / df['Interest Expense']
      calculated_ratios.append('Interest Coverage Ratio')
  else:
      missing_columns.append('Interest Coverage Ratio')

  if 'Operating Cash Flow' in df.columns and 'Total Debt Service' in df.columns:
      df['Debt Service Coverage Ratio (DSCR)'] = df['Operating Cash Flow'] / df['Total Debt Service']
      calculated_ratios.append('Debt Service Coverage Ratio (DSCR)')
  else:
      missing_columns.append('Debt Service Coverage Ratio (DSCR)')

  # Display a message for missing columns
  if missing_columns:
      print("\nThe following ratios could not be calculated due to missing columns:")
      for ratio in missing_columns:
          print(f"- {ratio}")

  # Display the resulting DataFrame with the calculated ratios
  if calculated_ratios:
      print("\nRatios have been calculated. Here is the updated DataFrame with the key ratios:\n")
      print(df[['Company Name'] + calculated_ratios])

      # Plotting the ratios for each company
      for ratio in calculated_ratios:
          plt.figure(figsize=(10, 6))
          plt.bar(df['Company Name'], df[ratio], color='lightcoral')
          plt.title(f'{ratio} Analysis')
          plt.xlabel('Company Name')
          plt.ylabel(ratio)
          plt.grid(True, axis='y', linestyle='--', alpha=0.7)
          plt.show()

  # Print the ratio explanations for the calculated ratios
  if calculated_ratios:
      print("\n### Ratio Explanations ###\n")

  ratios_explanation = {
      "Debt to Assets Ratio": {
          "Formula": "Total Liabilities / Total Assets",
          "Interpretation": "Indicates the percentage of a company's assets that are financed by debt. A higher ratio suggests higher financial risk."
      },
      "Debt to Equity Ratio": {
          "Formula": "Total Liabilities / Equity",
          "Interpretation": "Measures the degree to which a company is financing its operations through debt versus wholly-owned funds. A higher ratio indicates higher leverage and potentially higher financial risk."
      },
      "Equity Ratio": {
          "Formula": "Equity / Total Assets",
          "Interpretation": "Shows the proportion of a company’s assets that are financed by shareholders’ equity. A higher ratio indicates more reliance on equity financing."
      },
      "Interest Coverage Ratio": {
          "Formula": "EBIT / Interest Expense",
          "Interpretation": "Indicates how easily a company can pay interest on its outstanding debt. A higher ratio suggests the company is more capable of meeting its interest obligations."
      },
      "Debt Service Coverage Ratio (DSCR)": {
          "Formula": "Operating Cash Flow / Total Debt Service",
          "Interpretation": "Measures the cash flow available to pay current debt obligations. A higher DSCR indicates better ability to service debt."
      }
  }

  for ratio in calculated_ratios:
      if ratio in ratios_explanation:
          details = ratios_explanation[ratio]
          print(f"{ratio}:\n  Formula: {details['Formula']}\n  Interpretation: {details['Interpretation']}\n")

  # Optionally, save the DataFrame with the new columns to a new Excel file
  if calculated_ratios:
      output_file = "solvency_analysis.xlsx"
      df.to_excel(output_file, index=False)
      print(f"Solvency analysis has been saved to {output_file}")

      # Allow the user to download the result file
      files.download(output_file)
