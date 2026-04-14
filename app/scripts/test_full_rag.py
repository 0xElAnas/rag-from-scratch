from app.db.session import SessionLocal
from app.services.embedder import Embedder
from app.services.vector_store import VectorStore
from app.services.retrieval_service import RetrievalService
from app.services.prompt_builder import PromptBuilder
from app.services.generation_service import GenerationService


def main():
    db = SessionLocal()

    try:
        embedder = Embedder()
        vector_store = VectorStore()
        retrieval_service = RetrievalService(embedder, vector_store)
        prompt_builder = PromptBuilder()
        generation_service = GenerationService()

        question = "How many vacation days do employees get?"
        document_id = "102a1da6-c000-4e95-8cca-37d44ce061b1"

        chunks = retrieval_service.retrieve(
            db=db,
            question=question,
            document_id=document_id,
            top_k=5,
        )

        print(f"\nQuestion: {question}\n")
        print("Retrieved chunks:\n")

        for i, chunk in enumerate(chunks, start=1):
            print(f"[{i}] Page: {chunk.page_number}")
            print(chunk.text[:300])
            print("-" * 80)

        prompt = prompt_builder.build_answer_prompt(
            question=question,
            chunks=chunks,
        )

        answer = generation_service.generate_answer(prompt)

        print("\nFinal answer:\n")
        print(answer)

    finally:
        db.close()


if __name__ == "__main__":
    main()