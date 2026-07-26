from app.rag.retrievement import retrieve_documents

docs = retrieve_documents("السخان لا يبرد")
print(f"got {len(docs)} docs")
for d in docs:
    print(d.page_content)
    print(d.metadata)
    print("---")