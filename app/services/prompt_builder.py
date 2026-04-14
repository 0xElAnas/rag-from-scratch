from app.db.models import Chunk


class PromptBuilder:
    def build_answer_prompt(self, question: str, chunks: list[Chunk]) -> str:
        if not question:
            raise ValueError("question must not be empty")

        if not chunks:
            return (
                "You are a helpful assistant.\n\n"
                "No context was provided.\n"
                "If you do not know the answer, say so.\n\n"
                f"Question:\n{question}"
            )

        context_blocks = []

        for i, chunk in enumerate(chunks, start=1):
            page = getattr(chunk, "page_number", "unknown")

            context_blocks.append(
                f"[Source {i} | page {page}]\n{chunk.text.strip()}"
            )

        context = "\n\n".join(context_blocks)

        prompt = f"""You are a helpful assistant answering questions about a document.
            Use only the provided context.
            Do not use outside knowledge.
            If the answer is not in the context, say you do not know.
            Be concise and grounded.
            When possible, cite sources using [Source X].

            Question:
            {question}

            Context:
            {context}
            """

        return prompt.strip()