# from mtmai.core.logging import get_logger
from phi.knowledge.combined import CombinedKnowledgeBase
from phi.knowledge.pdf import PDFUrlKnowledgeBase

# from phi.storage.agent.postgres import PgAgentStorage
from phi.vectordb.pgvector import PgVector, SearchType

from mtmai.core.config import settings


def get_url_pdf_knowledge_base():
    url_pdf_knowledge_base = PDFUrlKnowledgeBase(
        urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
        vector_db=PgVector(
            table_name="recipes_demo",
            db_url=settings.MTMAI_DATABASE_URL,
            search_type=SearchType.hybrid,
        ),
    )
    # Load the knowledge base: Comment out after first run
    # knowledge_base.load(recreate=True, upsert=True)

    knowledge_base = CombinedKnowledgeBase(
        sources=[
            url_pdf_knowledge_base,
            # website_knowledge_base,
            # local_pdf_knowledge_base,
        ],
        vector_db=PgVector(
            # Table name: ai.combined_documents
            table_name="combined_documents",
            db_url=settings.MTMAI_DATABASE_URL,
        ),
    )


# model = OpenAIChat(
#     id="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
#     base_url="https://api.together.xyz/v1",
#     api_key="10747773f9883cf150558aca1b0dda81af4237916b03d207b8ce645edb40a546",
# )


def get_phidata_llm():
    from phi.model.groq import Groq

    # return OpenAIChat(
    #     id="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    #     base_url="https://api.together.xyz/v1",
    #     api_key="10747773f9883cf150558aca1b0dda81af4237916b03d207b8ce645edb40a546",
    # )
    # return OpenAIChat(
    #     id="llama-3.2-11b-vision-preview",
    #     base_url="https://api.groq.com/openai/v1",
    #     api_key="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",
    # )
    # return Groq(id="llama3-groq-70b-8192-tool-use-preview", api_key="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")
    return Groq(
        id="llama3-groq-70b-8192-tool-use-preview",
        api_key="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",
    )
