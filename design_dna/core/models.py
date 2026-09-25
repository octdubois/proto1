from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class Entity(BaseModel):
    id: str
    display_name: str
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    complexity: Optional[int] = None
    aliases: List[str] = Field(default_factory=list)

class GroundTruthModel(BaseModel):
    version: str = "1.0"
    occasions: List[Entity] = Field(default_factory=list)
    themes: List[Entity] = Field(default_factory=list)
    subjects: List[Entity] = Field(default_factory=list)
    actions: List[Entity] = Field(default_factory=list)
    moods: List[Entity] = Field(default_factory=list)
    art_styles: List[Entity] = Field(default_factory=list)
    compositions: List[Entity] = Field(default_factory=list)
    palettes: List[Entity] = Field(default_factory=list)
    decorations: List[Entity] = Field(default_factory=list)

class GenerationContext(BaseModel):
    id: str
    timestamp: str
    seed: int
    temperature: int

class DesignContext(BaseModel):
    occasion: Optional[str] = None
    theme: Optional[str] = None

class DesignContent(BaseModel):
    subject: Optional[str] = None
    concept: Optional[str] = None
    action: Optional[str] = None
    mood: List[str] = Field(default_factory=list)
    art_style: Optional[str] = None
    composition: Optional[str] = None
    palette: Optional[str] = None
    decorations: List[str] = Field(default_factory=list)

class Typography(BaseModel):
    enabled: bool = False
    text: Optional[str] = None
    style: Optional[str] = None

class ValidationScores(BaseModel):
    compatibility_score: float = 0.0
    novelty_score: float = 0.0

class SourceVersions(BaseModel):
    ground_truth: str = "1.0"
    compatibility: str = "1.0"
    generator: str = "1.0"

class DesignDNA(BaseModel):
    schema_version: str = "1.0"
    generation: GenerationContext
    context: DesignContext
    design: DesignContent
    typography: Typography = Field(default_factory=Typography)
    validation: ValidationScores = Field(default_factory=ValidationScores)
    source_versions: SourceVersions = Field(default_factory=SourceVersions)
