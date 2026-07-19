import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import SessionLocal
from app.documents.repository import DocumentRepository
from app.jobs.repository import IngestionJobRepository
from app.repository.chunk_repository import ChunkRepository
from app.storage.service import StorageService
from app.models.enums import JobStatus, MediaType, DocumentStatus
from app.models.document_chunk import DocumentChunk

from app.ingestion.parser_factory import ParserFactory
from app.ingestion.chunking.text_chunker import TextChunker
from app.embeddings.service import EmbeddingService

from app.jobs.publisher import publisher


class JobService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.job_repo = IngestionJobRepository(db)
        self.doc_repo = DocumentRepository(db)
        self.storage = StorageService()
        self.chunk_repo = ChunkRepository(db)

    async def process(self, job_id: str):
        job = await self.job_repo.get_by_id(job_id)

        await publisher.publish(
            job_id=str(job.id),
            status="RUNNING",
            progress=5,
        )

        if job is None:
            raise ValueError(f"Job {job_id} not found")

        document = await self.doc_repo.get_by_id(job.document_id)

        if document is None:
            raise ValueError("Document not found")

        response = self.storage.download_file(document.object_key)

        await publisher.publish(
            job_id=str(job.id),
            status="DOWNLOADED",
            progress=20,
        )

        try:
            file_bytes = response.read()

            parser = ParserFactory.get(document)

            text = await parser.parse(
                file_bytes=file_bytes,
                media_type=document.content_type,
            )

            await publisher.publish(
                job_id=str(job.id),
                status="PARSING_COMPLETE",
                progress=40,
            )

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

            await publisher.publish(
                job_id=str(job.id),
                status="CHUNKING_COMPLETE",
                progress=60,
            )

            embedding_service = EmbeddingService()

            vectors = await embedding_service.embed(
                [chunk.content for chunk in chunk_models]
            )

            for chunk, vector in zip(chunk_models, vectors):
                chunk.embedding = vector

            document.status = DocumentStatus.INDEXED
            job.status = JobStatus.COMPLETED
            job.progress = 100

            await publisher.publish(
                job_id=str(job.id),
                status="COMPLETED",
                progress=100,
            )

            await self.chunk_repo.create_many(chunk_models)
            await self.db.commit()

            # print(f"Total chunks: {len(chunks)}")

            # for i, chunk in enumerate(chunks[:3]):
            #     print("=" * 50)
            #     print(f"Chunk {i+1}")
            #     print(chunk)

            # print("=" * 60)
            # print(f"Filename   : {document.original_filename}")
            # print(f"Media Type : {document.media_type}")
            # print(f"Size       : {len(file_bytes)} bytes")
            # print("=" * 60)

        except Exception as e:
            job.status = JobStatus.FAILED
            job.error_message = str(e)

            document.status = DocumentStatus.FAILED
            await publisher.publish(
                job_id=str(job.id),
                status="FAILED",
                error=str(e),
            )

            await self.db.commit()

            raise
        finally:
            response.close()
            response.release_conn()