export type ProjectInput = {
  title: string;
  project_type: string;
  source_text: string;
  style: string;
  camera_style: string;
  renderer: string;
  resolution: string;
  fps: number;
  aspect_ratio: string;
  target_duration: number;
  quality: string;
  seed?: number;
  negative_prompt: string;
  files: string[];
  render: boolean;
};

export type PipelineStage = {
  label: string;
  progress: number;
  status: "waiting" | "active" | "complete";
};

export type StudioScene = {
  scene_number: number;
  duration: number;
  emotion: string;
  camera: string;
  prompt: string;
  character_ids: string[];
  continuity_notes: string;
  render_status: string;
};

export type StudioRenderQueueItem = {
  scene_number: number;
  status: string;
  reason: string;
  progress: number;
  estimated_render_seconds: number | null;
  attempts: number;
  depends_on: number[];
};


export type StudioCharacter = {
  id: string;
  name: string;
  description: string;
  age: number | null;
  gender: string | null;
  species: string;
  appearance: string;
  hair: string;
  skin: string;
  eyes: string;
  clothing: string;
  voice: string;
  accessories: string[];
  personality: string;
  hairstyle: string;
  facial_expression: string;
  emotional_state: string;
  current_location: string;
  props: string[];
};
export type StudioProductionStatus = {
  total_scenes: number;
  prompted_scenes: number;
  rendered_scenes: number;
  edit_ready_scenes: number;
  failed_scenes: number;
  status: string;
};

export type StudioProjectResponse = {
  project: {
    title: string;
    project_type: string;
    style: string;
    scenes: StudioScene[];
    character_registry?: {
      characters: Record<string, StudioCharacter>;
    };
  };
  scene_count: number;
  production_status: StudioProductionStatus;
  render_queue: StudioRenderQueueItem[];
};

const API_BASE_URL = process.env.NEXT_PUBLIC_GHOST_DIRECTOR_API ?? "http://127.0.0.1:8001";

export async function createProject(input: ProjectInput): Promise<StudioProjectResponse> {
  const response = await fetch(`${API_BASE_URL}/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input)
  });

  if (!response.ok) {
    throw new Error("Ghost Director could not create the project.");
  }

  return response.json();
}