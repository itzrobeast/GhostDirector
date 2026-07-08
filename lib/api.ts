export type ProjectInput = {
  title: string;
  projectType: string;
  sourceText: string;
  style: string;
  cameraStyle: string;
  renderer: string;
  resolution: string;
  fps: number;
  aspectRatio: string;
  targetDuration: number;
  quality: string;
  seed?: number;
  negativePrompt: string;
  files: string[];
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