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

export async function createProject(input: ProjectInput) {
  const response = await fetch("/api/projects", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input)
  });

  if (!response.ok) {
    throw new Error("Ghost Director could not create the project.");
  }

  return response.json();
}
