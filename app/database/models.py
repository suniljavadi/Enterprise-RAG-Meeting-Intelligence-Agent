from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(100), default="public")
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    filename: Mapped[str] = mapped_column(String(255))
    document_type: Mapped[str] = mapped_column(String(20))
    source: Mapped[str] = mapped_column(String(255), default="upload")
    author: Mapped[str] = mapped_column(String(255), nullable=True)
    project: Mapped[str] = mapped_column(String(255), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(30), default="uploaded")
    content: Mapped[str] = mapped_column(Text, default="")
    tenant_id: Mapped[str] = mapped_column(String(100), default="public", index=True)
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[int] = mapped_column(primary_key=True)
    chunk_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    document_id: Mapped[str] = mapped_column(ForeignKey("documents.document_id"), index=True)
    text: Mapped[str] = mapped_column(Text)
    page: Mapped[int] = mapped_column(Integer, nullable=True)
    section: Mapped[str] = mapped_column(String(255), default="General")
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    embedding: Mapped[list[float]] = mapped_column(JSON, default=list)
    document: Mapped[Document] = relationship(back_populates="chunks")

class Meeting(Base):
    __tablename__ = "meetings"
    id: Mapped[int] = mapped_column(primary_key=True)
    meeting_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    meeting_date: Mapped[datetime] = mapped_column(DateTime)
    summary: Mapped[str] = mapped_column(Text)
    decisions: Mapped[list] = mapped_column(JSON, default=list)
    risks: Mapped[list] = mapped_column(JSON, default=list)
    dependencies: Mapped[list] = mapped_column(JSON, default=list)
    questions: Mapped[list] = mapped_column(JSON, default=list)
    source_document_id: Mapped[str] = mapped_column(String(64), nullable=True)

class ActionItem(Base):
    __tablename__ = "action_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    meeting_id: Mapped[str] = mapped_column(ForeignKey("meetings.meeting_id"))
    action: Mapped[str] = mapped_column(Text)
    owner: Mapped[str] = mapped_column(String(255))
    deadline: Mapped[str] = mapped_column(String(30), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="OPEN")

class EvaluationResult(Base):
    __tablename__ = "evaluation_results"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[str] = mapped_column(String(64))
    metric: Mapped[str] = mapped_column(String(64))
    value: Mapped[float] = mapped_column(Float)
