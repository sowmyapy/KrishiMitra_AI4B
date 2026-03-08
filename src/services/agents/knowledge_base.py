"""
Knowledge base with RAG (Retrieval Augmented Generation)
"""
import logging

import chromadb
from chromadb.config import Settings

from src.config.settings import settings
from src.services.llm_factory import get_llm

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Vector database knowledge base with semantic search"""

    def __init__(self):
        """Initialize ChromaDB and LLM client"""
        self.chroma_client = chromadb.HttpClient(
            host=settings.chromadb_host,
            port=settings.chromadb_port,
            settings=Settings(anonymized_telemetry=False)
        )

        self.llm = get_llm()  # Use LLM factory for embeddings

        # Create or get collections
        self.agricultural_knowledge = self.chroma_client.get_or_create_collection(
            name="agricultural_knowledge",
            metadata={"description": "General agricultural knowledge and best practices"}
        )

        self.pest_disease_knowledge = self.chroma_client.get_or_create_collection(
            name="pest_disease_knowledge",
            metadata={"description": "Pest and disease identification and treatment"}
        )

        self.crop_management = self.chroma_client.get_or_create_collection(
            name="crop_management",
            metadata={"description": "Crop-specific management practices"}
        )

        logger.info("Knowledge base initialized")

    async def _generate_embedding(self, text: str) -> list[float]:
        """Generate embedding for text using LLM provider"""
        return await self.llm.generate_embedding(text)

    async def add_document(
        self,
        collection_name: str,
        document: str,
        metadata: dict,
        doc_id: str | None = None
    ):
        """
        Add document to knowledge base

        Args:
            collection_name: Name of collection
            document: Document text
            metadata: Document metadata
            doc_id: Optional document ID
        """
        collection = getattr(self, collection_name)

        # Generate embedding
        embedding = await self._generate_embedding(document)

        # Add to collection
        collection.add(
            documents=[document],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[doc_id] if doc_id else None
        )

        logger.info(f"Added document to {collection_name}")

    async def search(
        self,
        query: str,
        collection_name: str = "agricultural_knowledge",
        n_results: int = 5
    ) -> list[dict]:
        """
        Search knowledge base

        Args:
            query: Search query
            collection_name: Collection to search
            n_results: Number of results to return

        Returns:
            List of relevant documents with metadata
        """
        collection = getattr(self, collection_name)

        # Generate query embedding
        query_embedding = await self._generate_embedding(query)

        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        # Format results
        documents = []
        for i in range(len(results['documents'][0])):
            documents.append({
                "content": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "distance": results['distances'][0][i]
            })

        logger.info(f"Found {len(documents)} results for query: {query[:50]}...")
        return documents

    async def search_pest_disease(
        self,
        symptoms: str,
        crop_type: str,
        n_results: int = 3
    ) -> list[dict]:
        """
        Search for pest/disease information

        Args:
            symptoms: Description of symptoms
            crop_type: Type of crop
            n_results: Number of results

        Returns:
            List of matching pest/disease information
        """
        query = f"Crop: {crop_type}. Symptoms: {symptoms}"
        return await self.search(query, "pest_disease_knowledge", n_results)

    async def search_crop_management(
        self,
        crop_type: str,
        issue: str,
        n_results: int = 3
    ) -> list[dict]:
        """
        Search for crop management practices

        Args:
            crop_type: Type of crop
            issue: Management issue or question
            n_results: Number of results

        Returns:
            List of management recommendations
        """
        query = f"Crop: {crop_type}. Issue: {issue}"
        return await self.search(query, "crop_management", n_results)

    async def get_context_for_query(
        self,
        query: str,
        collections: list[str] | None = None,
        n_results: int = 3
    ) -> str:
        """
        Get relevant context for a query from multiple collections

        Args:
            query: User query
            collections: List of collections to search (default: all)
            n_results: Results per collection

        Returns:
            Formatted context string
        """
        if collections is None:
            collections = [
                "agricultural_knowledge",
                "pest_disease_knowledge",
                "crop_management"
            ]

        context_parts = []

        for collection_name in collections:
            results = await self.search(query, collection_name, n_results)

            if results:
                context_parts.append(f"\n## From {collection_name}:")
                for i, doc in enumerate(results, 1):
                    context_parts.append(f"\n{i}. {doc['content']}")

        return "\n".join(context_parts)

    async def seed_initial_knowledge(self):
        """Seed knowledge base with initial agricultural knowledge"""

        # Agricultural best practices
        agricultural_docs = [
            {
                "content": "Regular soil testing helps determine nutrient levels and pH. Test soil every 2-3 years for optimal crop management.",
                "metadata": {"category": "soil_management", "importance": "high"}
            },
            {
                "content": "Crop rotation prevents soil depletion and reduces pest buildup. Rotate between different crop families each season.",
                "metadata": {"category": "crop_rotation", "importance": "high"}
            },
            {
                "content": "Drip irrigation is 90% efficient compared to 60% for sprinkler systems. It reduces water waste and disease spread.",
                "metadata": {"category": "irrigation", "importance": "medium"}
            },
        ]

        for i, doc in enumerate(agricultural_docs):
            await self.add_document(
                "agricultural_knowledge",
                doc["content"],
                doc["metadata"],
                f"ag_doc_{i}"
            )

        # Pest and disease knowledge
        pest_disease_docs = [
            {
                "content": "Aphids: Small soft-bodied insects on leaves and stems. Cause yellowing and curling. Treatment: Neem oil spray or insecticidal soap.",
                "metadata": {"pest": "aphids", "severity": "medium", "crops": "multiple"}
            },
            {
                "content": "Powdery mildew: White powdery coating on leaves. Caused by fungus in humid conditions. Treatment: Sulfur-based fungicide, improve air circulation.",
                "metadata": {"disease": "powdery_mildew", "severity": "medium", "crops": "multiple"}
            },
            {
                "content": "Leaf blight: Brown spots with yellow halos on leaves. Bacterial or fungal. Treatment: Remove infected leaves, copper-based fungicide.",
                "metadata": {"disease": "leaf_blight", "severity": "high", "crops": "rice,wheat"}
            },
        ]

        for i, doc in enumerate(pest_disease_docs):
            await self.add_document(
                "pest_disease_knowledge",
                doc["content"],
                doc["metadata"],
                f"pest_doc_{i}"
            )

        # Crop management
        crop_management_docs = [
            {
                "content": "Rice water management: Maintain 2-5cm water depth during vegetative stage. Drain 7-10 days before harvest.",
                "metadata": {"crop": "rice", "stage": "all", "practice": "irrigation"}
            },
            {
                "content": "Wheat nitrogen application: Apply 50% at sowing, 25% at tillering, 25% at flowering for optimal yield.",
                "metadata": {"crop": "wheat", "stage": "fertilization", "practice": "nutrient_management"}
            },
            {
                "content": "Cotton heat stress: Provide adequate irrigation during flowering. Mulching helps maintain soil moisture and temperature.",
                "metadata": {"crop": "cotton", "stress": "heat", "practice": "stress_management"}
            },
        ]

        for i, doc in enumerate(crop_management_docs):
            await self.add_document(
                "crop_management",
                doc["content"],
                doc["metadata"],
                f"crop_doc_{i}"
            )

        logger.info("Knowledge base seeded with initial documents")
