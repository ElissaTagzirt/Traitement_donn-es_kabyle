from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("Ageldun-amectuh_St-Exupery_Tasaghelt.pdf")
#print(result.text_content)

# Enregistrer le contenu dans un fichier Markdown
with open("output.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)