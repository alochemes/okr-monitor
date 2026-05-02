"use client";

// Live 3D system schematic — the centerpiece of /v2.
//
// Architecture: 4 source plinths (GitHub/Linear/Slack/Notion) arranged in a
// tetrahedron-ish layout around a central glowing octahedron (the dashboard).
// Curved Bezier streams flow from each source to the center; a tracer
// particle moves along each stream. A wireframe boundary sphere frames the
// whole thing as a "system."
//
// Performance:
//   - Low-poly geometry (octahedron, box, low-segment sphere)
//   - dpr capped at 1.5 to avoid retina cost
//   - No HDRI environment, no shadows, no postprocessing
//   - Camera auto-rotates; mouse interaction disabled (page scroll is the
//     primary interaction, we don't fight for it)
//
// Accessibility:
//   - Canvas wrapped with aria-hidden="true" — all meaning conveyed via the
//     surrounding text. The 3D scene is decorative reinforcement, not the
//     content.
//   - Caller is responsible for swapping to <DataFlowFallbackSVG /> when
//     prefers-reduced-motion is true or window width < 768px.

import { useMemo, useRef } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Html, Line, OrbitControls } from "@react-three/drei";
import * as THREE from "three";

const PERSIMMON = "#C73A14";
const PERSIMMON_DEEP = "#5A1A07";
const CYAN = "#00D9FF";
const CYAN_DIM = "#0099B8";

// Source plinth positions — pulled out of a flat plane into a slight
// tetrahedron to give 3D depth that reads in motion.
const SOURCES = [
  { label: "GITHUB", position: [2.6, 1.0, 1.0] as Vec3 },
  { label: "LINEAR", position: [-2.6, 1.0, -1.0] as Vec3 },
  { label: "SLACK",  position: [2.6, -1.0, -1.0] as Vec3 },
  { label: "NOTION", position: [-2.6, -1.0, 1.0] as Vec3 },
];

type Vec3 = [number, number, number];

// --- Components -----------------------------------------------------------

function CentralNode() {
  const meshRef = useRef<THREE.Mesh>(null);
  const haloRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    const t = state.clock.elapsedTime;
    if (meshRef.current) {
      // Gentle pulse + slow self-rotation
      const s = 0.55 + Math.sin(t * 1.4) * 0.04;
      meshRef.current.scale.setScalar(s);
      meshRef.current.rotation.y = t * 0.18;
      meshRef.current.rotation.x = t * 0.06;
    }
    if (haloRef.current) {
      const halo = 1 + Math.sin(t * 1.4) * 0.08;
      haloRef.current.scale.setScalar(halo);
      const mat = haloRef.current.material as THREE.MeshBasicMaterial;
      mat.opacity = 0.18 + Math.sin(t * 1.4) * 0.07;
    }
  });

  return (
    <group>
      {/* Soft halo — translucent slightly larger sphere */}
      <mesh ref={haloRef}>
        <sphereGeometry args={[0.95, 24, 16]} />
        <meshBasicMaterial color={PERSIMMON} transparent opacity={0.18} depthWrite={false} />
      </mesh>
      {/* The core — octahedron */}
      <mesh ref={meshRef}>
        <octahedronGeometry args={[1, 0]} />
        <meshStandardMaterial
          color={PERSIMMON_DEEP}
          emissive={PERSIMMON}
          emissiveIntensity={1.1}
          metalness={0.4}
          roughness={0.35}
        />
      </mesh>
    </group>
  );
}

function SourcePlinth({ label, position }: { label: string; position: Vec3 }) {
  const ref = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (!ref.current) return;
    // Subtle Y-bob so the source feels alive (not stiff)
    const t = state.clock.elapsedTime;
    const seed = position[0] + position[2];
    ref.current.position.y = position[1] + Math.sin(t * 0.6 + seed) * 0.04;
  });

  return (
    <group ref={ref} position={position}>
      {/* Plinth — a flat box, lit from the central node */}
      <mesh>
        <boxGeometry args={[0.85, 0.18, 0.85]} />
        <meshStandardMaterial
          color="#101522"
          emissive={CYAN_DIM}
          emissiveIntensity={0.05}
          metalness={0.7}
          roughness={0.35}
        />
      </mesh>
      {/* Edge lighting — thin top inset that reads as a screen */}
      <mesh position={[0, 0.092, 0]}>
        <boxGeometry args={[0.65, 0.005, 0.65]} />
        <meshBasicMaterial color={CYAN} transparent opacity={0.85} />
      </mesh>
      {/* Floating mono label */}
      <Html
        position={[0, -0.32, 0]}
        center
        distanceFactor={9}
        style={{ pointerEvents: "none", userSelect: "none" }}
      >
        <div className="font-mono text-[10px] tracking-[0.22em] text-v2-cyan whitespace-nowrap">
          <span className="inline-block h-1 w-1 translate-y-[-2px] mr-1.5 rounded-full bg-v2-cyan animate-pulse-v2" />
          {label}
        </div>
      </Html>
    </group>
  );
}

