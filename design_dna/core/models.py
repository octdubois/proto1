from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class Entity(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    family: Optional[str] = None
    subcategory: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    characteristics: List[str] = Field(default_factory=list)
    complexity: Optional[int] = None

    # Intrinsic metadata - fallback/descriptive, but Compatibility Rules are authoritative
    preferred_moods: List[str] = Field(default_factory=list)
    preferred_styles: List[str] = Field(default_factory=list)
    preferred_palettes: List[str] = Field(default_factory=list)
    preferred_compositions: List[str] = Field(default_factory=list)

class GroundTruthModel(BaseModel):
    version: str = "2.0"
    occasions: List[Entity] = Field(default_factory=list)
    themes: List[Entity] = Field(default_factory=list)
    subjects: List[Entity] = Field(default_factory=list)
    actions: List[Entity] = Field(default_factory=list)
    environments: List[Entity] = Field(default_factory=list)
    moods: List[Entity] = Field(default_factory=list)
    art_styles: List[Entity] = Field(default_factory=list)
    visual_styles: List[Entity] = Field(default_factory=list)
    compositions: List[Entity] = Field(default_factory=list)
    palettes: List[Entity] = Field(default_factory=list)
    decorations: List[Entity] = Field(default_factory=list)
    typography: List[Entity] = Field(default_factory=list)
    textures: List[Entity] = Field(default_factory=list)
    visual_effects: List[Entity] = Field(default_factory=list)

class GenerationContext(BaseModel):
    id: str
    timestamp: str
    seed: int
    temperature: int

class DesignContext(BaseModel):
    occasion: Optional[str] = None
    theme: Optional[str] = None

class ConceptLayer(BaseModel):
    relationship: Optional[str] = None
    visual_hook: Optional[str] = None
    narrative_type: Optional[str] = None

class DesignContent(BaseModel):
    primary_subject: Optional[str] = None
    secondary_subjects: List[str] = Field(default_factory=list)
    concept: ConceptLayer = Field(default_factory=ConceptLayer)
    action: Optional[str] = None
    interaction: Optional[str] = None
    environment: Optional[str] = None
    mood: List[str] = Field(default_factory=list)
    art_style: Optional[str] = None
    visual_style: List[str] = Field(default_factory=list)
    composition: Optional[str] = None
    palette: Optional[str] = None
    decorations: List[str] = Field(default_factory=list)
    textures: List[str] = Field(default_factory=list)
    visual_effects: List[str] = Field(default_factory=list)

class Typography(BaseModel):
    enabled: bool = False
    text: Optional[str] = None
    style: Optional[str] = None

class ValidationScores(BaseModel):
    compatibility_score: float = 0.0
    novelty_score: float = 0.0
    wildcards_used: bool = False

class SourceVersions(BaseModel):
    ground_truth: str = "1.0"
    compatibility: str = "1.0"
    generator: str = "1.0"

class DesignDNA(BaseModel):
    schema_version: str = "2.0"
    generation: GenerationContext
    context: DesignContext
    design: DesignContent
    typography: Typography = Field(default_factory=Typography)
    validation: ValidationScores = Field(default_factory=ValidationScores)
    source_versions: SourceVersions = Field(default_factory=SourceVersions)
