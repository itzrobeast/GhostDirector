"use client";

import type { ChangeEvent, DragEvent, ReactNode } from "react";
import { useState } from "react";
import { motion } from "framer-motion";
import {
  FiArchive,
  FiBox,
  FiCamera,
  FiChevronDown,
  FiChevronsDown,
  FiClock,
  FiDownload,
  FiFilm,
  FiFolder,
  FiGrid,
  FiImage,
  FiLayers,
  FiMic,
  FiMusic,
  FiPlay,
  FiPlus,
  FiRefreshCw,
  FiSettings,
  FiUpload,
  FiVideo,
  FiZap
} from "react-icons/fi";
import { createProject, type ProjectInput, type StudioCharacter, type StudioProjectResponse } from "@/lib/api";

const navItems = [
  [FiFolder, "Projects"],
  [FiClock, "Recent Projects"],
  [FiPlus, "New Project"],
  [FiCamera, "Characters"],
  [FiArchive, "Assets"],
  [FiZap, "Renderer"],
  [FiSettings, "Settings"],
  [FiLayers, "Render Queue"],
  [FiGrid, "Logs"]
] as const;

const projectTypes = [
  "Movie",
  "Music Video",
  "Commercial",
  "TV Episode",
  "YouTube Short",
  "Animation",
  "Documentary",
  "Podcast Visualizer",
  "Custom"
];

const styles = [
  "Cinematic Realism",
  "Pixar",
  "Anime",
  "DreamWorks",
  "Cyberpunk",
  "Film Noir",
  "Fantasy",
  "Sci-Fi",
  "Horror",
  "Claymation",
  "Comic Book",
  "Custom"
];

const mediaTypes = [
  [FiMusic, "Music"],
  [FiCamera, "Character Images"],
  [FiImage, "Reference Images"],
  [FiVideo, "Reference Videos"],
  [FiGrid, "Mood Board"],
  [FiMic, "Voice"],
  [FiMusic, "Background Audio"],
  [FiBox, "Logo"],
  [FiLayers, "Fonts"]
] as const;

type UploadedAsset = {
  id: string;
  category: string;
  name: string;
  size: number;
  type: string;
};

const fileInputTypes = ".txt,.pdf,.docx,.md,.markdown,.json";

function toAsset(file: File, category: string): UploadedAsset {
  return {
    id: `${category}-${file.name}-${file.size}-${file.lastModified}`,
    category,
    name: file.name,
    size: file.size,
    type: file.type || "Unknown"
  };
}

function formatFileSize(size: number): string {
  if (size < 1024) {
    return `${size} B`;
  }

  if (size < 1024 * 1024) {
    return `${Math.round(size / 1024)} KB`;
  }

  return `${(size / (1024 * 1024)).toFixed(1)} MB`;
}
const stages = [
  ["Analyze Story", 100, "complete"],
  ["Create Characters", 72, "active"],
  ["Plan Scenes", 46, "active"],
  ["Generate Prompts", 20, "waiting"],
  ["Build Timeline", 0, "waiting"],
  ["Queue Rendering", 0, "waiting"]
] as const;

const scenes = [
  { id: 1, emotion: "Hopeful", camera: "Wide tracking", duration: "00:15" },
  { id: 2, emotion: "Tense", camera: "Slow dolly", duration: "00:12" },
  { id: 3, emotion: "Wonder", camera: "Crane reveal", duration: "00:18" }
];

const sampleInput: ProjectInput = {
  title: "Untitled Production",
  project_type: "Movie",
  source_text: "",
  style: "Cinematic Realism",
  camera_style: "Hollywood",
  renderer: "Seedance",
  resolution: "1920x1080",
  fps: 24,
  aspect_ratio: "16:9",
  target_duration: 90,
  quality: "High",
  negative_prompt: "low quality, flicker, distorted faces",
  files: [],
  render: false
};