// A single Bezier-curve stream from a source plinth to the center.
// Static line for the path + animated tracer sphere for the "data moving" effect.
function DataStream({
  from,
  offset,
  pathRef,
}: {
  from: Vec3;
  offset: number;
  pathRef?: React.MutableRefObject<THREE.QuadraticBezierCurve3 | null>;
}) {
  const curve = useMemo(() => {
    const start = new THREE.Vector3(...from);
    const end = new THREE.Vector3(0, 0, 0);
    const mid = new THREE.Vector3()
      .addVectors(start, end)
      .multiplyScalar(0.5)
      .add(new THREE.Vector3(0, 0.55, 0)); // bow upward
    const c = new THREE.QuadraticBezierCurve3(start, mid, end);
    if (pathRef) pathRef.current = c;
    return c;
  }, [from, pathRef]);

  const points = useMemo(() => curve.getPoints(48), [curve]);

  const tracerRef = useRef<THREE.Mesh>(null);
  useFrame((state) => {
    if (!tracerRef.current) return;
    const period = 2.6;
    const t = ((state.clock.elapsedTime + offset) % period) / period;
    const p = curve.getPoint(t);
    tracerRef.current.position.copy(p);
    // Fade out near the destination so it doesn't visually clip the central node
    const mat = tracerRef.current.material as THREE.MeshBasicMaterial;
    mat.opacity = 1 - Math.max(0, (t - 0.85) / 0.15);
  });

  return (
    <>
      <Line points={points} color={CYAN} lineWidth={1} transparent opacity={0.35} />
      <mesh ref={tracerRef}>
        <sphereGeometry args={[0.07, 12, 8]} />
        <meshBasicMaterial color={CYAN} transparent />
      </mesh>
    </>
  );
}

function BoundarySphere() {
  // Wireframe sphere — frames the system as a "container"
  return (
    <mesh>
      <sphereGeometry args={[4.2, 18, 12]} />
      <meshBasicMaterial color="#1A1F2E" wireframe transparent opacity={0.32} />
    </mesh>
  );
}

function CameraOrbit() {
  // Auto-orbit the camera around the scene. We use OrbitControls because
  // it handles damping & pole avoidance for us; user interaction is disabled
  // because the canvas competes with page scroll.
  return (
    <OrbitControls
      autoRotate
      autoRotateSpeed={0.6}
      enableZoom={false}
      enablePan={false}
      enableRotate={false}
      target={[0, 0, 0]}
    />
  );
}

// --- Public component -----------------------------------------------------

export function DataFlow3D({ className = "" }: { className?: string }) {
  return (
    <div className={`relative ${className}`} aria-hidden="true">
      <Canvas
        camera={{ position: [3.2, 1.6, 6.5], fov: 42 }}
        dpr={[1, 1.5]}
        gl={{ antialias: true, alpha: true, powerPreference: "high-performance" }}
        style={{ background: "transparent" }}
      >
        <ambientLight intensity={0.18} />
        {/* Persimmon core light from the central node */}
        <pointLight position={[0, 0, 0]} color={PERSIMMON} intensity={3.5} distance={6} decay={1.6} />
        {/* Cool fill from the corners */}
        <pointLight position={[5, 4, 5]}    color={CYAN} intensity={0.6} distance={10} />
        <pointLight position={[-5, -4, -5]} color={CYAN} intensity={0.4} distance={10} />

        <BoundarySphere />
        <CentralNode />

        {SOURCES.map((s) => (
          <SourcePlinth key={s.label} label={s.label} position={s.position} />
        ))}

        {SOURCES.map((s, i) => (
          <DataStream key={`stream-${s.label}`} from={s.position} offset={i * 0.6} />
        ))}

        <CameraOrbit />
      </Canvas>
    </div>
  );
}
