import pandas as pd
import ast


savable = pd.read_csv("savable.csv", encoding='utf-8')
altmetric = pd.read_csv("Altmetric.csv", encoding='utf-8')
'''
altmetric is the only file where the doi doesn't start with https://doi.org/, so merges on doi wouldn't work.
hence we add https://doi.org/ 
'''
altmetric['DOI'] = altmetric['DOI'].apply(lambda x: "https://doi.org/" + str(x) if x else x)
print(altmetric['DOI'].head(5))

overton = pd.read_csv("overton_data.csv", encoding='utf-8')
'''
overton data has not been split into columns, so we have to do that here.
add overton to the column name to make the final merge more intelligible.
'''
overton['overton_policy_doc_id'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("policy_document_id"))
overton['overton_policy_source_id'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("policy_source_id"))
overton['overton_source_title'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("source_title"))
overton['overton_document_title'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("document_title"))
overton['overton_published_on'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("published_on"))
overton['overton_doc_url'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("document_url"))
overton['overton_type'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("type"))
overton['overton_subtype'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("subtype"))
overton['overton_country'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("country"))
overton['overton_topics'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("topics"))
overton['overton_classifications'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("classifications"))
overton['overton_url'] = overton['docs'].apply(lambda x: ast.literal_eval(x).get("url"))
overton.drop(columns=['docs'], inplace=True)
overton.rename(columns={'title': 'overton_title'}, inplace=True)

middle = pd.merge(savable, altmetric, how='left', left_on='doi', right_on='DOI')
final = pd.merge(middle, overton, how='left', on='doi')

final.to_csv("final.csv", index=False)