export default function StudioHome() {
  const [projectTitle, setProjectTitle] = useState(sampleInput.title);
  const [sourceText, setSourceText] = useState(sampleInput.source_text);
  const [projectType, setProjectType] = useState(sampleInput.project_type);
  const [selectedStyle, setSelectedStyle] = useState(sampleInput.style);
  const [cameraStyle, setCameraStyle] = useState(sampleInput.camera_style);
  const [rendererName, setRendererName] = useState(sampleInput.renderer);
  const [resolution, setResolution] = useState(sampleInput.resolution);
  const [fps, setFps] = useState(String(sampleInput.fps));
  const [aspectRatio, setAspectRatio] = useState(sampleInput.aspect_ratio);
  const [targetDuration, setTargetDuration] = useState(String(sampleInput.target_duration));
  const [quality, setQuality] = useState(sampleInput.quality);
  const [negativePrompt, setNegativePrompt] = useState(sampleInput.negative_prompt);
  const [seed, setSeed] = useState(sampleInput.seed ? String(sampleInput.seed) : "");
  const [advancedOpen, setAdvancedOpen] = useState(false);
  const [uploadedAssets, setUploadedAssets] = useState<UploadedAsset[]>([]);
  const [isDirecting, setIsDirecting] = useState(false);
  const [statusMessage, setStatusMessage] = useState("Ready to direct.");
  const [projectResult, setProjectResult] = useState<StudioProjectResponse | null>(null);

  async function handleDirectFilm() {
    setIsDirecting(true);
    setStatusMessage("Sending project to Ghost Director...");

    try {
      const result = await createProject({
        ...sampleInput,
        title: projectTitle,
        project_type: projectType,
        source_text: sourceText || "A cinematic story begins in a city at sunrise.",
        style: selectedStyle,
        camera_style: cameraStyle,
        renderer: rendererName,
        resolution,
        fps: Number(fps),
        aspect_ratio: aspectRatio,
        target_duration: Number(targetDuration),
        quality,
        negative_prompt: negativePrompt,
        seed: seed ? Number(seed) : undefined,
        files: uploadedAssets.map((asset) => `${asset.category}: ${asset.name}`)
      });
      setProjectResult(result);
      setStatusMessage(
        `Created ${result.scene_count} scenes. Project status: ${result.production_status.status}.`
      );
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error";
      setStatusMessage(message);
    } finally {
      setIsDirecting(false);
    }
  }
  const displayScenes = projectResult?.project.scenes.map((scene) => ({
    id: scene.scene_number,
    emotion: scene.emotion || "Unscored",
    camera: scene.camera || "Camera pending",
    duration: `${scene.duration}s`,
    prompt: scene.prompt,
    status: scene.render_status
  })) ?? scenes.map((scene) => ({ ...scene, prompt: "", status: "PREVIEW" }));

  const liveStages = projectResult ? [
    ["Analyze Story", 100, "complete"],
    ["Create Characters", 100, "complete"],
    ["Plan Scenes", 100, "complete"],
    ["Generate Prompts", 100, "complete"],
    ["Build Timeline", 100, "complete"],
    ["Queue Rendering", projectResult.render_queue.length ? 100 : 0, projectResult.render_queue.length ? "complete" : "waiting"]
  ] as const : stages;

  const displayQueue = projectResult?.render_queue ?? [];
  const displayCharacters = Object.values(projectResult?.project.character_registry?.characters ?? {});

  function addAssets(files: FileList | File[], category: string) {
    const nextAssets = Array.from(files).map((file) => toAsset(file, category));
    setUploadedAssets((currentAssets) => {
      const existingIds = new Set(currentAssets.map((asset) => asset.id));
      return [
        ...currentAssets,
        ...nextAssets.filter((asset) => !existingIds.has(asset.id))
      ];
    });
  }

  function handleFileSelect(event: ChangeEvent<HTMLInputElement>, category: string) {
    if (event.target.files) {
      addAssets(event.target.files, category);
      event.target.value = "";
    }
  }

  function handleDrop(event: DragEvent<HTMLElement>, category: string) {
    event.preventDefault();
    if (event.dataTransfer.files.length) {
      addAssets(event.dataTransfer.files, category);
    }
  }

  function assetsFor(category: string) {
    return uploadedAssets.filter((asset) => asset.category === category);
  }
  return (
    <main className="min-h-screen bg-obsidian text-white">
      <div className="flex min-h-screen">
        <aside className="hidden w-72 shrink-0 border-r border-stroke bg-panel/95 px-4 py-5 lg:block">
          <div className="mb-8 flex items-center gap-3 px-2">
            <div className="grid h-10 w-10 place-items-center rounded bg-ember text-white">
              <FiFilm size={20} />
            </div>
            <div>
              <p className="text-sm text-white/55">Ghost Director</p>
              <h1 className="text-lg font-semibold">Studio</h1>
            </div>
          </div>
          <nav className="space-y-1">
            {navItems.map(([Icon, label]) => (
              <button
                className="flex w-full items-center gap-3 rounded px-3 py-3 text-left text-sm text-white/70 transition hover:bg-white/10 hover:text-white"
                key={label}
              >
                <Icon size={18} />
                {label}
              </button>
            ))}
          </nav>
        </aside>

        <section className="studio-scrollbar flex-1 overflow-y-auto">
          <div className="mx-auto max-w-7xl px-4 py-6 md:px-8">
            <header className="mb-6 flex flex-col gap-4 border-b border-stroke pb-6 xl:flex-row xl:items-end xl:justify-between">
              <div>
                <p className="mb-2 text-sm uppercase tracking-[0.28em] text-gold">AI filmmaking control center</p>
                <h2 className="text-4xl font-semibold tracking-tight md:text-6xl">Ghost Director Studio</h2>
                <p className="mt-3 max-w-2xl text-lg text-white/65">Create complete cinematic productions from a single idea.</p>
              </div>
              <button className="inline-flex h-14 items-center justify-center gap-3 rounded bg-ember px-6 font-semibold text-white shadow-studio transition hover:bg-orange-500 disabled:cursor-not-allowed disabled:opacity-60" disabled={isDirecting} onClick={handleDirectFilm}>
                <FiPlay size={20} />
                {isDirecting ? "Directing..." : "Direct My Film"}
              </button>
            </header>

            <div className="grid gap-5 xl:grid-cols-[1.3fr_0.9fr]">
              <motion.section
                animate={{ opacity: 1, y: 0 }}
                className="rounded border border-stroke bg-panel p-5 shadow-studio"
                initial={{ opacity: 0, y: 16 }}
                transition={{ duration: 0.35 }}
              >
                <div className="mb-5 flex items-center justify-between gap-4">
                  <div>
                    <h3 className="text-xl font-semibold">New Project</h3>
                    <p className="text-sm text-white/50">Structured project input for the Ghost Director engine.</p>
                  </div>
                  <span className="rounded bg-cyan/15 px-3 py-1 text-xs text-cyan">{statusMessage}</span>
                </div>

                <div className="grid gap-4 md:grid-cols-2">
                  <label className="space-y-2">
                    <span className="text-sm text-white/60">Project Name</span>
                    <input className="h-12 w-full rounded border border-stroke bg-panelSoft px-4 outline-none transition focus:border-ember" onChange={(event) => setProjectTitle(event.target.value)} value={projectTitle} />
                  </label>
                  <label className="space-y-2">
                    <span className="text-sm text-white/60">Project Type</span>
                    <div className="relative">
                      <select className="h-12 w-full appearance-none rounded border border-stroke bg-panelSoft px-4 outline-none transition focus:border-ember" onChange={(event) => setProjectType(event.target.value)} value={projectType}>
                        {projectTypes.map((type) => <option key={type}>{type}</option>)}
                      </select>
                      <FiChevronDown className="pointer-events-none absolute right-4 top-4 text-white/50" />
                    </div>
                  </label>
                </div>

                <label className="mt-4 block space-y-2">
                  <span className="text-sm text-white/60">Main Input</span>
                  <textarea
                    className="min-h-72 w-full resize-y rounded border border-stroke bg-panelSoft p-4 leading-7 outline-none transition focus:border-ember"
                    onChange={(event) => setSourceText(event.target.value)}
                    placeholder="Paste a prompt, story, lyrics, screenplay, chapter, markdown, or production notes..."
                    value={sourceText}
                  />
                </label>

                <label
                  className="mt-4 block cursor-pointer rounded border border-dashed border-stroke bg-black/20 p-5 text-center text-sm text-white/55 transition hover:border-ember hover:text-white"
                  onDragOver={(event) => event.preventDefault()}
                  onDrop={(event) => handleDrop(event, "Source Files")}
                >
                  <FiUpload className="mx-auto mb-2" size={22} />
                  Drop TXT, PDF, DOCX, Markdown, or JSON files here
                  <input
                    accept={fileInputTypes}
                    className="sr-only"
                    multiple
                    onChange={(event) => handleFileSelect(event, "Source Files")}
                    type="file"
                  />
                </label>

                {assetsFor("Source Files").length > 0 && (
                  <div className="mt-3 grid gap-2 sm:grid-cols-2">
                    {assetsFor("Source Files").map((asset) => (
                      <FileCard asset={asset} key={asset.id} />
                    ))}
                  </div>
                )}
              </motion.section>

              <section className="grid gap-5">
                <Panel title="Render Settings" icon={<FiZap />}>
                  <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-1 2xl:grid-cols-2">
                    <Setting label="Renderer" onChange={setRendererName} options={["Seedance", "ComfyUI", "OpenArt", "Veo", "Higgsfield", "LTX", "Flux"]} value={rendererName} />
                    <Setting label="Resolution" onChange={setResolution} options={["1920x1080", "1280x720", "1080x1920", "1024x1024"]} value={resolution} />
                    <Setting label="FPS" onChange={setFps} options={["24", "30", "48", "60"]} value={fps} />
                    <Setting label="Aspect Ratio" onChange={setAspectRatio} options={["16:9", "9:16", "1:1", "2.39:1"]} value={aspectRatio} />
                    <Setting label="Target Duration" onChange={setTargetDuration} options={["30", "60", "90", "180"]} value={targetDuration} />
                    <Setting label="Quality" onChange={setQuality} options={["Draft", "Standard", "High", "Ultra"]} value={quality} />
                  </div>
                  <button
                    className="mt-4 flex w-full items-center justify-between rounded border border-stroke bg-panelSoft px-3 py-3 text-left text-sm text-white/70 transition hover:border-ember hover:text-white"
                    onClick={() => setAdvancedOpen((isOpen) => !isOpen)}
                    type="button"
                  >
                    Advanced options
                    <FiChevronsDown className={`transition ${advancedOpen ? "rotate-180" : ""}`} />
                  </button>
                  {advancedOpen && (
                    <div className="mt-3 grid gap-3">
                      <label className="space-y-2">
                        <span className="text-xs text-white/45">Seed</span>
                        <input
                          className="h-11 w-full rounded border border-stroke bg-panelSoft px-3 text-sm outline-none transition focus:border-ember"
                          inputMode="numeric"
                          onChange={(event) => setSeed(event.target.value.replace(/\D/g, ""))}
                          placeholder="Auto"
                          value={seed}
                        />
                      </label>
                      <label className="space-y-2">
                        <span className="text-xs text-white/45">Negative Prompt</span>
                        <textarea
                          className="min-h-24 w-full resize-y rounded border border-stroke bg-panelSoft px-3 py-2 text-sm leading-6 outline-none transition focus:border-ember"
                          onChange={(event) => setNegativePrompt(event.target.value)}
                          value={negativePrompt}
                        />
                      </label>
                    </div>
                  )}
                </Panel>

                <Panel title="Camera Style" icon={<FiCamera />}>
                  <Setting label="Direction Language" onChange={setCameraStyle} options={["Hollywood", "Documentary", "Music Video", "Michael Bay", "Denis Villeneuve", "Wes Anderson", "Christopher Nolan", "Custom"]} value={cameraStyle} />
                </Panel>
              </section>
            </div>

            <div className="mt-5 grid gap-5 xl:grid-cols-[0.9fr_1.1fr]">
              <Panel title="Media" icon={<FiUpload />}>
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-2">
                  {mediaTypes.map(([Icon, label]) => {
                    const categoryAssets = assetsFor(label);

                    return (
                      <label
                        className="cursor-pointer rounded border border-stroke bg-panelSoft p-4 transition hover:border-ember hover:bg-white/10"
                        key={label}
                        onDragOver={(event) => event.preventDefault()}
                        onDrop={(event) => handleDrop(event, label)}
                      >
                        <Icon className="mb-3 text-gold" size={20} />
                        <p className="text-sm font-medium">{label}</p>
                        <p className="mt-1 text-xs text-white/45">Drop files</p>
                        <input
                          className="sr-only"
                          multiple
                          onChange={(event) => handleFileSelect(event, label)}
                          type="file"
                        />
                        {categoryAssets.length > 0 && (
                          <div className="mt-3 space-y-2">
                            {categoryAssets.map((asset) => (
                              <FileCard asset={asset} key={asset.id} compact />
                            ))}
                          </div>
                        )}
                      </label>
                    );
                  })}
                </div>
              </Panel>

              <Panel title="Visual Style" icon={<FiImage />}>
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                  {styles.map((style) => (
                    <button className={`rounded border p-4 text-left text-sm transition hover:border-ember hover:bg-white/10 ${selectedStyle === style ? "border-ember bg-ember/10" : "border-stroke bg-panelSoft"}`} key={style} onClick={() => setSelectedStyle(style)}>
                      {style}
                    </button>
                  ))}
                </div>
              </Panel>
            </div>

            <Panel className="mt-5" title="Characters" icon={<FiCamera />}>
              {displayCharacters.length ? (
                <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                  {displayCharacters.map((character) => (
                    <CharacterCard character={character} key={character.id} />
                  ))}
                </div>
              ) : (
                <div className="rounded border border-dashed border-stroke bg-panelSoft p-5 text-sm text-white/50">
                  Character memory will appear here after Ghost Director creates or recognizes project characters.
                </div>
              )}
            </Panel>
            <div className="mt-5 grid gap-5 xl:grid-cols-3">
              <Panel title="Live Progress" icon={<FiRefreshCw />}>
                <div className="space-y-4">
                  {liveStages.map(([label, progress, status]) => (
                    <div key={label}>
                      <div className="mb-2 flex items-center justify-between text-sm">
                        <span>{label}</span>
                        <span className="text-white/45">{status}</span>
                      </div>
                      <div className="h-2 rounded bg-white/10">
                        <div className="h-2 rounded bg-ember" style={{ width: `${progress}%` }} />
                      </div>
                    </div>
                  ))}
                </div>
              </Panel>

              <Panel title="Render Queue" icon={<FiLayers />}>
                <div className="space-y-3">
                  {displayQueue.length ? displayQueue.map((item) => (
                    <div className="flex items-center justify-between rounded bg-panelSoft px-4 py-3 text-sm" key={item.scene_number}>
                      <span>Scene {item.scene_number.toString().padStart(3, "0")} / {item.status}</span>
                      <button className="text-gold">Retry</button>
                    </div>
                  )) : (
                    <div className="rounded bg-panelSoft px-4 py-3 text-sm text-white/50">No scenes queued yet.</div>
                  )}
                </div>
              </Panel>

              <Panel title="Export" icon={<FiDownload />}>
                <div className="grid gap-3">
                  {["Project JSON", "Scene JSON", "Prompts", "Timeline", "Edit Decision List", "Final Movie", "Assets", "ZIP Archive"].map((item) => (
                    <button className="flex items-center justify-between rounded bg-panelSoft px-4 py-3 text-sm transition hover:bg-white/10" key={item}>
                      {item}
                      <FiDownload />
                    </button>
                  ))}
                </div>
              </Panel>
            </div>

            <Panel className="mt-5" title="Scenes" icon={<FiFilm />}>
              <div className="grid gap-4 lg:grid-cols-3">
                {displayScenes.map((scene) => (
                  <article className="rounded border border-stroke bg-panelSoft p-4" key={scene.id}>
                    <div className="mb-4 aspect-video rounded bg-gradient-to-br from-slate-800 via-zinc-900 to-orange-950" />
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <h4 className="font-semibold">Scene {scene.id.toString().padStart(3, "0")}</h4>
                        <p className="mt-1 text-sm text-white/50">{scene.emotion} / {scene.camera}</p>
                        <p className="mt-2 line-clamp-3 text-xs text-white/40">{scene.prompt || scene.status}</p>
                      </div>
                      <span className="rounded bg-white/10 px-2 py-1 text-xs">{scene.duration}</span>
                    </div>
                    <div className="mt-4 grid grid-cols-4 gap-2 text-xs">
                      {['Preview', 'Edit', 'Re-render', 'Delete'].map((action) => (
                        <button className="rounded bg-black/25 px-2 py-2 text-white/65 transition hover:text-white" key={action}>{action}</button>
                      ))}
                    </div>
                  </article>
                ))}
              </div>
            </Panel>

            <Panel className="mt-5" title="Timeline" icon={<FiLayers />}>
              <div className="grid min-h-32 grid-cols-3 gap-3 rounded bg-black/25 p-4">
                {displayScenes.map((scene) => (
                  <div className="rounded border border-stroke bg-panelSoft p-3" key={scene.id}>
                    <p className="text-sm font-medium">Scene {scene.id}</p>
                    <p className="mt-2 text-xs text-white/45">Drag, trim, transition</p>
                  </div>
                ))}
              </div>
            </Panel>
          </div>
        </section>
      </div>
    </main>
  );
}

