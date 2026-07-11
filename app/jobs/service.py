import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import SessionLocal
from app.documents.repository import DocumentRepository
from app.jobs.repository import IngestionJobRepository
from app.repository.chunk_repository import ChunkRepository
from app.storage.service import StorageService
from app.models.enums import JobStatus, MediaType
from app.models.document_chunk import DocumentChunk

from app.ingestion.parsers.pdf_parser import PDFParser
from app.ingestion.chunking.text_chunker import TextChunker
from app.embeddings.service import EmbeddingService


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.job_repo = IngestionJobRepository(db)
        self.doc_repo = DocumentRepository(db)
        self.storage = StorageService()
        self.chunk_repo = ChunkRepository(db)

    async def process(self, job_id: str):
        job = await self.job_repo.get_by_id(job_id)

        if job is None:
            raise ValueError(f"Job {job_id} not found")

        document = await self.doc_repo.get_by_id(job.document_id)

        if document is None:
            raise ValueError("Document not found")

        response = self.storage.download_file(document.object_key)

        try:
            file_bytes = response.read()

            if document.media_type == MediaType.PDF:
                parser = PDFParser()

                text = parser.extract_text(file_bytes)

                # print("=" * 60)
                # print(text[:1000])
                # print("=" * 60)
                chunker = TextChunker()

                chunks = chunker.split(text)
                chunk_models = []

                


                for index, chunk in enumerate(chunks):
                    chunk_models.append(
                        DocumentChunk(
                            document_id=document.id,
                            chunk_index=index,
                            content=chunk,
                        )
                    )

                embedding_service = EmbeddingService()

                vectors = await embedding_service.embed(
                    [chunk.content for chunk in chunk_models]
                )

                print(len(vectors))
                print(len(vectors[0]))

                await self.chunk_repo.create_many(chunk_models)
                await self.db.commit()

                # print(f"Total chunks: {len(chunks)}")

                # for i, chunk in enumerate(chunks[:3]):
                #     print("=" * 50)
                #     print(f"Chunk {i+1}")
                #     print(chunk)

            print("=" * 60)
            print(f"Filename   : {document.original_filename}")
            print(f"Media Type : {document.media_type}")
            print(f"Size       : {len(file_bytes)} bytes")
            print("=" * 60)

        finally:
            response.close()
            response.release_conn()