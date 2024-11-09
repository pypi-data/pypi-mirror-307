
#***********************************************************************************************************
#*************************** WELCOME MESSAGE ****************************************************************
#***********************************************************************************************************

def assoview():
#  pip install mlxtend pandas openpyxl
#  pip install pandas scikit-learn openpyxl matplotlib
  print("**********************************************************")
  print("assoview")
  print()
  print()
  print("Function: arule")
  print("Input file format: MS Excel")
  print("Notes: use the 'Items' for the rules mining")
  # print()
  # print()
  print("**********************************************************")


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