function CharacterCard({ character }: { character: StudioCharacter }) {
  const displayName = character.name || "Unnamed Character";
  const details = [
    character.species,
    character.age ? `${character.age} years old` : "",
    character.current_location
  ].filter(Boolean).join(" / ");

  return (
    <article className="rounded border border-stroke bg-panelSoft p-4">
      <div className="mb-4 flex items-start gap-3">
        <div className="grid h-14 w-14 shrink-0 place-items-center rounded bg-ember/20 text-lg font-semibold text-gold">
          {displayName.slice(0, 1).toUpperCase()}
        </div>
        <div className="min-w-0">
          <h4 className="truncate font-semibold">{displayName}</h4>
          <p className="mt-1 text-xs text-white/45">{details || "Persistent character"}</p>
        </div>
      </div>
      <div className="space-y-2 text-xs text-white/55">
        <p><span className="text-white/35">Clothing:</span> {character.clothing || "Not set"}</p>
        <p><span className="text-white/35">Expression:</span> {character.facial_expression || character.emotional_state || "Not set"}</p>
        <p><span className="text-white/35">Accessories:</span> {character.accessories.length ? character.accessories.join(", ") : "None"}</p>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-2 text-xs">
        <button className="rounded bg-black/25 px-3 py-2 text-white/65 transition hover:text-white">Edit</button>
        <button className="rounded bg-black/25 px-3 py-2 text-white/65 transition hover:text-white">Consistency</button>
      </div>
    </article>
  );
}
function FileCard({ asset, compact = false }: { asset: UploadedAsset; compact?: boolean }) {
  return (
    <div className="rounded border border-stroke bg-black/25 px-3 py-2 text-left">
      <p className="truncate text-xs font-medium text-white/80">{asset.name}</p>
      {!compact && <p className="mt-1 text-xs text-white/40">{asset.category} / {formatFileSize(asset.size)}</p>}
      {compact && <p className="mt-1 text-[11px] text-white/40">{formatFileSize(asset.size)}</p>}
    </div>
  );
}

function Panel({ children, className = "", icon, title }: { children: ReactNode; className?: string; icon: ReactNode; title: string }) {
  return (
    <section className={`rounded border border-stroke bg-panel p-5 shadow-studio ${className}`}>
      <div className="mb-4 flex items-center gap-3">
        <div className="grid h-9 w-9 place-items-center rounded bg-white/10 text-gold">{icon}</div>
        <h3 className="text-lg font-semibold">{title}</h3>
      </div>
      {children}
    </section>
  );
}

function Setting({ label, onChange, options, value }: { label: string; onChange: (value: string) => void; options: string[]; value: string }) {
  return (
    <label className="space-y-2">
      <span className="text-xs text-white/45">{label}</span>
      <div className="relative">
        <select
          className="h-11 w-full appearance-none rounded border border-stroke bg-panelSoft px-3 text-sm outline-none transition focus:border-ember"
          onChange={(event) => onChange(event.target.value)}
          value={value}
        >
          {options.map((option) => (
            <option key={option}>{option}</option>
          ))}
        </select>
        <FiChevronDown className="pointer-events-none absolute right-3 top-3.5 text-white/45" />
      </div>
    </label>
  );
}